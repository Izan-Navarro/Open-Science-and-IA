
## 1. Introducción
Este proyecto tiene como objetivo analizar 10 artículos de acceso abierto utilizando Grobid u otras herramientas de análisis de texto. Se implementan tres tareas principales:

1. Generación de una nube de palabras clave a partir de los resúmenes.
2. Creación de una visualización con el número de figuras por artículo.
3. Extracción de una lista de enlaces presentes en cada artículo.

A continuación, se detalla la validación de cada una de estas tareas.

---

## 2. Validación de los Resultados

### 2.1 Nube de Palabras Clave
**Procedimiento:**
- Se extrae el abstract de cada artículo en formato XML mediante Grobid.
- Se limpia el texto eliminando stopwords y caracteres especiales.
- Se genera una nube de palabras con la librería WordCloud.

**Validación:**
- Se comparan las palabras clave obtenidas con las keywords listadas en los artículos cuando están disponibles.
- Se verifica manualmente que las palabras clave sean relevantes y representativas del contenido.

### 2.2 Visualización del Número de Figuras por Artículo
**Procedimiento:**
- Se extrae el contenido completo del artículo en XML.
- Se cuentan las etiquetas `<figure>` dentro del XML.
- Se genera un gráfico de barras con Matplotlib para representar el número de figuras por artículo.

**Validación:**
- Se seleccionan aleatoriamente algunos artículos y se cuenta manualmente el número de figuras.
- Se comparan estos valores con los obtenidos automáticamente para comprobar la precisión del conteo.

### 2.3 Extracción de Enlaces
**Procedimiento:**
- Se analiza el texto extraído del artículo y se buscan enlaces mediante expresiones regulares.
- Se guardan los enlaces extraídos en archivos de texto por artículo.

**Validación:**
- Se seleccionan algunos artículos y se revisan manualmente los enlaces presentes en el texto.
- Se comparan los enlaces identificados manualmente con los extraídos automáticamente para verificar su correcta detección.

---

## 3. Conclusión
El proyecto sigue un enfoque sistemático para garantizar la precisión y fiabilidad de los resultados. La validación manual de una muestra de los artículos analizados permite corregir posibles errores y mejorar los algoritmos empleados. Además, el uso de herramientas estándar como Grobid y Matplotlib asegura la reproducibilidad del análisis.

Este documento proporciona una justificación clara de los métodos utilizados y los procedimientos seguidos para garantizar la validez de los resultados obtenidos.


