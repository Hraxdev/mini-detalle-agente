<h1 align="center">
🤖 Asistente Virtual E-commerce
</h1>

<h3 align="center">
Mini Detalle
</h3>

<p align="center">

Proyecto desarrollado para el <b>Challenge Técnico del Programa Oracle Next Education (ONE) / Alura Latam</b>

</p>
<p align="center">

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white">

<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">

<img src="https://img.shields.io/badge/LangChain-00A67E?style=for-the-badge">

<img src="https://img.shields.io/badge/FAISS-00599C?style=for-the-badge">

<img src="https://img.shields.io/badge/OpenAI-GPT--3.5-412991?style=for-the-badge">

<img src="https://img.shields.io/badge/Oracle-OCI-F80000?style=for-the-badge&logo=oracle&logoColor=white">

</p>
---
## 📷 Vista de la aplicación

<p align="center">
  <img src="docs/interfaz.png" width="900">
</p>

---
## 📋 Descripción del Proyecto
El Asistente Virtual para **Mini Detalle** es un agente RAG (*Retrieval-Augmented Generation*) diseñado para automatizar la atención a clientes y prospectos dentro del e-commerce:
1. **Identificación de usuarios:** Clasifica al usuario por su correo electrónico (Cliente Registrado vs. Prospecto).
2. **Control de Precios:** Oculta precios a los prospectos e invita a la conversión; muestra listas de precios personalizadas a clientes registrados.
3. **Atención Inteligente:** Responde sobre existencias, inventarios, fichas técnicas y tiempos de entrega por código postal usando RAG con LangChain y FAISS.

---

## 🛠️ Tecnologías Utilizadas
| Tecnología | Función |
|------------|---------|
| Python 3.10+ | Lenguaje de programación |
| Streamlit | Interfaz web |
| LangChain | Framework RAG |
| FAISS | Base de datos vectorial |
| OpenAI GPT-3.5 Turbo | Modelo de IA |
| OpenAI Embeddings | Generación de embeddings |
| Oracle Cloud Infrastructure (OCI) | Despliegue en la nube |

---

## 🚀 Instalación y Ejecución Local

1. **Clonar el repositorio:**
```bash
git clone [https://github.com/TU_USUARIO/mini-detalle-agente.git](https://github.com/TU_USUARIO/mini-detalle-agente.git)
cd mini-detalle-agente
```

2. **Crear y activar entorno virtual:**
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno (`.env`):**
Crea un archivo `.env` en la raíz con el contenido:
```env
OPENAI_API_KEY=tu_clave_api_aqui
```

5. **Ejecutar la aplicación:**
```bash
streamlit run app.py
```
Accede desde tu navegador a `http://localhost:8501`.

---

## ☁️ Despliegue en Oracle Cloud Infrastructure (OCI)
---

## ✨ Funcionalidades

- ✅ Identificación automática de clientes registrados.
- ✅ Detección de prospectos.
- ✅ Consulta inteligente mediante IA (RAG).
- ✅ Búsqueda semántica con FAISS.
- ✅ Consulta de inventario.
- ✅ Consulta de fichas técnicas.
- ✅ Consulta de tiempos de entrega.
- ✅ Respuestas generadas con OpenAI.
- 
## ☁️ Despliegue

Actualmente el proyecto se ejecuta en un entorno local sobre Windows para su desarrollo y pruebas.

La siguiente etapa del proyecto contempla su despliegue en Oracle Cloud Infrastructure (OCI).

---

# 📚 Documentación Técnica

Consulta los documentos técnicos del proyecto:
 - 📐 [DOC-01 - Arquitectura Técnica y Estrategia RAG](./docs/DOC-01_Arquitectura_Tecnica_RAG.md)

 - 📘 [DOC-02 - Base de Conocimiento Operativa](./docs/DOC-02_Base_Conocimiento_Operativa.md)
   
 - 🛒 [DOC-03 - Catálogo de Productos RAG](./docs/DOC-03_Catalogo_Productos_RAG.md)

 - ☁️ [DOC-04 - Guía de Despliegue OCI](./docs/DOC-04_Guia_Despliegue_OCI.md)
   
