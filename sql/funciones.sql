---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------
-----------------------------------Definición de las funciones del esquema-------------------------------
---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------
BEGIN WORK;

DROP FUNCTION IF EXISTS fotocasa.insert_to_inmuebles(
    VARCHAR(20),
	VARCHAR(30),
	TEXT,
	TEXT,
	INT,
	INT,
	INT,
	TEXT[],
	VARCHAR(30),
    VARCHAR(30),
	TEXT,
	VARCHAR(10),
	NUMERIC,
	NUMERIC,
	TEXT
);
CREATE OR REPLACE FUNCTION fotocasa.insert_to_inmuebles(
	p_id_fotocasa VARCHAR(20),
	p_tipo_inmueble VARCHAR(30),
	p_descripcion TEXT,
	p_inmobiliaria TEXT,
	p_superficie INT,
	p_habitaciones INT,
	p_baños INT,
	p_extra TEXT[],
	p_ciudad VARCHAR(30),
	p_zona_de_la_ciudad VARCHAR(30),
	p_calle TEXT,
	p_código_postal VARCHAR(10),
	p_latitud NUMERIC,
	p_longitud NUMERIC,
	p_url TEXT
)
RETURNS INT
LANGUAGE sql AS $$ 
    WITH inserted AS (
        INSERT INTO fotocasa.inmuebles (
            clave_inmueble,
            id_fotocasa,
            tipo_inmueble,
            descripcion,
            inmobiliaria,
            superficie,
            habitaciones,
            baños,
            extra,
            ciudad,
            zona_de_la_ciudad,
            calle,
            código_postal,
            latitud,
            longitud,
            url
        )
        VALUES (
            DEFAULT, 
            p_id_fotocasa, 
            p_tipo_inmueble, 
            p_descripcion, 
            p_inmobiliaria, 
            p_superficie, 
            p_habitaciones, 
            p_baños, 
            p_extra, 
            p_ciudad, 
            p_zona_de_la_ciudad, 
            p_calle, 
            p_código_postal,
            p_latitud,
            p_longitud,
            p_url
        )
        ON CONFLICT ON CONSTRAINT u1_inmuebles DO NOTHING
        RETURNING clave_inmueble
    )
    SELECT clave_inmueble FROM inserted
    UNION
    SELECT clave_inmueble FROM fotocasa.inmuebles WHERE id_fotocasa = p_id_fotocasa;
$$;


DROP FUNCTION IF EXISTS fotocasa.insert_to_historico(
    INT,
    INT
);
CREATE OR REPLACE FUNCTION fotocasa.insert_to_historico(
	p_clave_inmueble INT,
    p_precio INT
)
RETURNS void
LANGUAGE sql AS $$ 
    INSERT INTO fotocasa.historico (
        clave_instante,
        clave_inmueble,
        precio,
        fecha
    )
    VALUES (
        DEFAULT,
        p_clave_inmueble,
        p_precio,
        CURRENT_DATE 
    )
    ON CONFLICT ON CONSTRAINT u_historico DO NOTHING;
$$;

COMMIT WORK;
---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------