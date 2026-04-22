COPY diametros_tubos FROM 'backup_normativas/diametros_tubos.csv' (FORMAT 'csv', HEADER 1, delimiter ',', quote '"');
COPY intensidades_subterraneas FROM 'backup_normativas/intensidades_subterraneas.csv' (FORMAT 'csv', HEADER 1, delimiter ',', quote '"');
COPY secciones_neutro FROM 'backup_normativas/secciones_neutro.csv' (FORMAT 'csv', HEADER 1, delimiter ',', quote '"', force_not_null 'seccion_fase_mm2');
