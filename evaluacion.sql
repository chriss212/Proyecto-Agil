CREATE DATABASE evaluaciones;

USE evaluaciones;

CREATE TABLE evaluaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_empleado VARCHAR(100),
    rol VARCHAR(100),
    criterios TEXT,
    autoevaluacion JSON,
    evaluacion_gerente JSON,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    rol ENUM('gerente', 'empleado') NOT NULL
);

INSERT INTO usuarios (nombre_usuario, contrasena, rol) VALUES ('gerente', 'gerente123', 'gerente');
INSERT INTO usuarios (nombre_usuario, contrasena, rol) VALUES ('empleado', 'empleado123', 'empleado');



CREATE TABLE evaluaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_empleado VARCHAR(100) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    autoevaluacion TEXT,
    evaluacion_gerente TEXT
);


CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    rol ENUM('gerente', 'empleado') NOT NULL
);


INSERT INTO usuarios (nombre_usuario, contrasena, rol) VALUES
('gerente1', 'contrasena123', 'gerente'),
('empleado1', 'contrasena456', 'empleado'),
('empleado2', 'contrasena789', 'empleado'),
('empleado3', 'contrasena321', 'empleado'),
('empleado4', 'contrasena654', 'empleado');