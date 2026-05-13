import os
import sys
import json
import math
import time
import random
import requests
from typing import Any, Dict, List, Generator
from requests.exceptions import ConnectionError, Timeout, RequestException



def get_total_pages(endpoint: str, payload: Dict[str, Any], headers: Dict[str, str], delay: int, city: str, ads_per_page=30) -> int:
    """Devuelve el número total de páginas de resultados para una ciudad

    Argumentos:
        endpoint: str -> Enlace al que se hacen las solicitudes HTTP
        payload: Dict[str, Any] -> Campos que se envían con la solicitud HTTP y que codifican una ciudad
        headers: Dict[str, str] -> Encabezados necesarios para la solicitud HTTP
        delay: int -> Tiempo promedio en segundos entre solicitudes HTTP
        city: str -> Ciudad de la que se quieren rastrear anuncios
        ads_per_page: int -> Número de anuncios por página de resultados. Por defecto son 30

    Devuelve:
        int -> Número de páginas de anuncios para una ciudad 
    """
    # Se hace la primera solicitud HTTP para una ciudad concreta
    time.sleep(random.uniform(delay - 1, delay + 1))

    MAX_RETRIES: int = 3
    BACKOFF_FACTOR: int = 10
    retries: int = 0

    while retries < MAX_RETRIES:
        try:
            response: requests.Response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            data: Dict[str, Any] = response.json()
            total_ads: int = data.get('totalItems', 0)

            return math.ceil(total_ads / ads_per_page)

        except (ConnectionError, Timeout) as err:
            retries += 1
            wait_time: int = BACKOFF_FACTOR * retries
            print('[AVISO] Se produjo un error de conexión al intentar conectar con el servidor de fotocasa')
            print(f'No se pudo recuperar el número de anuncios totales para la ciudad \"{city.replace('-', ' ')}\"')
            print(err)
            print(f'La solicitud al servidor se reintentará en {wait_time} segundos')
            time.sleep(wait_time)
            continue

        except requests.HTTPError as err:
            retries += 1
            wait_time: int = BACKOFF_FACTOR * retries
            print(f'[AVISO] Se obtuvo una respuesta inesperada del servidor de fotocasa con \"status={response.status_code}\"')
            print(f'No se pudo recuperar el número de anuncios totales para la ciudad \"{city.replace('-', ' ')}\"')
            print(err)
            print(f'La solicitud al servidor se reintentará en {wait_time} segundos')
            time.sleep(wait_time)
            continue

        except RequestException as err:
            retries += 1
            wait_time: int = BACKOFF_FACTOR * retries
            print('[AVISO] Ocurrió un error inesperado realizando la solicitud al servidor de fotocasa')
            print(f'No se pudo recuperar el número de anuncios totales para la ciudad \"{city.replace('-', ' ')}\"')
            print(err)
            print(f'La solicitud al servidor se reintentará en {wait_time} segundos')
            time.sleep(wait_time)
            continue

        except Exception as err:
            retries += 1
            wait_time: int = BACKOFF_FACTOR * retries
            print(
                '[AVISO] Ocurrió un error inesperado y no se pudo recuperar el número de anuncios totales para la ciudad '
                f'\"{city.replace('-', ' ')}\"'
            )
            print(err)
            print(f'La solicitud al servidor se reintentará en {wait_time} segundos')
            time.sleep(wait_time)
            continue

    print(f'Tras un total de {retries} intentos, no se pudo recuperar el número de anuncios totales para la ciudad \"{city.replace('-', ' ')}\"')
    sys.exit('Saliendo del programa...')



