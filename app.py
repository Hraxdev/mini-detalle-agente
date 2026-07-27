import os
import streamlit as st
from typing import TypedDict, List
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.documents import Document

# Componentes de LangGraph
from langgraph.graph import StateGraph, START, END

# 1. Cargar variables de entorno (.env)
load_dotenv()

# Configuración de página de Streamlit
st.set_page_config(page_title="Asistente RAG - LangGraph", page_icon="🤖")
st.title("🤖 Asistente Virtual RAG (Powered by LangGraph)")

# ------------------------------------------------------------------
# Definición del Estado y el Grafo de LangGraph
# ------------------------------------------------------------------

# El estado almacena el flujo de datos entre los nodos del grafo
class RAGState(TypedDict):
    question: str
    context: List[Document]
    answer: str

@st.cache_resource
def setup_rag_graph():
    """Carga documentos, indexa en FAISS y construye el grafo de LangGraph."""
    pdf_path = "documento.pdf"  # Asegúrate de que coincida con el nombre de tu PDF
    
    if not os.path.exists(pdf_path):
        st.error(f"No se encontró el archivo '{pdf_path}'. Por favor, verifica la ruta.")
        st.stop()
        
    # Cargar e indexar el PDF
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # NODO 1: Recuperación de contexto (Retrieve)
    def retrieve_node(state: RAGState) -> dict:
        query = state["question"]
        retrieved_docs = retriever.invoke(query)
        return {"context": retrieved_docs}

    # NODO 2: Generación de respuesta con el LLM (Generate)
    def generate_node(state: RAGState) -> dict:
        query = state["question"]
        context_docs = state["context"]
        
        # Unir el contenido de los documentos recuperados
        context_text = "\n\n".join([doc.page_content for doc in context_docs])
        
        prompt = f"""Eres un asistente de soporte preciso. Responde a la pregunta del usuario utilizando únicamente el siguiente contexto provisto:

Contexto:
{context_text}

Pregunta: {query}
Respuesta:"""
        
        response = llm.invoke(prompt)
        return {"answer": response.content}

    # CONSTRUCCIÓN DEL GRAFO
    builder = StateGraph(RAGState)
    
    # Agregar nodos
    builder.add_node("retrieve", retrieve_node)
    builder.add_node("generate", generate_node)
    
    # Definir las conexiones (aristas)
    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "generate")
    builder.add_edge("generate", END)
    
    # Compilar el grafo
    graph = builder.compile()
    return graph

# Inicializar el grafo
graph = setup_rag_graph()

# ------------------------------------------------------------------
# Interfaz de Usuario con Streamlit
# ------------------------------------------------------------------

question = st.text_input("Realiza una pregunta sobre el documento:")

if st.button("Consultar") and question:
    with st.spinner("Buscando respuesta..."):
        # Ejecutar el grafo pasando el estado inicial
        initial_state = {"question": question, "context": [], "answer": ""}
        result = graph.invoke(initial_state)
        
        st.markdown("### Respuesta:")
        st.write(result["answer"])
        
        # Mostrar los fragmentos recuperados para transparencia
        with st.expander("Ver fuentes consultadas (Contexto)"):
            for i, doc in enumerate(result["context"], 1):
                st.markdown(f"**Fuente {i}:**")
                st.write(doc.page_content)