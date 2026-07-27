import os
import streamlit as st
from typing import TypedDict, List
from dotenv import load_dotenv

# Cargar variables de entorno (.env)
load_dotenv()

# Cargadores de documentos
from langchain_community.document_loaders import TextLoader, CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.documents import Document

# Componentes de LangGraph
from langgraph.graph import StateGraph, START, END

# Configuración de Streamlit
st.set_page_config(page_title="Asistente RAG Multi-archivo", page_icon="🤖")
st.title("🤖 Asistente Virtual RAG (LangGraph - Multi-fuente)")

# 1. Definición del Estado del Grafo
class RAGState(TypedDict):
    question: str
    context: List[Document]
    answer: str

# 2. Configuración e Indexación de Múltiples Archivos desde la carpeta /data
@st.cache_resource
def setup_rag_graph():
    docs: List[Document] = []
    
    # Carpeta donde se encuentran los archivos
    data_dir = "data"
    
    # Lista de archivos requeridos y sus cargadores correspondientes
    files_to_load = [
        ("catalogo_productos.txt", TextLoader, {"encoding": "utf-8"}),
        ("clientes_registrados.csv", CSVLoader, {"encoding": "utf-8"}),
        ("politicas_envio.txt", TextLoader, {"encoding": "utf-8"})
    ]
    
    # Carga y consolidación de datos desde data/
    for file_name, loader_cls, loader_kwargs in files_to_load:
        file_path = os.path.join(data_dir, file_name)
        
        if not os.path.exists(file_path):
            st.error(f"No se encontró el archivo '{file_path}'. Verifica que la carpeta 'data' contenga este archivo.")
            st.stop()
        
        loader = loader_cls(file_path=file_path, **loader_kwargs)
        docs.extend(loader.load())
    
    # Vectorstore FAISS con Embeddings de OpenAI
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # NODO 1: Búsqueda de información relevante
    def retrieve_node(state: RAGState) -> dict:
        query = state["question"]
        retrieved_docs = retriever.invoke(query)
        return {"context": retrieved_docs}

    # NODO 2: Generación de respuesta basada en los documentos consultados
    def generate_node(state: RAGState) -> dict:
        query = state["question"]
        context_docs = state["context"]
        context_text = "\n\n".join([doc.page_content for doc in context_docs])
        
        prompt = f"""Eres un asistente de atención y soporte preciso. Responde a la pregunta del usuario basándote únicamente en el siguiente contexto proveniente del catálogo de productos, registro de clientes y políticas de envío:

Contexto:
{context_text}

Pregunta: {query}
Respuesta:"""
        
        response = llm.invoke(prompt)
        return {"answer": response.content}

    # CONSTRUCCIÓN DEL GRAFO
    builder = StateGraph(RAGState)
    builder.add_node("retrieve", retrieve_node)
    builder.add_node("generate", generate_node)
    
    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "generate")
    builder.add_edge("generate", END)
    
    return builder.compile()

# Inicializar el Grafo
graph = setup_rag_graph()

# 3. Interfaz de usuario con Streamlit
question = st.text_input("Ingresa tu consulta sobre clientes, catálogo o políticas:")

if st.button("Consultar") and question:
    with st.spinner("Buscando en las fuentes de información..."):
        initial_state = {"question": question, "context": [], "answer": ""}
        result = graph.invoke(initial_state)
        
        st.markdown("### Respuesta:")
        st.write(result["answer"])
        
        with st.expander("Ver fuentes consultadas"):
            for i, doc in enumerate(result["context"], 1):
                source = doc.metadata.get("source", "Desconocido")
                st.markdown(f"**Fuente {i} ({source}):**")
                st.text(doc.page_content)