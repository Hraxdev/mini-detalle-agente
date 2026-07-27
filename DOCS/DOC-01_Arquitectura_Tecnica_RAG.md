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
