import os
import csv
import streamlit as st
from typing import TypedDict, List
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader, CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langgraph.graph import StateGraph, START, END

load_dotenv()

st.set_page_config(page_title="Blink - Asistente Virtual", page_icon="👋", layout="centered")

# ------------------------------------------------------------------
# Registro y Búsqueda de Clientes en CSV Local
# ------------------------------------------------------------------
CSV_PATH = os.path.join("data", "clientes_registrados.csv")

def buscar_o_registrar_cliente(email: str, nombre: str = ""):
    email_clean = email.strip().lower()
    cliente_encontrado = None
    
    os.makedirs("data", exist_ok=True)
    
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("email", "").strip().lower() == email_clean:
                    cliente_encontrado = row
                    break

    if cliente_encontrado:
        return cliente_encontrado

    nombre_final = nombre.strip() if nombre.strip() else "Amigo/a"
    nuevo_cliente = {
        "email": email_clean,
        "nombre": nombre_final,
        "lista_precios": "Lista 1"
    }
    
    file_exists = os.path.exists(CSV_PATH)
    with open(CSV_PATH, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["email", "nombre", "lista_precios"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(nuevo_cliente)
        
    return nuevo_cliente

# ------------------------------------------------------------------
# Estado y Grafo RAG Local
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
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    def retrieve_node(state: RAGState) -> dict:
        query = state["question"]
        retrieved_docs = retriever.invoke(query)
        return {"context": retrieved_docs}

    def generate_node(state: RAGState) -> dict:
        context_docs = state["context"]
        user = state["user_info"]
        
        context_text = "\n\n".join([f"• {doc.page_content}" for doc in context_docs])
        
        respuesta = (
            f"¡Hola **{user['nombre']}**! Con gusto te apoyo.\n\n"
            f"De acuerdo con nuestra base de datos e información consultada, aquí tienes los detalles:\n\n"
            f"{context_text}\n\n"
            f"*(Perfil del usuario: {user['email']} | Nivel de tarifa: {user.get('lista_precios', 'Lista 1')})*"
        )
        return {"answer": respuesta}

    builder = StateGraph(RAGState)
    builder.add_node("retrieve", retrieve_node)
    builder.add_node("generate", generate_node)
    
    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "generate")
    builder.add_edge("generate", END)
    
    return builder.compile()

# ------------------------------------------------------------------
# Interfaz de Usuario (Streamlit)
# ------------------------------------------------------------------
if "user_data" not in st.session_state:
    st.session_state.user_data = None

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
                user_info = buscar_o_registrar_cliente(input_email, input_nombre)
                st.session_state.user_data = user_info
                st.rerun()

    st.stop()

# Menú lateral
with st.sidebar:
    st.markdown("### 👤 Tu Perfil")
    st.write(f"**Nombre:** {st.session_state.user_data['nombre']}")
    st.write(f"**Correo:** {st.session_state.user_data['email']}")
    st.write(f"**Nivel de Cliente:** {st.session_state.user_data.get('lista_precios', 'Lista 1')}")
    st.write("---")
    if st.button("Cerrar Sesión"):
        st.session_state.user_data = None
        st.rerun()

# Chat principal
st.title("🤖 Chat con Blink")
st.markdown(f"¡Hola de nuevo, **{st.session_state.user_data['nombre']}**! Qué gusto saludarte. 😊")
st.markdown("¿En qué te puedo apoyar hoy? Puedes preguntarme sobre productos, existencias, tus datos de cliente o políticas de envío.")

graph = setup_rag_graph()

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