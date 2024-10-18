-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         11.4.2-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para evaluaciones
CREATE DATABASE IF NOT EXISTS `evaluaciones` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `evaluaciones`;

-- Volcando estructura para tabla evaluaciones.evaluaciones
CREATE TABLE IF NOT EXISTS `evaluaciones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_empleado` varchar(100) NOT NULL,
  `rol` varchar(50) NOT NULL,
  `autoevaluacion` text DEFAULT NULL,
  `evaluacion_gerente` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla evaluaciones.evaluaciones: ~2 rows (aproximadamente)
DELETE FROM `evaluaciones`;
INSERT INTO `evaluaciones` (`id`, `nombre_empleado`, `rol`, `autoevaluacion`, `evaluacion_gerente`) VALUES
	(1, 'Alexis', 'Empleado', '[5, 5, 3, 5, 5, 3, 3, 4, 5, 3, 3, 5, 5, 5, 5]', '[5, 5, 5, 5, 5]'),
	(2, 'Ximena', 'Empleado', '[3, 3, 4, 5, 1, 2, 3, 3, 4, 5, 1, 5, 5, 5, 5]', '[3, 4, 5, 2, 4]');

-- Volcando estructura para tabla evaluaciones.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_usuario` varchar(100) NOT NULL,
  `contrasena` varchar(100) NOT NULL,
  `rol` enum('gerente','empleado') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre_usuario` (`nombre_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla evaluaciones.usuarios: ~5 rows (aproximadamente)
DELETE FROM `usuarios`;
INSERT INTO `usuarios` (`id`, `nombre_usuario`, `contrasena`, `rol`) VALUES
	(1, 'gerente1', 'contrasena123', 'gerente'),
	(2, 'empleado1', 'contrasena456', 'empleado'),
	(3, 'empleado2', 'contrasena789', 'empleado'),
	(4, 'empleado3', 'contrasena321', 'empleado'),
	(5, 'empleado4', 'contrasena654', 'empleado');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
