
CREATE DATABASE IF NOT EXISTS canal_noticias
    CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE canal_noticias;

CREATE TABLE roles (
    id_rol      INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(50)  NOT NULL,
    permisos    VARCHAR(255) NOT NULL,
    habilitado  TINYINT      NOT NULL DEFAULT 1,
    CONSTRAINT uq_roles_nombre UNIQUE (nombre)
) ENGINE=InnoDB;

CREATE TABLE categorias (
    id_categoria  INT AUTO_INCREMENT PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL,
    habilitado    TINYINT      NOT NULL DEFAULT 1,
    CONSTRAINT uq_categorias_nombre UNIQUE (nombre)
) ENGINE=InnoDB;

CREATE TABLE etiquetas (
    id_etiqueta  INT AUTO_INCREMENT PRIMARY KEY,
    nombre       VARCHAR(50)  NOT NULL,
    habilitado   TINYINT      NOT NULL DEFAULT 1,
    CONSTRAINT uq_etiquetas_nombre UNIQUE (nombre)
) ENGINE=InnoDB;

CREATE TABLE estados_articulo (
    id_estado   INT AUTO_INCREMENT PRIMARY KEY,
    estado      VARCHAR(30)  NOT NULL,
    CONSTRAINT uq_estados_articulo UNIQUE (estado)
) ENGINE=InnoDB;

CREATE TABLE planes (
    id_plan        INT AUTO_INCREMENT PRIMARY KEY,
    nombre         VARCHAR(50)    NOT NULL,
    precio         DECIMAL(10,2)  NOT NULL,
    duracion_dias  INT            NOT NULL,
    habilitado     TINYINT        NOT NULL DEFAULT 1,
    CONSTRAINT ck_planes_precio    CHECK (precio >= 0),
    CONSTRAINT ck_planes_duracion  CHECK (duracion_dias >= 1)
) ENGINE=InnoDB;



CREATE TABLE usuarios (
    id_usuario  INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    correo      VARCHAR(100) NOT NULL,
    contrasena  VARCHAR(255) NOT NULL,         
    id_rol      INT          NOT NULL,
    habilitado  TINYINT      NOT NULL DEFAULT 1,
    CONSTRAINT uq_usuarios_correo UNIQUE (correo),
    CONSTRAINT fk_usuarios_rol FOREIGN KEY (id_rol) REFERENCES roles (id_rol)
) ENGINE=InnoDB;

CREATE TABLE autores (
    id_autor    INT AUTO_INCREMENT PRIMARY KEY,
    biografia   TEXT         NULL,
    id_usuario  INT          NOT NULL,
    habilitado  TINYINT      NOT NULL DEFAULT 1,
    CONSTRAINT uq_autores_usuario UNIQUE (id_usuario),     
    CONSTRAINT fk_autores_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario)
) ENGINE=InnoDB;

CREATE TABLE lectores (
    id_lector   INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario  INT          NOT NULL,
    habilitado  TINYINT      NOT NULL DEFAULT 1,
    CONSTRAINT uq_lectores_usuario UNIQUE (id_usuario),    
    CONSTRAINT fk_lectores_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario)
) ENGINE=InnoDB;


CREATE TABLE articulos (
    id_articulo        INT AUTO_INCREMENT PRIMARY KEY,
    titulo             VARCHAR(150) NOT NULL,
    contenido          TEXT         NOT NULL,
    fecha_publicacion  DATE         NOT NULL,
    id_autor           INT          NOT NULL,
    id_categoria       INT          NOT NULL,
    id_estado          INT          NOT NULL,
    habilitado         TINYINT      NOT NULL DEFAULT 1,
    CONSTRAINT fk_articulos_autor     FOREIGN KEY (id_autor)     REFERENCES autores (id_autor),
    CONSTRAINT fk_articulos_categoria FOREIGN KEY (id_categoria) REFERENCES categorias (id_categoria),
    CONSTRAINT fk_articulos_estado    FOREIGN KEY (id_estado)    REFERENCES estados_articulo (id_estado),
    INDEX idx_articulos_listado (habilitado, fecha_publicacion)   -- acelera el listado principal
) ENGINE=InnoDB;


CREATE TABLE articulos_etiquetas (
    id_articulo  INT NOT NULL,
    id_etiqueta  INT NOT NULL,
    PRIMARY KEY (id_articulo, id_etiqueta),
    CONSTRAINT fk_ae_articulo FOREIGN KEY (id_articulo) REFERENCES articulos (id_articulo) ON DELETE CASCADE,
    CONSTRAINT fk_ae_etiqueta FOREIGN KEY (id_etiqueta) REFERENCES etiquetas (id_etiqueta)
) ENGINE=InnoDB;

#Suscripciones 
CREATE TABLE suscripciones (
    id_suscripcion  INT AUTO_INCREMENT PRIMARY KEY,
    id_lector       INT  NOT NULL,
    id_plan         INT  NOT NULL,
    fecha_inicio    DATE NOT NULL,
    fecha_fin       DATE NOT NULL,
    estado          ENUM('ACTIVA','VENCIDA','CANCELADA') NOT NULL DEFAULT 'ACTIVA',
    CONSTRAINT fk_susc_lector FOREIGN KEY (id_lector) REFERENCES lectores (id_lector),
    CONSTRAINT fk_susc_plan   FOREIGN KEY (id_plan)   REFERENCES planes (id_plan),
    INDEX idx_susc_lector_estado (id_lector, estado)
) ENGINE=InnoDB;

#Interacciones 
CREATE TABLE comentarios (
    id_comentario  INT AUTO_INCREMENT PRIMARY KEY,
    id_lector      INT     NOT NULL,
    id_articulo    INT     NOT NULL,
    fecha          DATE    NOT NULL,
    contenido      TEXT    NOT NULL,
    habilitado     TINYINT NOT NULL DEFAULT 1,
    CONSTRAINT fk_com_lector   FOREIGN KEY (id_lector)   REFERENCES lectores (id_lector),
    CONSTRAINT fk_com_articulo FOREIGN KEY (id_articulo) REFERENCES articulos (id_articulo),
    INDEX idx_com_articulo (id_articulo)
) ENGINE=InnoDB;

CREATE TABLE likes (
    id_like      INT AUTO_INCREMENT PRIMARY KEY,
    id_lector    INT  NOT NULL,
    id_articulo  INT  NOT NULL,
    fecha        DATE NOT NULL,
    CONSTRAINT uq_likes_lector_articulo UNIQUE (id_lector, id_articulo), 
    CONSTRAINT fk_like_lector   FOREIGN KEY (id_lector)   REFERENCES lectores (id_lector),
    CONSTRAINT fk_like_articulo FOREIGN KEY (id_articulo) REFERENCES articulos (id_articulo)
) ENGINE=InnoDB;
