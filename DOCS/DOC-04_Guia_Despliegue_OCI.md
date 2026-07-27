4. Información Disponible para Consulta

El asistente puede proporcionar información como:

Datos generales
Nombre del producto.
Categoría.
Descripción.
Disponibilidad.
Características técnicas
Materiales.
Dimensiones.
Peso.
Colores disponibles.
Personalización.
Inventario
Existencias disponibles.
Estado del producto.
5. Control de Información Comercial

El campo:

"requiere_autenticacion_precio": true
permite establecer reglas de seguridad comercial.

Cuando un usuario solicita precio:

El sistema valida el perfil del usuario.
Identifica si cuenta con autorización.
Muestra información comercial correspondiente.
6. Ejemplo de Interacción
Consulta del usuario:

"¿Tienen el Set de Escritorio Minimalista y de qué material es?"

Respuesta esperada:

"Contamos con el Set de Escritorio Minimalista disponible en stock. Está elaborado en piel sintética premium y disponible en diferentes colores. Si deseas conocer el precio asignado a tu cuenta, es necesario validar tu correo registrado."
7. Integración con RAG

El catálogo participa dentro del flujo:
Catálogo de Productos
          |
          |
Procesamiento documental
          |
          |
Embeddings
          |
          |
FAISS Vector Store
          |
          |
Recuperación de contexto
         |
         |
Respuesta del asistente

8. Evolución Futura

La estructura puede evolucionar para integrarse con:

Bases de datos empresariales.
Sistemas ERP.
Inventarios en tiempo real.
Servicios cloud.

---

# DOC-04_Guia_Despliegue_OCI.md

Crea el último archivo:

```text
DOC-04_Guia_Despliegue_OCI.md
# Guía de Despliegue Cloud y Preparación OCI

## Proyecto

**Asistente Virtual E-commerce - Mini Detalle**

---

# 1. Objetivo del Documento

Este documento describe la estrategia prevista para llevar el asistente virtual desde un ambiente local de desarrollo hacia una infraestructura cloud utilizando Oracle Cloud Infrastructure (OCI).

Actualmente la aplicación se encuentra en fase funcional local y este documento servirá como guía para la etapa de despliegue.

---

# 2. Estado Actual del Proyecto

La aplicación actualmente opera bajo un entorno local utilizando:

- Python 3.10+
- Streamlit
- LangChain
- FAISS
- OpenAI API

El desarrollo y pruebas iniciales se realizan en ambiente Windows.

---

# 3. Objetivo de Despliegue Cloud

La siguiente fase contempla publicar la aplicación en Oracle Cloud Infrastructure para obtener:

- Disponibilidad pública.
- Mayor capacidad de procesamiento.
- Ambiente accesible para demostración.
- Integración con servicios cloud.

---

# 4. Alternativas de Implementación OCI

Las opciones consideradas son:

## OCI Compute Instance

Máquina virtual donde se instalará:

- Sistema operativo Linux.
- Python.
- Dependencias del proyecto.
- Aplicación Streamlit.

## OCI Container Instance

Alternativa basada en contenedores para facilitar:

- Portabilidad.
- Administración.
- Escalabilidad.

---

# 5. Proceso Previsto de Implementación

Las actividades consideradas son:

1. Crear recurso cloud en OCI.
2. Configurar entorno de ejecución.
3. Instalar dependencias.
4. Configurar variables de entorno.
5. Publicar aplicación Streamlit.
6. Configurar acceso externo.
7. Validar funcionamiento.

---

# 6. Variables de Configuración

La aplicación requiere gestionar información sensible mediante variables de entorno:

Ejemplo:
OPENAI_API_KEY=clave_segura

Las credenciales no deben almacenarse directamente dentro del código fuente.

---

# 7. Evidencia del Despliegue

Como parte de la entrega del proyecto se considera incluir evidencia visual:

- Captura de pantalla del asistente funcionando.
- Acceso mediante URL pública.
- Demostración de consultas realizadas.

---

# 8. Gestión de Logs y Monitoreo

Durante la operación cloud se deberá considerar monitoreo de:

- Inicio y cierre del servicio.
- Errores de aplicación.
- Disponibilidad del asistente.
- Fallos en recuperación RAG.
- Eventos relevantes del sistema.

---

# 9. Evolución del Proyecto

La implementación OCI representa una etapa posterior dentro de la evolución del asistente, permitiendo transformar una solución local en un servicio disponible en infraestructura cloud.
docs
│
├── DOC-01_Arquitectura_Tecnica_RAG.md
├── DOC-02_Base_Conocimiento_Operativa.md
├── DOC-03_Catalogo_Productos_RAG.md
└── DOC-04_Guia_Despliegue_OCI.md
