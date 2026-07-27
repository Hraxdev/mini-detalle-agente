# 🤖 Asistente Virtual E-commerce — Mini Detalle

Proyecto desarrollado para el **Challenge Técnico del Programa Oracle Next Education (ONE) / Alura Latam**.

## 📋 Descripción del Proyecto
El Asistente Virtual para **Mini Detalle** es un agente RAG (*Retrieval-Augmented Generation*) diseñado para automatizar la atención a clientes y prospectos dentro del e-commerce:
1. **Identificación de usuarios:** Clasifica al usuario por su correo electrónico (Cliente Registrado vs. Prospecto).
2. **Control de Precios:** Oculta precios a los prospectos e invita a la conversión; muestra listas de precios personalizadas a clientes registrados.
3. **Atención Inteligente:** Responde sobre existencias, inventarios, fichas técnicas y tiempos de entrega por código postal usando RAG con LangChain y FAISS.

---

## 🛠️ Tecnologías Utilizadas
- **Lenguaje:** Python 3.10+
- **Framework UI:** Streamlit
- **Framework IA/RAG:** LangChain
- **Base de Datos Vectorial:** FAISS
- **Modelo LLM:** OpenAI GPT-3.5 Turbo / Embeddings
- **Infraestructura:** Oracle Cloud Infrastructure (OCI Compute VM)

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

1. Instancia **Ubuntu 22.04 LTS** en OCI Compute VM.
2. Regla de entrada (*Ingress Rule*) en OCI VCN habilitada en el **Puerto TCP 8501**.
3. Ejecución del proceso en segundo plano con `nohup` o `tmux`.