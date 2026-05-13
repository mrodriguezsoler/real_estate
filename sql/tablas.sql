---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------
----------------------------------Definición de las tablas del esquema-----------------------------------
---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------
BEGIN WORK;

DROP TABLE IF EXISTS fotocasa.inmuebles CASCADE;
CREATE TABLE fotocasa.inmuebles (
	clave_inmueble SERIAL,
	id_fotocasa VARCHAR(20) NOT NULL,
	tipo_inmueble VARCHAR(30),
	descripcion TEXT,
	inmobiliaria TEXT,
	superficie INT,
	habitaciones INT,
	baños INT,
	extra TEXT[],
	ciudad VARCHAR(45),
	zona_de_la_ciudad TEXT,
	calle TEXT,
	código_postal VARCHAR(10),
	latitud NUMERIC,
	longitud NUMERIC,
	url TEXT,
	CONSTRAINT pk_inmuebles PRIMARY KEY (clave_inmueble),
	CONSTRAINT u1_inmuebles UNIQUE (id_fotocasa)
);

DROP TABLE IF EXISTS fotocasa.historico CASCADE;
CREATE TABLE fotocasa.historico (
	clave_instante SERIAL,
	clave_inmueble INT NOT NULL,
	precio INT,
	fecha DATE NOT NULL, 
	CONSTRAINT pk_historico PRIMARY KEY (clave_instante),
	CONSTRAINT u_historico UNIQUE (clave_inmueble, fecha),
	CONSTRAINT fk_historico_inmuebles FOREIGN KEY (clave_inmueble) REFERENCES fotocasa.inmuebles(clave_inmueble)
);

COMMIT WORK;
---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------