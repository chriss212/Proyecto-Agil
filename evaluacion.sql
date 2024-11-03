-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS evaluaciones;

-- Usar la base de datos
USE evaluaciones;

-- Crear la tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    nombre_usuario VARCHAR(255) PRIMARY KEY,
    contrasena VARCHAR(255) NOT NULL,
    rol ENUM('gerente', 'empleado') NOT NULL
);

-- Ejemplo de inserción de usuarios
INSERT INTO usuarios (nombre_usuario, contrasena, rol) VALUES 
('gerente1', 'contrasena_segura', 'gerente'),
('empleado1', 'contrasena_segura', 'empleado'),
('empleado2', 'contrasena_segura', 'empleado');

-- Asegurarse de que los datos se han insertado correctamente
SELECT * FROM usuarios;
