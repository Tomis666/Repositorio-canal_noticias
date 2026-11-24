USE canal_noticias;

INSERT INTO roles (nombre, permisos) VALUES
    ('Administrador', 'ALL'),
    ('Editor', 'EDICION'),
    ('Lector', 'LECTURA');

INSERT INTO usuarios (nombre, correo, contrasena, id_rol) VALUES
    ('Administrador del Canal', 'admin@canal.cl',  '03316f8e1dcc6469f0e587b2afe69fba$68392410fa6c66dfd140b2b2ff0d50ff43eeeb58cf7c8fce2e35df65a448244f', 1),
    ('Ignacio',          'ignac@canal.cl', '22782ae9a3816430b5579e5a8b477edd$e23cbe76e7907c62bcfd003511dfdd02a9f6a7cc53fea13f8e507cf0da595863',  2),
    ('Renato',               'ren@gmail.com',    '27c1959bd1f3478706a07e5b2f1886b6$1e0ff6a6b06c3be36266eef25db3c5208c6cbb5d2870a14f0be5410cdb214749', 3),
    ('Juan Pérez',              'juan.perez@hotmail.com', '92021fbda5c7cb5585bc6b7b7d852c1b$dc8755dd15086f6c23d8506a945a796b8f45ef41f6cb7fc1601ca0dbd7c75dbb', 3);

INSERT INTO autores (biografia, id_usuario) VALUES
    ('Reportero de investigación con 10 años de experiencia.', 2);

INSERT INTO categorias (nombre) VALUES ('Política Nacional'), ('Deportes'), ('Economía'), ('Cultura');

INSERT INTO etiquetas (nombre) VALUES ('Última hora'), ('Congreso'), ('Fútbol'), ('Mundial');

INSERT INTO estados_articulo (estado) VALUES ('Borrador'), ('Publicado'), ('Archivado');

INSERT INTO articulos (titulo, contenido, fecha_publicacion, id_autor, id_categoria, id_estado) VALUES
    ('Protesta masiva en Temucó',
     'Ya saslio el GTA6',
     CURDATE(), 1, 1, 2),
    ('La Roja clasifica al mundial después de más de una década de espera',
     'La selección logró el cupo en un partido que se definió en los minutos finales...',
     CURDATE(), 1, 2, 2),
    ('Nuevo informe económico proyecta crecimiento para el próximo año',
     'Borrador pendiente de revisión editorial...',
     CURDATE(), 1, 3, 1);

INSERT INTO articulos_etiquetas (id_articulo, id_etiqueta) VALUES (1, 1), (1, 2), (2, 1), (2, 3), (2, 4);

INSERT INTO lectores (id_usuario) VALUES (3), (4);

INSERT INTO planes (nombre, precio, duracion_dias) VALUES
    ('Gratuito', 0,      3650),
    ('Mensual',  4990,   30),
    ('Anual',    49990,  365);

INSERT INTO suscripciones (id_lector, id_plan, fecha_inicio, fecha_fin, estado) VALUES
    (1, 2, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 30 DAY), 'ACTIVA');

INSERT INTO comentarios (id_lector, id_articulo, fecha, contenido) VALUES
    (1, 1, CURDATE(), 'Por fin una buena noticia para el país.');

INSERT INTO likes (id_lector, id_articulo, fecha) VALUES (1, 1, CURDATE()), (2, 2, CURDATE());
