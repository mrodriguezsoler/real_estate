import psycopg2
from ad import Ad


def upload_to_database(ad: Ad) -> None:
    """Sube y almacena un anuncio en la base de datos fotocasa de PostgreSQL
    Argumentos:
        ad: Ad -> Datos de un anuncio de fotocasa como instancia de la clase Ad
    
    Devuelve:
        None
    """
    # Se establece una conexión con la base de datos
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Hby5XJ7#YG55^cd",
        host="localhost",
        port="5432"
    )

    try:
        with conn:
            with conn.cursor() as cursor:
                # Se definen las consultas a realizar
                insert_inmuebles_query: str = """
                    SELECT * FROM fotocasa.insert_to_inmuebles(
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    );
                """
                insert_historico_query: str = "SELECT * FROM fotocasa.insert_to_historico(%s, %s);"

                # Se ejecuta la función SQL fotocasa.insert_to_inmuebles()
                cursor.execute(insert_inmuebles_query, (
                    ad.id,
                    ad.property_type,
                    ad.description,
                    ad.agency,
                    ad.surface,
                    ad.rooms,
                    ad.baths,
                    ad.extra_features,
                    ad.city,
                    ad.city_zone,
                    ad.street,
                    ad.zip_code,
                    ad.latitude,
                    ad.longitude,
                    ad.url
                ))
                ad_key: int = cursor.fetchone()[0]
                if ad_key is None:
                    print(f'\n[AVISO] No se devolvió la clave del inmueble con ID de fotocasa \"{ad.id}\"')
                    return

                # Se ejecuta la función SQL fotocasa.insert_to_historico()
                cursor.execute(insert_historico_query, (
                    ad_key, ad.price
                ))

    except Exception as err:
        conn.rollback()
        raise RuntimeError(
            f'\n[ERROR] Ocurrió un error inesperado al insertar el inmueble con ID de fotocasa \"{ad.id}\" en la base de datos'
        ) from err

    finally:
        conn.close()