def fetch_page(endpoint: str, payload: Dict[str, Any], headers: Dict[str, str], city: str, page: int, delay: int) -> Dict[str, Any]:
    """Intercepta los datos de una página de anuncios de una ciudad concreta via API request

    Argumentos:
        endpoint: str -> Enlace al que se hacen las solicitudes HTTP
        payload: Dict[str, Any] -> Campos que se envían con la solicitud HTTP y que codifican una ciudad
        headers: Dict[str, str] -> Encabezados necesarios para la solicitud HTTP
        city: str -> Nombre de la ciudad de la que se quieren obtener anuncios
        page: int -> Página de resultados a la que se realiza la solicitud
        delay: int -> Tiempo promedio en segundos entre solicitudes HTTP
    
    Devuelve:
        Dict[str, Any] -> Respuesta del servidor en formato JSON
    """
    # Se ajusta el referer de los headers para la solicitud para simular una navegación real
    if page > 1:
        referer: str = (
            f"https://www.fotocasa.es/es/comprar/viviendas/{city}/todas-las-zonas/l"
            if page == 2 
            else f"https://www.fotocasa.es/es/comprar/viviendas/{city}/todas-las-zonas/l/{page - 1}"
        )
        headers["Referer"] = referer

    payload['pageNumber'] = page  # Se ajusta el número de página del payload para cada solicitud

    time.sleep(random.uniform(delay - 1, delay + 1))

    MAX_RETRIES: int = 3
    BACKOFF_FACTOR: int = 10
    retries: int = 0

    while retries < MAX_RETRIES:
        try:
            response: requests.Response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            data: Dict[str, Any] = response.json()

            return data
        
        except (ConnectionError, Timeout) as err:
            retries += 1
            wait_time: int = BACKOFF_FACTOR * retries
            print('[AVISO] Se produjo un error de conexión al intentar conectar con el servidor de fotocasa')
            print(f'No se pudieron recuperar los datos de la página {page} de resultados de la ciudad \"{city.replace('-', ' ')}\"')
            print(err)
            print(f'La solicitud al servidor se reintentará en {wait_time} segundos')
            time.sleep(wait_time)
            continue

        except requests.HTTPError as err:
            retries += 1
            wait_time: int = BACKOFF_FACTOR * retries
            print(f'[AVISO] Se obtuvo una respuesta inesperada del servidor de fotocasa con \"status={response.status_code}\"')
            print(f'No se pudieron recuperar los datos de la página {page} de resultados de la ciudad \"{city.replace('-', ' ')}\"')
            print(err)
            print(f'La solicitud al servidor se reintentará en {wait_time} segundos')
            time.sleep(wait_time)
            continue

        except RequestException as err:
            retries += 1
            wait_time: int = BACKOFF_FACTOR * retries
            print('[AVISO] Ocurrió un error inesperado al realizar la solicitud al servidor de fotocasa')
            print(f'No se pudieron recuperar los datos de la página {page} de resultados de la ciudad \"{city.replace('-', ' ')}\"')
            print(err)
            print(f'La solicitud al servidor se reintentará en {wait_time} segundos')
            time.sleep(wait_time)
            continue

        except Exception as err:
            retries += 1
            wait_time: int = BACKOFF_FACTOR * retries
            print(
                f'[AVISO] Ocurrió un error inesperado y no se pudieron recuperar los datos de la página {page} de resultados de la '
                f'ciudad \"{city.replace('-', ' ')}\"'
            )
            print(err)
            print(f'La solicitud al servidor se reintentará en {wait_time} segundos')
            time.sleep(wait_time)
            continue

    print(
        f'Tras un total de {retries} intentos, no se pudieron recuperar los datos de los anuncios de la página {page} de resultados de '
        f'la ciudad \"{city.replace('-', ' ')}\"'
    )
    sys.exit('Saliendo del programa...')



def crawler(delay: int, city_start: str) -> Generator[Dict[str, Any]]:
    """Se rastrean todos los inmuebles a la venta de un conjunto de ciudades del portal inmobiliario fotocasa

    Argumentos:
        delay: int -> Tiempo en segundos entre solicitudes HTTP
        city_start: str -> Ciudad a partir de la cual se desea empezar a scrapear. Ideal en caso de errores
        para relanzar el código en el mismo punto en el que se quedó la última instancia del programa
    
    Genera:
        Generator[str, str, Dict[str, Any]] -> Tupla con el nombre de la ciudad que se recorre, el número de la
        página de anuncios, y la respuesta en formato JSON del servidor
    """
    endpoint: str = "https://web.gw.fotocasa.es/v1/search/ads"

    with os.scandir("../payloads/") as payloads:  # Rutas de los payloads
        payloads_paths: List[str] = [f'../payloads/{payload.name}' for payload in payloads]

    cities: List[str] = [payload_path.split('/')[2].replace('.json', '') for payload_path in payloads_paths]
    start: bool = False

    for payload_path, city in zip(payloads_paths, cities):
        if not start:  # El scraping comienza a partir de la ciudad city_start
            if city != city_start:
                continue
            else:
                start = True 
            
        with open(payload_path) as j:  # Se carga un payload en un diccionario
            payload: Dict[str, Any] = json.load(j)

        headers: Dict[str, str] = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Accept-Language": "es-ES,es;q=0.8",
            "Origin": "https://www.fotocasa.es",
            "Referer": "https://www.fotocasa.es/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
            "Sec-Ch-Ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Brave";v="146"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
        }

        total_pages: int = get_total_pages(endpoint, payload, headers, delay, city)  # Total de páginas de anuncios
        
        for page in range(1, total_pages + 1):  # Se itera sobre todas las páginas de anuncios de una ciudad
            yield city, page, fetch_page(endpoint, payload, headers, city, page, delay)
        print('\n\n\n\n')