CREATE TABLE diametros_tubos(id_sistema VARCHAR, seccion_fase_mm2 DOUBLE, diametro_minimo_mm DOUBLE);;
CREATE TABLE intensidades_subterraneas(id_sistema VARCHAR, seccion_mm2 DOUBLE, material VARCHAR, aislamiento VARCHAR, intensidad_A DOUBLE);;
CREATE TABLE secciones_neutro(seccion_fase_mm2 DOUBLE PRIMARY KEY, seccion_neutro_mm2 DOUBLE);;

