# Arquitectura Técnica y Estrategia RAG

## Proyecto

**Asistente Virtual E-commerce - Mini Detalle**

## Descripción General

El proyecto consiste en el desarrollo de un asistente virtual conversacional basado en Inteligencia Artificial Generativa y arquitectura **RAG (Retrieval-Augmented Generation)**.

El objetivo del sistema es proporcionar atención automatizada a clientes y prospectos mediante recuperación inteligente de información empresarial, permitiendo consultar productos, disponibilidad, características técnicas, políticas comerciales y tiempos estimados de entrega.

La solución combina modelos de lenguaje, recuperación semántica y reglas de negocio para ofrecer respuestas precisas, controladas y alineadas con la operación comercial de Mini Detalle.

---

# 1. Objetivos del Sistema

## 1.1 Identificación del Usuario

El asistente implementa un mecanismo de identificación mediante correo electrónico para clasificar al usuario dentro de dos perfiles principales:

- **Cliente registrado:** usuario con acceso a información comercial personalizada.
- **Prospecto:** usuario interesado que requiere orientación comercial y registro.

Esta clasificación permite aplicar diferentes reglas de acceso a la información.

---

## 1.2 Control de Información Comercial

El sistema implementa controles para proteger información sensible como precios y condiciones comerciales.

Los usuarios pueden consultar:

- Características de productos.
- Disponibilidad.
- Especificaciones técnicas.
- Información general.

La consulta de precios requiere validación del perfil comercial correspondiente.

---

## 1.3 Atención Comercial Automatizada

El asistente funciona como primer punto de contacto digital para:

- Resolver preguntas frecuentes.
- Orientar sobre productos.
- Capturar oportunidades comerciales.
- Canalizar usuarios hacia procesos de registro o contacto comercial.

---

## 1.4 Consulta de Entregas

El sistema utiliza el Código Postal del usuario como dato de referencia para proporcionar información relacionada con zonas logísticas y tiempos estimados de entrega.

---

# 2. Arquitectura General del Sistema

La solución está compuesta por los siguientes elementos:
Usuario
|
|
Streamlit Interface
|
|
Agente Conversacional
|
|
LangChain + Lógica RAG
|
|
FAISS Vector Store
|
|
Base de Conocimiento
(Productos, FAQ, Políticas)
|
|
OpenAI API

---

# 3. Pipeline RAG

## 3.1 Ingesta de Información

El sistema procesa documentos utilizados como fuente de conocimiento:

- Archivos PDF.
- Archivos CSV.
- Documentos JSON.
- Archivos Markdown.

La información corresponde a:

- Catálogo de productos.
- Fichas técnicas.
- Preguntas frecuentes.
- Políticas comerciales.

---

## 3.2 Procesamiento y Fragmentación

Los documentos son divididos en fragmentos de información (*chunks*) con el objetivo de conservar contexto semántico y permitir una recuperación eficiente.

Este proceso permite que el modelo consulte únicamente información relevante para cada pregunta.

---

## 3.3 Generación de Embeddings

Cada fragmento de información es transformado en representaciones vectoriales mediante embeddings.

Estos vectores permiten realizar búsquedas basadas en similitud semántica.

---

## 3.4 Almacenamiento Vectorial

Actualmente el proyecto utiliza **FAISS** como motor de búsqueda vectorial.

Sus funciones principales son:

- Almacenar embeddings.
- Recuperar información relacionada.
- Proporcionar contexto al modelo generativo.

---

## 3.5 Recuperación de Contexto

Cuando un usuario realiza una consulta:

1. El sistema analiza la intención.
2. Busca información relacionada en FAISS.
3. Recupera los fragmentos relevantes.
4. Envía el contexto al modelo de lenguaje.

---

## 3.6 Generación de Respuesta

El modelo genera una respuesta utilizando:

- La consulta del usuario.
- El contexto recuperado.
- Las reglas de negocio establecidas.

---

# 4. Control Conversacional y Guardrails

El asistente implementa reglas para mantener respuestas confiables:

## Restricciones

- No inventar información.
- No proporcionar precios sin autorización.
- No responder información inexistente.
- Solicitar datos adicionales cuando sean necesarios.

## Manejo de contingencias

Cuando la información requerida no está disponible, el sistema:

- Solicita mayor contexto.
- Sugiere contacto comercial.
- Indica las limitaciones de información disponible.

---

# 5. Tecnologías Utilizadas

| Tecnología | Uso |
|---|---|
| Python 3.10+ | Desarrollo del backend |
| Streamlit | Interfaz conversacional |
| LangChain | Orquestación del flujo RAG |
| FAISS | Base vectorial |
| OpenAI API | Modelo generativo y embeddings |
| VS Code | Entorno de desarrollo |

---

# 6. Evolución Futura

La arquitectura está preparada para evolucionar hacia infraestructura cloud mediante:

- Oracle Cloud Infrastructure (OCI).
- Servicios administrados.
- Mayor disponibilidad.
- Escalabilidad del servicio.

El despliegue cloud será documentado en una etapa posterior.
