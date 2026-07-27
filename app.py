import os
import csv
import io
import pandas as pd
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
# 1. Gestión de Clientes (Base de datos Local CSV -> Preparado para MySQL)
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

    nombre_final = nombre.strip() if nombre.strip() else "Cliente"
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

# Datasets estáticos del catálogo para estructurar tablas limpias
PRODUCTOS_DATA = [
    {"Producto": "Escritorio Minimalista Executive", "Descripción": "Escritorio compacto elaborado en piel sintética premium con estructura metálica.", "Colores": "Negro, Café, Azul Marino", "Existencias": 45, "Precio": 1200},
    {"Producto": "Silla Ergonómica Pro", "Descripción": "Silla de oficina con soporte lumbar ajustable y malla transpirable.", "Colores": "Negro, Gris", "Existencias": 30, "Precio": 2500},
    {"Producto": "Lámpara LED Smart Desk", "Descripción": "Lámpara de escritorio con regulador táctil y puerto de carga USB.", "Colores": "Blanco, Negro", "Existencias": 60, "Precio": 600}
]

# ------------------------------------------------------------------
# 2. Grafo RAG Filtrado (Sin mostrar datos sensibles)
# ------------------------------------------------------------------
class RAGState(TypedDict):
    question: str
    user_info: dict
    cp_info: str
    context: List[Document]
    answer: str

@st.cache_resource
def setup_rag_graph():
    docs: List[Document] = []
    data_dir = "data"
    
    files_to_load = [
        ("catalogo_productos.txt", TextLoader, {"encoding": "utf-8"}),
        ("politicas_envio.txt", TextLoader, {"encoding": "utf-8"})
    ]
    
    for file_name, loader_cls, loader_kwargs in files_to_load:
        file_path = os.path.join(data_dir, file_name)
        if os.path.exists(file_path):
            loader = loader_cls(file_path=file_path, **loader_kwargs)
            docs.extend(loader.load())
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    def retrieve_node(state: RAGState) -> dict:
        return {"context": retriever.invoke(state["question"])}

    def generate_node(state: RAGState) -> dict:
        user = state["user_info"]
        cp = state.get("cp_info", "").strip()
        
        info_envio = ""
        if cp:
            if cp.isdigit() and 1000 <= int(cp) <= 16999:
                info_envio = "🚚 **Zona Centro / CDMX:** Entrega en 24-48 hrs. Envío Gratis en compras > $500 MXN."
            elif cp.isdigit() and 50000 <= int(cp) <= 57999:
                info_envio = "🚚 **Zona Metropolitana / Edo. Méx:** Entrega en 2-3 días hábiles. Costo: $120 MXN."
            else:
                info_envio = "🚚 **Resto de la República:** Entrega en 3-5 días hábiles vía FedEx/DHL. Costo: $200 MXN."

        respuesta = f"¡Hola **{user['nombre']}**! Aquí tienes la información solicitada de nuestro catálogo:\n\n"
        if info_envio:
            respuesta += f"{info_envio}\n\n"
            
        return {"answer": respuesta}

    builder = StateGraph(RAGState)
    builder.add_node("retrieve", retrieve_node)
    builder.add_node("generate", generate_node)
    
    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "generate")
    builder.add_edge("generate", END)
    
    return builder.compile()

# ------------------------------------------------------------------
# 3. Interfaz de Usuario
# ------------------------------------------------------------------
if "user_data" not in st.session_state:
    st.session_state.user_data = None

if not st.session_state.user_data:
    st.markdown("## 👋 ¡Hola!")
    st.markdown("### Soy **Blink**, tu asistente personal.")
    st.markdown("Por favor ingresa tu nombre y correo para acceder al catálogo completo y tus beneficios de cliente.")
    st.write("---")

    with st.form(key="login_form"):
        input_nombre = st.text_input("¿Cómo te gusta que te llamen?", placeholder="Ej. Rubén Leñero")
        input_email = st.text_input("Tu correo electrónico:", placeholder="ejemplo@correo.com")
        submit_btn = st.form_submit_button("¡Empezar a conversar!")

        if submit_btn:
            if not input_email or "@" not in input_email or "." not in input_email:
                st.error("Por favor, ingresa un correo electrónico válido.")
            else:
                st.session_state.user_data = buscar_o_registrar_cliente(input_email, input_nombre)
                st.rerun()

    st.stop()

# Menú lateral
with st.sidebar:
    st.markdown("### 👤 Tu Perfil")
    st.write(f"**Cliente:** {st.session_state.user_data['nombre']}")
    st.write(f"**Correo:** {st.session_state.user_data['email']}")
    st.write("---")
    if st.button("Cerrar Sesión"):
        st.session_state.user_data = None
        st.rerun()

st.title("🤖 Chat con Blink")
st.markdown(f"¡Hola de nuevo, **{st.session_state.user_data['nombre']}**! Qué gusto saludarte. 😊")

# ------------------------------------------------------------------
# Entradas del Cliente (Pregunta + Código Postal)
# ------------------------------------------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    question = st.text_input("Escribe tu mensaje aquí:", placeholder="Ej. ¿Qué escritorios o sillas tienen disponibles?")

with col2:
    cp_input = st.text_input("📮 Código Postal (Envío):", placeholder="Ej. 01000", max_chars=5)

if st.button("Enviar Consulta") and question:
    with st.spinner("Blink está procesando tu solicitud..."):
        graph = setup_rag_graph()
        
        result = graph.invoke({
            "question": question,
            "user_info": st.session_state.user_data,
            "cp_info": cp_input,
            "context": [],
            "answer": ""
        })
        
        st.markdown("### Respuesta de Blink:")
        st.write(result["answer"])

        # VALIDACIÓN DE CLIENTE REGISTRADO PARA MOSTRAR LA TABLA CON PRECIOS
        if st.session_state.user_data.get("email"):
            st.markdown("### 📋 Catálogo de Productos Disponible")
            
            # Convertir catálogo a DataFrame / Tuplas estructuradas
            df_productos = pd.DataFrame(PRODUCTOS_DATA)
            
            # Formatear precio para la vista
            df_productos["Precio ($ MXN)"] = df_productos["Precio"].apply(lambda x: f"${x:,.2f} MXN")
            
            # Mostrar tabla interactiva sin exponer listas de control internas
            st.dataframe(
                df_productos[["Producto", "Descripción", "Colores", "Existencias", "Precio ($ MXN)"]],
                use_container_width=True,
                hide_index=True
            )

            # Botón de Descarga en CSV / Excel para Impresión/Resguardo del Cliente
            csv_buffer = io.StringIO()
            df_productos.to_csv(csv_buffer, index=False)
            
            st.download_button(
                label="📥 Descargar Catálogo en CSV / Para Imprimir",
                data=csv_buffer.getvalue(),
                file_name=f"catalogo_productos_{st.session_state.user_data['nombre'].replace(' ', '_')}.csv",
                mime="text/csv"
            )