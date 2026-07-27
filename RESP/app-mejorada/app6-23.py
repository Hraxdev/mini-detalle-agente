import os
import csv
import streamlit as st
from typing import TypedDict, List
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Cargadores de documentos
from langchain_community.document_loaders import TextLoader, CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# Embeddings y LLM
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOCIGenAI

# Componentes de LangGraph
from langgraph.graph import StateGraph, START, END

# Configuración de página
st.set_page_config(page_title="Blink - Asistente Virtual", page_icon="👋", layout="centered")

# ------------------------------------------------------------------
# Funciones para la Gestión de Clientes (Corpus)
# ------------------------------------------------------------------
CSV_PATH = os.path.join("data", "clientes_registrados.csv")

def buscar_o_registrar_cliente(email: str, nombre: str = ""):
    """Busca al cliente por email. Si no existe, lo registra en el CSV como cliente nuevo."""
    email_clean = email.strip().lower()
    cliente_encontrado = None
    
    # Asegurar que la carpeta data exista
    os.makedirs("data", exist_ok=True)
    
    # 1. Buscar si el cliente ya existe
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("email", "").strip().lower() == email_clean:
                    cliente_encontrado = row
                    break

    # 2. Si existe, retornar sus datos
    if cliente_encontrado:
        return cliente_encontrado

    # 3. Si no existe, registrarlo dinámicamente en el CSV (Corpus)
    nombre_final = nombre.strip() if nombre.strip() else "Amigo/a"
    nuevo_cliente = {
        "email": email_clean,
        "nombre": nombre_final,
        "lista_precios": "Lista 1"  # Nivel por defecto para nuevos usuarios
    }
    
    file_exists = os.path.exists(CSV_PATH)
    with open(CSV_PATH, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["email", "nombre", "lista_precios"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(nuevo_cliente)
        
    return nuevo_cliente

# ------------------------------------------------------------------
# Manejo de Sesión del Usuario
# ------------------------------------------------------------------
if "user_data" not in st.session_state:
    st.session_state.user_data = None

# PANTALLA 1: ROMPER EL HIELO Y REGISTRO (Si no ha iniciado sesión)
if not st.session_state.user_data:
    st.markdown("## 👋 ¡Hola!")
    st.markdown("### Soy **Blink**, tu asistente personal.")
    st.markdown(
        "Para conocerte mejor y darte una atención personalizada con los detalles y precios que necesitas, "
        "por favor compárteme tu nombre y correo electrónico antes de empezar a platicar."
    )
    st.write("---")

    with st.form(key="welcome_form"):
        input_nombre = st.text_input("¿Cómo te gusta que te llamen?", placeholder="Ej. Carlos Mendoza")
        input_email = st.text_input("Tu correo electrónico:", placeholder="ejemplo@correo.com")
        submit_btn = st.form_submit_button("¡Empezar a conversar!")

        if submit_btn:
            if not input_email or "@" not in input_email or "." not in input_email:
                st.error("Por favor, ingresa un correo electrónico válido para continuar.")
            else:
                # Guardar o recuperar cliente en el corpus
                user_info = buscar_o_registrar_cliente(input_email, input_nombre)
                st.session_state.user_data = user_info
                st.success(f"¡Un gusto tenerte aquí, {user_info['nombre']}!")
                st.rerun()

    st.stop()  # No ejecuta el resto hasta autenticarse

# ------------------------------------------------------------------
# PANTALLA 2: INTERFAZ DE CHAT (Usuario Autenticado)
# ------------------------------------------------------------------

# Menú lateral profesional y atento
with st.sidebar:
    st.markdown("### 👤 Tu Perfil")
    st.write(f"**Nombre:** {st.session_state.user_data['nombre']}")
    st.write(f"**Correo:** {st.session_state.user_data['email']}")
    st.write(f"**Nivel de Cliente:** {st.session_state.user_data.get('lista_precios', 'Lista 1')}")
    st.write("---")
    if st.button("Cerrar Sesión"):
        st.session_state.user_data = None
        st.rerun()

# Bienvenida en el Chat principal
st.title("🤖 Chat con Blink")
st.markdown(f"¡Hola de nuevo, **{st.session_state.user_data['nombre']}**! Que gusto saludarte. 😊")
st.markdown("¿En qué te puedo apoyar hoy? Puedes preguntarme sobre productos, existencias, tus datos de cliente o políticas de envío.")

# ------------------------------------------------------------------
# LangGraph + OCI GenAI + Contexto Personalizado
# ------------------------------------------------------------------
class RAGState(TypedDict):
    question: str
    user_info: dict
    context: List[Document]
    answer: str

@st.cache_resource
def setup_rag_graph():
    docs: List[Document] = []
    data_dir = "data"
    
    files_to_load = [
        ("catalogo_productos.txt", TextLoader, {"encoding": "utf-8"}),
        ("clientes_registrados.csv", CSVLoader, {"encoding": "utf-8"}),
        ("politicas_envio.txt", TextLoader, {"encoding": "utf-8"})
    ]
    
    for file_name, loader_cls, loader_kwargs in files_to_load:
        file_path = os.path.join(data_dir, file_name)
        if os.path.exists(file_path):
            loader = loader_cls(file_path=file_path, **loader_kwargs)
            docs.extend(loader.load())
    
    # Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # Modelo en OCI
    COMPARTMENT_OCID = os.getenv("OCI_COMPARTMENT_OCID", "ocid1.compartment.oc1..tu_ocid_aqui")
    llm = ChatOCIGenAI(
        model_id="meta.llama-3-70b-instruct",
        service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
        compartment_id=COMPARTMENT_OCID,
        model_kwargs={"temperature": 0.2, "max_tokens": 600}
    )

    # NODO 1: Búsqueda
    def retrieve_node(state: RAGState) -> dict:
        query = state["question"]
        retrieved_docs = retriever.invoke(query)
        return {"context": retrieved_docs}

    # NODO 2: Generación Humana y Atenta
    def generate_node(state: RAGState) -> dict:
        query = state["question"]
        context_docs = state["context"]
        user = state["user_info"]
        
        context_text = "\n\n".join([doc.page_content for doc in context_docs])
        
        prompt = f"""Eres Blink, un asistente de soporte virtual atento, amable, profesional y muy humano. No seas solemne ni acartonado. 

Estás conversando con:
- Nombre: {user['nombre']}
- Email: {user['email']}
- Nivel de tarifa asignado: {user.get('lista_precios', 'Lista 1')}

Instrucciones:
1. Responde a la duda utilizando el contexto provisto abajo.
2. Dirígete a la persona por su nombre de forma natural.
3. Si consulta sobre precios, considera la lista de precios que le corresponde de acuerdo a su perfil o explícasela de forma clara.
4. Sé atento y útil.

Contexto:
{context_text}

Pregunta del usuario: {query}
Respuesta de Blink:"""
        
        response = llm.invoke(prompt)
        return {"answer": response.content}

    # Construcción del Grafo
    builder = StateGraph(RAGState)
    builder.add_node("retrieve", retrieve_node)
    builder.add_node("generate", generate_node)
    
    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "generate")
    builder.add_edge("generate", END)
    
    return builder.compile()

graph = setup_rag_graph()

# ------------------------------------------------------------------
# Entrada del Usuario
# ------------------------------------------------------------------
question = st.text_input("Escribe tu mensaje aquí:")

if st.button("Enviar") and question:
    with st.spinner("Blink está pensando..."):
        initial_state = {
            "question": question,
            "user_info": st.session_state.user_data,
            "context": [],
            "answer": ""
        }
        result = graph.invoke(initial_state)
        
        st.markdown("### Respuesta de Blink:")
        st.write(result["answer"])
        
        with st.expander("Ver detalle de las fuentes consultadas"):
            for i, doc in enumerate(result["context"], 1):
                source = doc.metadata.get("source", "Desconocido")
                st.markdown(f"**Fuente {i} ({source}):**")
                st.text(doc.page_content)