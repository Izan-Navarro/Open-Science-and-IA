# Procesamiento de PDFs con Grobid

Este proyecto contiene un conjunto de scripts en Python que interactúan con el servicio Grobid para procesar documentos PDF. Los scripts realizan varias tareas, incluyendo la generación de nubes de palabras basadas en los resúmenes (abstracts), el conteo de las figuras en los artículos y la extracción de enlaces del contenido. El proyecto utiliza Docker para la contenedorización y Docker Compose para la orquestación de servicios.

## Descripción

Este proyecto aprovecha Grobid, una biblioteca de aprendizaje automático para extraer información de documentos académicos en formato PDF. Los tres scripts realizan las siguientes tareas:

1. **Generador de Nube de Palabras**: Crea una nube de palabras a partir del resumen (abstract) de cada artículo.
2. **Conteo de Figuras**: Cuenta el número de figuras en cada artículo y genera un gráfico de barras.
3. **Extracción de Enlaces**: Extrae y guarda las URL encontradas en el texto de cada artículo.

## Requisitos

- Docker
- Docker Compose
- Python 3.9+
- Grobid (Ejecutándose en un contenedor Docker)
- Bibliotecas Python necesarias:
    - `requests`
    - `matplotlib`
    - `wordcloud`
    - `nltk`

Para instalar las dependencias de Python, se incluye un archivo `requirements.txt`.

## Instrucciones de Instalación

1. Clona este repositorio:

    ```bash
    git clone https://github.com/tu-repositorio/pdftools.git
    cd pdftools
    ```

2. Construye las imágenes Docker utilizando Docker Compose:

    ```bash
    docker-compose up --build
    ```

   Este comando construirá las imágenes Docker necesarias para la aplicación y el servicio Grobid.

3. Asegúrate de tener tus archivos PDF en el directorio `./data/papers/`. El programa buscará los PDFs allí.

## Instrucciones de Ejecución

Para ejecutar los scripts, puedes ejecutar todo el proyecto utilizando Docker Compose:

```bash
docker-compose up
```


También se puede ejecutar cada uno de los scripts por separado asi:
```
docker exec -it wordcloud_app python /app/script.py
docker exec -it wordcloud_app python /app/figures_script.py
docker exec -it wordcloud_app python /app/links_script.py
```

Para ejecutar las pruebas (después de ejecutar los scripts):

```
docker-compose run tests
```
