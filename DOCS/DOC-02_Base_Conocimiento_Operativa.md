# Manual de Políticas Operativas y Base de Conocimiento

## Proyecto

**Asistente Virtual E-commerce - Mini Detalle**

## Descripción General

Este documento define la información operativa y comercial utilizada como fuente de conocimiento para el asistente virtual basado en arquitectura RAG.

La información contenida permite al agente responder consultas relacionadas con productos, envíos, métodos de pago, precios, garantías y devoluciones, manteniendo respuestas consistentes con las reglas de negocio establecidas.

---

# 1. Objetivo de la Base de Conocimiento

La base de conocimiento tiene como finalidad proporcionar información estructurada que permita al asistente:

- Resolver preguntas frecuentes.
- Orientar a clientes y prospectos.
- Consultar políticas comerciales.
- Aplicar reglas de acceso a información sensible.
- Mejorar la experiencia de atención digital.

---

# 2. Políticas de Envío y Entrega

El asistente solicita el Código Postal (CP) del usuario para identificar la zona logística y proporcionar información estimada de entrega.

## Tiempos estimados

| Zona logística | Tiempo estimado |
|---|---|
| Metropolitana / Local | 24 a 48 horas hábiles |
| Nacional estándar | 3 a 5 días hábiles |
| Zona extendida o difícil acceso | 5 a 8 días hábiles |

## Costos de envío

Las condiciones de envío pueden variar dependiendo del tipo de cliente y condiciones comerciales:

- Clientes B2B pueden contar con beneficios según monto mínimo de compra.
- Prospectos o clientes minoristas pueden estar sujetos a tarifas de paquetería.

---

# 3. Políticas de Precios y Acceso Comercial

Los precios son información comercial protegida y dependen del perfil del usuario.

El asistente puede proporcionar:

- Información general del producto.
- Características técnicas.
- Disponibilidad.
- Especificaciones.

La consulta de precios requiere validación del usuario.

---

# 4. Listas Comerciales

El sistema contempla diferentes niveles comerciales:

| Lista | Segmento |
|---|---|
| Lista 1 | Público general / Referencial |
| Lista 2 | Cliente frecuente / Minorista |
| Lista 3 | Mayorista / Distribuidor |
| Lista 4 | Convenio / Cuenta especial |

La lista aplicable dependerá del perfil comercial asignado.

---

# 5. Métodos de Pago

Los métodos disponibles pueden incluir:

- Tarjetas de crédito y débito.
- Transferencias SPEI.
- Crédito comercial autorizado.

Las condiciones pueden variar según el tipo de cliente.

---

# 6. Garantías y Devoluciones

## Reporte de incidencias

Las incidencias deberán reportarse dentro de un plazo máximo de:

**7 días hábiles posteriores a la recepción del producto.**

## Garantía

La cobertura depende del tipo de producto:

- Garantías estándar de 30 a 90 días naturales.

## Reembolsos

El proceso contempla:

1. Recepción e inspección del producto.
2. Validación de condiciones.
3. Autorización del reembolso.
4. Aplicación al mismo método de pago utilizado.

Tiempo estimado:

**3 a 5 días hábiles posteriores a la aprobación.**

---

# 7. Reglas de Respuesta del Asistente

Para mantener respuestas confiables, el agente debe:

- No inventar información.
- No proporcionar precios sin validación.
- Solicitar datos adicionales cuando sean necesarios.
- Utilizar únicamente información disponible en la base de conocimiento.
- Canalizar consultas comerciales cuando corresponda.

---

# 8. Integración con Arquitectura RAG

Esta información representa una fuente documental que puede ser procesada mediante:

- Ingesta documental.
- Fragmentación de contenido (*chunking*).
- Generación de embeddings.
- Indexación vectorial mediante FAISS.
- Recuperación semántica para generación de respuestas.
