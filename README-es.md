
# py_text_in_order

([Leer en inglés](README.md))

En los datos obtenidos mediante OCR (Reconocimiento Óptico de
Caracteres), es común encontrar que las palabras no están en el orden
adecuado debido a errores en el procesamiento o a la estructura del
propio documento. Esto puede afectar la lectura y la interpretación del
texto extraído. Aquí presentamos un conjunto de herramientas para
procesar y ordenar correctamente las palabras en documentos digitales,
mejorando así la organización del texto y facilitando su análisis.

## Módulo de Procesamiento de Texto

Este módulo ofrece varias funciones clave para cargar, extraer, y
ordenar las palabras detectadas mediante OCR, organizándolas en líneas
coherentes de texto. Las funciones principales son:

### Funciones Principales

- **`cargar_datos_ocr(ruta_json)`**: Esta función carga los datos OCR
  desde un archivo JSON, retornando un diccionario con el contenido. Es
  útil cuando los resultados del OCR están almacenados en este formato.

- **`extraer_palabras(datos_ocr)`**: Extrae las palabras y sus
  correspondientes coordenadas de los datos OCR. Devuelve una lista de
  diccionarios que representa cada palabra junto con su posición en la
  imagen (coordenadas), lo que permite ordenar y procesar las palabras
  correctamente.

- **`ordenar_palabras(palabras, tolerancia_vertical=6)`**: Esta función
  organiza las palabras extraídas en líneas, tomando en cuenta las
  posiciones verticales y horizontales. Esto es útil para reconstruir
  correctamente el texto cuando las palabras no están en el orden
  adecuado.

- **`agrupar_palabras_por_linea(palabras_ordenadas, tolerancia_vertical=6)`**:
  Agrupa las palabras en líneas de texto coherentes, según su posición,
  y devuelve una lista de líneas de texto ordenadas.

### Example Usage

``` python
directorio_entrada = './directorio_entrada'
directorio_salida = './directorio_salida'
procesar_directorio(directorio_entrada, directorio_salida)
```
