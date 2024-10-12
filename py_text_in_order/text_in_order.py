import json
import os
from typing import List, Dict, Any

def cargar_datos_ocr(ruta_json: str) -> Dict[str, Any]:
    """
    Carga los datos OCR desde un archivo JSON.

    Args:
    ruta_json (str): Ruta al archivo JSON que contiene los datos OCR.

    Returns:
    Dict[str, Any]: Diccionario con los datos OCR cargados.
    """
    with open(ruta_json, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def extraer_palabras(datos_ocr: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extrae y procesa las palabras de los datos OCR.

    Args:
    datos_ocr (Dict[str, Any]): Diccionario con los datos OCR.

    Returns:
    List[Dict[str, Any]]: Lista de diccionarios, cada uno representando una palabra con sus coordenadas.
    """
    texto_completo = datos_ocr['text']
    palabras = []

    for token in datos_ocr['pages'][0]['tokens']:
        vertices = token['layout']['boundingPoly']['vertices']
        coordenadas = [(v.get('x', 0), v.get('y', 0)) for v in vertices]
        
        start_index = int(token['layout']['textAnchor']['textSegments'][0].get('startIndex', 0))
        end_index = int(token['layout']['textAnchor']['textSegments'][0].get('endIndex', start_index))
        texto = texto_completo[start_index:end_index].replace('\n', ' ')
        
        x_values = [v.get('x', 0) for v in vertices]
        y_values = [v.get('y', 0) for v in vertices]
        
        palabras.append({
            'texto': texto,
            'coordenadas': coordenadas,
            'x_min': min(x_values),
            'y_min': min(y_values),
            'x_center': sum(x_values) / len(vertices),
            'y_center': sum(y_values) / len(vertices)
        })

    return palabras

def ordenar_palabras(palabras: List[Dict[str, Any]], tolerancia_vertical: int = 6) -> List[Dict[str, Any]]:
    """
    Ordena las palabras en líneas y dentro de cada línea.

    Args:
    palabras (List[Dict[str, Any]]): Lista de palabras a ordenar.
    tolerancia_vertical (int): Tolerancia vertical para agrupar palabras en la misma línea.

    Returns:
    List[Dict[str, Any]]: Lista de palabras ordenadas.
    """
    lineas = []
    for palabra in palabras:
        for linea in lineas:
            if abs(palabra['y_center'] - linea[0]['y_center']) <= tolerancia_vertical:
                linea.append(palabra)
                break
        else:
            lineas.append([palabra])
    
    return [palabra for linea in sorted(lineas, key=lambda l: l[0]['y_center'])
            for palabra in sorted(linea, key=lambda w: w['x_center'])]

def agrupar_palabras_por_linea(palabras_ordenadas: List[Dict[str, Any]], tolerancia_vertical: int = 6) -> List[str]:
    """
    Agrupa las palabras en líneas de texto.

    Args:
    palabras_ordenadas (List[Dict[str, Any]]): Lista de palabras ordenadas.
    tolerancia_vertical (int): Tolerancia vertical para agrupar palabras en la misma línea.

    Returns:
    List[str]: Lista de líneas de texto.
    """
    lineas = []
    linea_actual = []
    y_anterior = None

    for palabra in palabras_ordenadas:
        y_actual = palabra['y_min']
        
        if y_anterior is None or abs(y_actual - y_anterior) <= tolerancia_vertical:
            linea_actual.append(palabra)
        else:
            lineas.append(''.join(p['texto'] for p in sorted(linea_actual, key=lambda p: p['x_min'])))
            linea_actual = [palabra]
        
        y_anterior = y_actual
    
    if linea_actual:
        lineas.append(''.join(p['texto'] for p in sorted(linea_actual, key=lambda p: p['x_min'])))
    
    return lineas

def procesar_archivo_json(ruta_json: str, directorio_salida: str) -> None:
    """
    Procesa un archivo JSON de OCR y guarda el resultado en un archivo de texto.

    Args:
    ruta_json (str): Ruta al archivo JSON de entrada.
    directorio_salida (str): Directorio donde se guardará el archivo de texto resultante.
    """
    datos_ocr = cargar_datos_ocr(ruta_json)
    palabras = extraer_palabras(datos_ocr)
    palabras_ordenadas = ordenar_palabras(palabras)
    lineas_texto = agrupar_palabras_por_linea(palabras_ordenadas)

    nombre_archivo = os.path.splitext(os.path.basename(ruta_json))[0] + "_procesado.txt"
    ruta_salida = os.path.join(directorio_salida, nombre_archivo)

    with open(ruta_salida, 'w', encoding='utf-8') as archivo:
        for linea in lineas_texto:
            archivo.write(linea + '\n')

def procesar_directorio(directorio_entrada: str, directorio_salida: str) -> None:
    """
    Procesa todos los archivos JSON en un directorio y guarda los resultados en otro directorio.

    Args:
    directorio_entrada (str): Directorio que contiene los archivos JSON de entrada.
    directorio_salida (str): Directorio donde se guardarán los archivos de texto resultantes.
    """
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)

    for archivo in os.listdir(directorio_entrada):
        if archivo.endswith('.json'):
            ruta_json = os.path.join(directorio_entrada, archivo)
            procesar_archivo_json(ruta_json, directorio_salida)
            print(f"Procesado: {archivo}")
