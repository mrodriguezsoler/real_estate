import json
from ad import Ad
from typing import Optional, Tuple, Dict, List


def load_json(feature_map_path: str, property_type_map_path: str) -> Tuple[dict]:
    """Se abren dos archivos JSON y se almacenan en un diccionario: el de las correspondencias
    entre las IDs y sus características, y el de las IDs y los tipos de propiedades.

    Argumentos:
        feature_map_path: str -> Ruta del JSON de las características
        property_type_path: str -> Ruta del JSON de los tipos de inmuebles
    
    Devuelve:
        Tuple[dict] -> Tupla con los dos diccionarios
    """    
    with open(feature_map_path, 'r', encoding='utf-8') as f:  # JSON de las características
        feature_map: Dict[str, str] = json.load(f)

    with open(property_type_map_path, 'r', encoding='utf-8') as f:  # JSON de los tipos de propiedades
        property_type_map: Dict[str, str] = json.load(f)
    
    return feature_map, property_type_map



def safe_get(dictionary: dict, path: List[str], default=None) -> str | int | None:
    """Se accede de forma segura a los elementos anidados de un diccionario
    Argumentos:
        dictionary: dict -> Estructura de la que se quieren recuperar datos
        path: List[str] -> Ruta de elementos a seguir para llegar al dato objetivo
        default: Optional[str] -> Valor por defecto que se devuelve al no encontrar coincidencias
    
    Devuelve:
        dictionary | default -> Dato objetivo o valor por defecto al no haber coincidencias
    """
    for key in path:
        if isinstance(dictionary, dict):
            dictionary = dictionary.get(key)
        else:
            return default
        if dictionary is None:
            return default
    return dictionary



def extract_data(ad: dict, feature_map: dict, property_type_map: dict) -> Ad:
    """Se extrae la información relevante de cada anuncio y se almacena en un diccionario. Entre
    estos datos, se recolecta el identificador del inmueble de fotocasa, el tipo de propiedad, la
    descripción del inmueble por parte del vendedor, la inmobiliaria propietaria de la vivienda,
    el precio de venta actual, la superficie, el número de habitaciones, el total de baños,
    características adicionales del inmueble (como si tiene parking, trastero, ascensor, balcón,
    piscina, terraza...), la ciudad y la zona en la que se encuentra la propiedad, la calle de la
    vivienda, el código postal, las coordenadas exactas del inmueble en forma de latitud y longitud,
    y la URL del anuncio.

    Argumentos:
        ad: dict -> Diccionario del anuncio que se intercepta del backend de fotocasa
        feature_map: dict -> Diccionario de características adicionales de una vivienda
        property_type_map: dict -> Diccionario de tipos de propiedades
    
    Devuelve:
        Ad -> Instancia de la clase Ad con los datos del anuncio
    
    """
    property_subtype_id: Optional[str] = ad.get('propertySubtype')

    features: Optional[List[Dict[str, str]]] = ad.get('features', [])
    extra_features_ids: Optional[List[str]] = [f.get('id') for f in features if f.get('id') is not None]
    extra_features: Optional[List[str]] = [feature_map.get(fid) for fid in extra_features_ids if fid in feature_map.keys()]

    latitude: Optional[float] = float(safe_get(ad, ['location', 'latitude'])) if safe_get(ad, ['location', 'latitude']) is not None else None
    longitude: Optional[float] = float(safe_get(ad, ['location', 'longitude'])) if safe_get(ad, ['location', 'longitude']) is not None else None

    ad_url = None
    for language in ad.get('uris', []):
        if language.get('language') == 'es_ES':
            ad_url = language.get('value')
            break

    return Ad(
        id=ad.get('id'),
        property_type=property_type_map.get(property_subtype_id),
        description=ad.get('description'),
        agency=safe_get(ad, ['agency', 'name']),
        price=safe_get(ad, ['transaction', 'price']),

        surface=ad.get('surface'),
        rooms=ad.get('rooms'),
        baths=ad.get('baths'),
        extra_features=sorted(extra_features) if extra_features else None,

        city=safe_get(ad, ['location', 'level5Name']),
        city_zone=safe_get(ad, ['location', 'level7Name']),
        street=ad.get('street'),
        zip_code=ad.get('zipCode'),
        latitude=latitude,
        longitude=longitude,

        url=ad_url
    )