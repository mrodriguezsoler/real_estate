import os
import sys
import traceback
from ad import Ad
from typing import Dict, List, Any

from crawler import crawler
from database import upload_to_database
from extract import load_json, extract_data



def main(delay: int, start_city: str) -> None:
    """Orquesta la ejecución de todas las funciones de la carpeta src
    
    Argumentos:
        delay: int -> Tiempo promedio en segundos entre solicitudes HTTP
        start_city: str -> Ciudad por la que empezar a scrapear
    
    Devuelve:
        None
    """
    # Se cargan los diccionarios de mapeos
    feature_map_path: str = '../maps/feature_map.json'
    property_type_map_path: str = '../maps/property_type_map.json'
    feature_map, property_type_map = load_json(feature_map_path, property_type_map_path)

    # Se recorre cada anuncio y se almacenan los datos relevantes
    for city, page, data in crawler(delay, start_city):
        content: List[Dict[str, Any]] = data.get('items')
        if content is None:
            continue

        # Se añaden los datos de los anuncios en la base de datos
        for ad_raw in content:
            ad: Ad = extract_data(ad_raw, feature_map, property_type_map)

            try:
                upload_to_database(ad)
                print(
                    f'Se subió correctamente el anuncio de ID de fotocasa \"{ad.id}\" de la '
                    f'página {page} de la ciudad \"{city.replace('-', ' ')}\"'
                )

            except Exception as err:
                print(err)
                traceback.print_exc()
                continue



if __name__ == '__main__':
    while True:
        try:  # Se comprueba que el delay introducido es válido
            delay: int = int(input('Introduce un valor de retraso entre solicitudes  '))
        except ValueError:
            print('[AVISO] Introduce un valor de retraso entre solicitudes válido')
            continue
        break

    print('\n')

    # Se recuperan los nombres de ciudades válidos
    with os.scandir("../payloads/") as payloads:
        cities: List[str] = [payload.name.replace('-', ' ').replace('.json', '') for payload in payloads]

    # Se comprueba que la ciudad introducida es válida
    print('Teniendo en cuenta que el programa scrapea las ciudades en el siguiente orden:')
    for city in cities:
        print(city)

    while True:
        start_city: str = input('Introduce el nombre de la ciudad a partir de la cual deseas empezar a scrapear  ')

        if start_city not in cities:
            print('[AVISO] Introduce una ciudad válida de la lista de arriba')
            continue
        break
    
    # Se lanza el programa
    main(delay, start_city)