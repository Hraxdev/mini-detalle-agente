# Catálogo de Productos y Fichas Técnicas

## Proyecto

**Asistente Virtual E-commerce - Mini Detalle**

## Descripción General

Este documento define la estructura de información utilizada para representar productos, inventario y fichas técnicas dentro de la arquitectura RAG del asistente virtual.

El catálogo funciona como fuente de conocimiento estructurada para permitir consultas inteligentes sobre productos, características, disponibilidad y especificaciones técnicas.

---

# 1. Objetivo del Catálogo

El catálogo permite al asistente:

- Identificar productos mediante SKU o nombre.
- Consultar características técnicas.
- Informar disponibilidad.
- Proporcionar detalles relevantes del producto.
- Aplicar reglas comerciales relacionadas con precios.

---

# 2. Formatos Compatibles

La información puede almacenarse y procesarse mediante:

- JSON.
- CSV.
- Markdown.

Estos formatos permiten integrar información estructurada dentro del pipeline RAG.

---

# 3. Modelo de Datos del Producto

Cada producto cuenta con una estructura similar a:

```json
{
  "sku": "MD-KIT-001",
  "nombre": "Kit Detalle Gourmet Corporativo",
  "categoria": "Regalos y Detalles",
  "descripcion_corta": "Caja decorativa premium con selección de chocolates artesanales, café gourmet y taza térmica.",
  "existencias": 150,
  "disponibilidad": "En Stock",
  "especificaciones": {
    "dimensiones": "25x20x10 cm",
    "peso": "1.2 kg",
    "personalizable": true
  },
  "requiere_autenticacion_precio": true
}
