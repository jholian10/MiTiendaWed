-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 01-07-2026 a las 06:27:46
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `mitiendaweb_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carritos`
--

CREATE TABLE `carritos` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `actualizado_el` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `carritos`
--

INSERT INTO `carritos` (`id`, `usuario_id`, `actualizado_el`) VALUES
(6, 20, '2026-06-23 04:54:10'),
(14, 27, '2026-06-25 07:11:05'),
(21, 29, '2026-06-30 06:27:02'),
(23, 1, '2026-07-01 03:03:21'),
(25, 30, '2026-07-01 03:41:05'),
(26, 31, '2026-07-01 04:04:01');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito_detalles`
--

CREATE TABLE `carrito_detalles` (
  `id` int(11) NOT NULL,
  `carrito_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL DEFAULT 1,
  `agregado_el` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `carrito_detalles`
--

INSERT INTO `carrito_detalles` (`id`, `carrito_id`, `producto_id`, `cantidad`, `agregado_el`) VALUES
(4, 14, 4, 3, '2026-06-25 07:17:21');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `direcciones_usuario`
--

CREATE TABLE `direcciones_usuario` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `departamento` varchar(100) NOT NULL,
  `ciudad` varchar(100) NOT NULL,
  `direccion_detallada` varchar(255) NOT NULL,
  `barrio` varchar(100) DEFAULT NULL,
  `telefono_contacto` varchar(20) DEFAULT NULL,
  `es_principal` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `direcciones_usuario`
--

INSERT INTO `direcciones_usuario` (`id`, `usuario_id`, `departamento`, `ciudad`, `direccion_detallada`, `barrio`, `telefono_contacto`, `es_principal`) VALUES
(39, 29, 'Atlántico', 'Candelaria', 'calle 19 A', 'samiguel', 'N/A', 1),
(40, 1, 'Cundinamarca', 'Cajicá', 'calle 19 A', 'kjlñ', 'N/A', 1),
(41, 30, 'Atlántico', 'Candelaria', '21 A', 'samiguel', 'N/A', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `favoritos`
--

CREATE TABLE `favoritos` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `agregado_el` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `favoritos`
--

INSERT INTO `favoritos` (`id`, `usuario_id`, `producto_id`, `agregado_el`) VALUES
(15, 29, 4, '2026-06-30 06:02:56'),
(17, 29, 2, '2026-06-30 06:03:10'),
(18, 29, 3, '2026-06-30 06:03:21');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notificaciones`
--

CREATE TABLE `notificaciones` (
  `id` int(11) NOT NULL,
  `mensaje` text NOT NULL,
  `leido` tinyint(1) DEFAULT 0,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `notificaciones`
--

INSERT INTO `notificaciones` (`id`, `mensaje`, `leido`, `fecha_creacion`) VALUES
(1, 'Producto registrado: 45y', 0, '2026-06-23 01:21:31'),
(2, '¡Producto Actualizado! El administrador modificó los datos de \"45y\".', 0, '2026-06-23 02:27:02'),
(3, '¡Producto Actualizado! El administrador modificó los datos de \"45y\".', 0, '2026-06-23 02:27:18'),
(4, '¡Producto Eliminado! El administrador removió \"Bolso Artesanal Grande\" del sistema.', 0, '2026-06-23 02:28:42'),
(5, '¡AGOTADO!: El producto \"45y\" se ha quedado sin existencias.', 0, '2026-06-23 02:29:14'),
(6, '¡Alerta de Inventario! El producto \"45y\" fue modificado y se ha quedado AGOTADO (0 unidades).', 0, '2026-06-23 02:29:15'),
(7, '¡AGOTADO!: El producto \"Cartera Crochet Elegante\" se ha quedado sin existencias.', 0, '2026-06-23 05:05:43'),
(8, '¡AGOTADO!: El producto \"Cartera Tejida Pequeña\" se ha quedado sin existencias.', 0, '2026-06-23 06:01:37'),
(9, '¡Alerta de Inventario! El producto \"Cartera Tejida Pequeña\" fue modificado y se ha quedado AGOTADO (0 unidades).', 0, '2026-06-23 06:01:40'),
(10, 'Producto registrado: ui', 0, '2026-06-23 06:05:27'),
(11, '¡Producto Actualizado! El administrador modificó los datos de \"Bolso Tipo Saco Artesanal\".', 0, '2026-06-23 06:05:37'),
(12, '¡Producto Actualizado! El administrador modificó los datos de \"Bolso Tipo Saco Artesanal\".', 0, '2026-06-23 06:06:00'),
(13, '¡Producto Actualizado! El administrador modificó los datos de \"Bolso Artesanal con Flecos\".', 0, '2026-06-23 06:06:16');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `referencia` varchar(100) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `estado` enum('PENDIENTE','PAGADO','EMPACANDO','EN_TRANSITO','ENTREGADO') DEFAULT 'PENDIENTE',
  `direccion_envio` varchar(255) NOT NULL,
  `ciudad_envio` varchar(100) NOT NULL,
  `telefono_contacto` varchar(20) NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedidos`
--

INSERT INTO `pedidos` (`id`, `usuario_id`, `referencia`, `total`, `estado`, `direccion_envio`, `ciudad_envio`, `telefono_contacto`, `fecha_creacion`) VALUES
(1, 1, 'ORD_1_1782186663150', 105000.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-23 03:51:03'),
(2, 1, 'ORD_1_1782186949884', 105000.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-23 03:55:49'),
(3, 1, 'ORD_1_1782188411693', 105000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-06-23 04:20:11'),
(4, 1, 'ORD_1_1782188813507', 105000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-06-23 04:26:53'),
(5, 1, 'ORD_1_1782189234740', 190000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-06-23 04:33:54'),
(6, 1, 'PRUEBA_123', 0.00, 'PENDIENTE', '', '', '', '2026-06-23 04:43:14'),
(7, 1, 'ORD_1_1782190043317', 190000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-06-23 04:47:23'),
(8, 20, 'ORD_20_1782190369135', 210000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-06-23 04:52:49'),
(9, 1, 'ORD_1_1782363286564', 380000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 04:54:46'),
(10, 1, 'ORD_1_1782363813794', 380000.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 05:03:33'),
(11, 1, 'ORD_1_1782363840420', 105000.02, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 05:04:00'),
(12, 1, 'ORD_1_1782364064442', 105000.02, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 05:07:44'),
(13, 1, 'ORD_1_1782364125886', 105000.02, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 05:08:45'),
(14, 1, 'ORD_1_1782364153699', 105000.02, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 05:09:13'),
(15, 1, 'ORD_1_1782364260181', 105000.02, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 05:11:00'),
(16, 1, 'ORD_1_1782364272879', 105000.02, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 05:11:12'),
(17, 1, 'ORD_1_1782364795536', 105000.02, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 05:19:55'),
(18, 27, 'ORD_27_1782365037916', 85000.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 05:23:57'),
(19, 1, 'ORD_1_1782365241331', 0.02, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 05:27:21'),
(20, 27, 'ORD_27_1782365275449', 85000.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 05:27:55'),
(21, 27, 'ORD_27_1782365454209', 85000.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 05:30:54'),
(22, 27, 'ORD_27_1782365457592', 85000.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 05:30:57'),
(23, 27, 'ORD_27_1782365510252', 85000.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 05:31:50'),
(24, 27, 'ORD_27_1782365798573', 85000.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 05:36:38'),
(25, 27, 'ORD_27_1782366029680', 85000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 05:40:29'),
(26, 27, 'ORD_27_1782366439063', 105000.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 05:47:19'),
(27, 27, 'ORD_27_1782366484603', 105000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 05:48:04'),
(28, 27, 'ORD_27_1782370996623', 85000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 07:03:16'),
(29, 27, 'ORD_27_1782371208916', 105000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 07:06:48'),
(30, 27, 'ORD_27_1782371421257', 105000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-06-25 07:10:21'),
(31, 1, 'ORD_1_1782796061810', 200000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-06-30 05:07:41'),
(32, 29, 'ORD_29_1782796399683', 89000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-06-30 05:13:19'),
(33, 29, 'ORD_29_1782797121619', 89000.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-30 05:25:21'),
(34, 29, 'ORD_29_1782797138066', 89000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-06-30 05:25:38'),
(35, 29, 'ORD_29_1782797575906', 170000.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-30 05:32:55'),
(36, 29, 'ORD_29_1782797627374', 85000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-06-30 05:33:47'),
(37, 29, 'ORD_29_1782797744728', 85000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-06-30 05:35:44'),
(38, 29, 'ORD_29_1782798175413', 85000.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-30 05:42:55'),
(39, 29, 'ORD_29_1782798200328', 85000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-06-30 05:43:20'),
(40, 29, 'ORD_29_1782798867057', 85000.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-30 05:54:27'),
(41, 29, 'ORD_29_1782798871526', 85000.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-30 05:54:31'),
(42, 29, 'ORD_29_1782798895680', 170000.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-30 05:54:55'),
(43, 29, 'ORD_29_1782800302997', 315000.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-30 06:18:23'),
(44, 29, 'ORD_29_1782800793311', 735000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-06-30 06:26:33'),
(45, 1, 'ORD_1_1782874960282', 190000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-07-01 03:02:40'),
(46, 1, 'ORD_1_1782875653074', 89000.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-07-01 03:14:13'),
(47, 30, 'ORD_30_1782877185636', 85000.00, 'EMPACANDO', 'No especificada', 'No especificada', 'No especificado', '2026-07-01 03:39:45');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedido_detalles`
--

CREATE TABLE `pedido_detalles` (
  `id` int(11) NOT NULL,
  `pedido_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedido_detalles`
--

INSERT INTO `pedido_detalles` (`id`, `pedido_id`, `producto_id`, `cantidad`, `precio_unitario`) VALUES
(1, 28, 1, 1, 85000.00),
(2, 29, 4, 1, 105000.00),
(3, 30, 4, 1, 105000.00),
(4, 32, 7, 1, 89000.00),
(5, 34, 7, 1, 89000.00),
(6, 36, 1, 1, 85000.00),
(7, 37, 1, 1, 85000.00),
(8, 31, 2, 1, 95000.00),
(9, 31, 7, 1, 89000.00),
(11, 39, 3, 1, 85000.00),
(12, 44, 4, 7, 105000.00),
(13, 45, 2, 2, 95000.00),
(14, 47, 3, 1, 85000.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `proveedor_id` int(11) DEFAULT NULL,
  `nombre` varchar(120) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio_compra` decimal(10,2) NOT NULL,
  `precio_venta` decimal(10,2) NOT NULL,
  `stock` int(11) NOT NULL DEFAULT 0,
  `stock_minimo` int(11) NOT NULL DEFAULT 5,
  `imagen_url` longtext DEFAULT NULL,
  `estado` tinyint(1) NOT NULL DEFAULT 1,
  `creado_el` timestamp NOT NULL DEFAULT current_timestamp(),
  `actualizado_el` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `proveedor_id`, `nombre`, `descripcion`, `precio_compra`, `precio_venta`, `stock`, `stock_minimo`, `imagen_url`, `estado`, `creado_el`, `actualizado_el`) VALUES
(1, 1, 'Bolso Artesanal Borgoña', 'Exclusivo bolso tejido a mano color vino con flecos elegantes, broche magnético y apliques de bordado floral artesanal.', 45000.00, 85000.00, 15, 3, 'bolso-borgona.jpg.jpeg', 1, '2026-06-25 06:20:55', '2026-06-25 06:20:55'),
(2, 1, 'Bolso Elegance Dunaka', 'Bolso de hombro premium texturizado en tono rosa pastel, diseñado con hilos de alta calidad y cargaderas de flecos continuos.', 50000.00, 95000.00, 10, 2, 'bolso-elegance.jpg.jpeg', 1, '2026-06-25 06:20:55', '2026-06-25 06:20:55'),
(3, 1, 'Bolso Índigo Artesanal', 'Hermoso bolso artesanal en color azul índigo profundo, con asa tejida reforzada, borla decorativa y detalles florales hechos a mano.', 45000.00, 85000.00, 12, 3, 'bolso-indigo.jpg.jpeg', 1, '2026-06-25 06:20:55', '2026-06-25 06:20:55'),
(4, 1, 'Bolso Verde Oliva', 'Bolso tipo tote amplio elaborado en trapillo tipo pluma ligero, suave y resistente. Ideal para un diseño minimalista y versátil.', 55000.00, 105000.00, 20, 5, 'bolso-verde.jpg.jpeg', 1, '2026-06-25 06:20:55', '2026-06-25 06:20:55'),
(5, 1, 'Cartera Clásica con Flecos', 'Cartera cuadrada estructurada color beige arena con flecos laterales decorativos y asa de mano superior rígida.', 40000.00, 78000.00, 8, 2, 'cartera-clas.jpg.jpeg', 1, '2026-06-25 06:20:55', '2026-06-25 06:20:55'),
(6, 1, 'Cartera Sobre de Mano', 'Cartera de mano estilo sobre compacta tejida en tono crema, con un elegante llavero de borla larga y detalles de perlas.', 30000.00, 55000.00, 25, 4, 'cartera-clasica.jpg.jpeg', 1, '2026-06-25 06:20:55', '2026-06-25 06:20:55'),
(7, 1, 'Morral Urbano Tejido', 'Morral artesanal de diseño contemporáneo y juvenil, cómodo y perfecto para el uso diario sin perder el estilo tradicional.', 48000.00, 89000.00, 7, 2, 'morral-urbano.jpg.jpeg', 1, '2026-06-25 06:20:55', '2026-06-25 06:20:55');

--
-- Disparadores `productos`
--
DELIMITER $$
CREATE TRIGGER `tr_alerta_nuevo_sin_stock` AFTER INSERT ON `productos` FOR EACH ROW BEGIN
    IF NEW.stock = 0 THEN
        INSERT INTO notificaciones (mensaje, leido)
        VALUES (CONCAT('¡Alerta! El nuevo producto "', NEW.nombre, '" se ha registrado sin existencias (0 unidades).'), 0);
    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `tr_alerta_stock_actualizado` AFTER UPDATE ON `productos` FOR EACH ROW BEGIN
    IF NEW.stock = 0 AND OLD.stock > 0 THEN
        INSERT INTO notificaciones (mensaje, leido)
        VALUES (CONCAT('¡AGOTADO!: El producto "', NEW.nombre, '" se ha quedado sin existencias.'), 0);
    ELSEIF NEW.stock <= NEW.stock_minimo AND OLD.stock > NEW.stock_minimo AND NEW.stock > 0 THEN
        INSERT INTO notificaciones (mensaje, leido)
        VALUES (CONCAT('Stock bajo: El producto "', NEW.nombre, '" tiene solo ', NEW.stock, ' unidades.'), 0);
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedor`
--

CREATE TABLE `proveedor` (
  `id_proveedor` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `gmail` varchar(255) NOT NULL,
  `telefono` varchar(50) NOT NULL,
  `creado_el` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proveedor`
--

INSERT INTO `proveedor` (`id_proveedor`, `nombre`, `direccion`, `gmail`, `telefono`, `creado_el`) VALUES
(1, 'df', 'fd', '', '', '2026-06-22 07:04:16');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reportes_venta`
--

CREATE TABLE `reportes_venta` (
  `id` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `monto` decimal(10,2) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reseñas`
--

CREATE TABLE `reseñas` (
  `id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `calificacion` int(11) NOT NULL CHECK (`calificacion` >= 1 and `calificacion` <= 5),
  `comentario` text DEFAULT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `soporte`
--

CREATE TABLE `soporte` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `remitente` varchar(50) NOT NULL DEFAULT 'cliente',
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(150) NOT NULL,
  `asunto` varchar(200) NOT NULL,
  `mensaje` text NOT NULL,
  `estado` enum('pendiente','en_proceso','resuelto') NOT NULL DEFAULT 'pendiente',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `soporte`
--

INSERT INTO `soporte` (`id`, `usuario_id`, `remitente`, `nombre`, `correo`, `asunto`, `mensaje`, `estado`, `fecha_creacion`) VALUES
(1, NULL, 'cliente', '', '', '', 'Hola', 'pendiente', '2026-06-23 01:03:08'),
(2, 1, 'cliente', 'Super Admin Dunaka', 'jholianmanuel10@gmail.com', '', 'hola', 'pendiente', '2026-06-25 04:42:54'),
(3, 1, 'admin', '', '', '', 'wq', 'pendiente', '2026-07-01 04:15:28'),
(4, 31, 'cliente', 'LUCIANA SOFIA', 'lucianasofia2605@gmail.com', '', 'Hola', 'pendiente', '2026-07-01 04:15:45'),
(5, 31, 'cliente', 'LUCIANA SOFIA', 'lucianasofia2605@gmail.com', '', 'Hshhshs', 'pendiente', '2026-07-01 04:15:57'),
(6, 31, 'admin', '', '', '', 'jhggg', 'pendiente', '2026-07-01 04:16:09'),
(7, 31, 'cliente', 'LUCIANA SOFIA', 'lucianasofia2605@gmail.com', '', 'Jdjdrttwtttwyyywyyywhhhwhhwh', 'pendiente', '2026-07-01 04:19:19');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(150) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `rol` enum('superadmin','admin','cliente') NOT NULL DEFAULT 'cliente',
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `creado_el` timestamp NOT NULL DEFAULT current_timestamp(),
  `codigo_recuperacion` varchar(6) DEFAULT NULL,
  `codigo_expira` datetime DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `foto_perfil` varchar(255) DEFAULT 'default.png',
  `foto_perfil_url` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `correo`, `password_hash`, `rol`, `activo`, `creado_el`, `codigo_recuperacion`, `codigo_expira`, `telefono`, `direccion`, `ciudad`, `foto_perfil`, `foto_perfil_url`) VALUES
(1, 'Super Admin Dunaka', 'jholianmanuel10@gmail.com', 'scrypt:32768:8:1$WNyKMyD4qkF1qUg8$ed36fd1ffef116564842723f0ad77fbdc7df31dede2e359386bf1b7f263369518c2f8a05c03070cc53a420605450abaa8aa7a126d5e1979ff3a1569b5f8482e0', 'superadmin', 1, '2026-06-23 00:35:09', '895223', '2026-06-23 01:01:24', '', '', '', 'default.png', '/static/uploads/perfiles/user_1.png'),
(20, 'Yo', 'yo@gmail.com', 'scrypt:32768:8:1$EyhzET7UXarPT5yB$3074060c353a3989acf7b2105d78d1c6bc421ac51378e38d019bcda4213eeaa3f5b486156d22cf7e959373e728bd7cd271f4c2b0ea9ea4d4dcfe390c928941a0', 'cliente', 1, '2026-06-23 04:51:56', NULL, NULL, NULL, NULL, NULL, 'default.png', NULL),
(22, 'Angie Paola Gutiérrez Reales', 'agutierrezreales@gmail.com', 'scrypt:32768:8:1$IkKyXD2mIfCjXrnR$03331f7c4aa53b507df6ef54e30e509a335f99ecfc60169e433e22d1f9dd559e5e8d9299d2a7ffb5c91baf9540ab77485feab496e074e872e00930d1cc3977f2', 'cliente', 1, '2026-06-23 05:09:16', '389608', '2026-06-23 00:23:01', NULL, NULL, NULL, 'default.png', NULL),
(26, 'sapo', 'sapo@gmail.com', 'scrypt:32768:8:1$Zc8QpfQIjJXCgUnv$251eb4f55f2ffd3beb97f2f28e8bca8d4a7a5087585623ad6f8aabf309d201cd11abbe8fbbaf4cb8af44ee51fb7b6b2dac467363fcc3b9f383dac51b3a130d70', 'cliente', 1, '2026-06-23 05:20:43', '423789', '2026-06-23 00:30:56', NULL, NULL, NULL, 'default.png', NULL),
(27, 'ema', 'ema@gmail.com', 'scrypt:32768:8:1$niFUg7VWl59mk0OJ$d5ad28a4295db684e0a12182c54f735e1c5f92b388beecfd5d22d9d924bb478626b7db2ed9c9dc3f9aab543bfb3f3480aca8f4c180a6aae6343c62c06ce94dfa', 'cliente', 1, '2026-06-25 05:23:19', NULL, NULL, NULL, NULL, NULL, 'default.png', NULL),
(29, 'you', 'you@gmail.com', 'scrypt:32768:8:1$6aWjQwp8zm9m2Rdj$ef3297b705a0fabea29458010c1b997f2bbd2edaa4df20c6f03715434bee21c0c01167b097c31f99a5cdf2ee23c1e703bdf7ff740b89d3aaa8b08b67e8278a9f', 'cliente', 1, '2026-06-30 05:12:45', NULL, NULL, NULL, NULL, NULL, 'default.png', NULL),
(30, 'tutu', 'tutu@gmail.com', 'scrypt:32768:8:1$nc72OR3wSc8GxGjk$b96c1764b5ca2ed33d75948ec158a04bbda36ae2b8d6d3330fc87ea4e0f7491abb3f4712f35be0dae59fb3eefcf0efb526335be9d71eb1b9ddc5d6749410cac2', 'cliente', 1, '2026-07-01 03:38:26', NULL, NULL, NULL, NULL, NULL, 'default.png', NULL),
(31, 'LUCIANA SOFIA', 'lucianasofia2605@gmail.com', 'google_auth', 'cliente', 1, '2026-07-01 04:03:57', NULL, NULL, NULL, NULL, NULL, 'default.png', NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `carritos`
--
ALTER TABLE `carritos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `carrito_detalles`
--
ALTER TABLE `carrito_detalles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unq_carrito_producto` (`carrito_id`,`producto_id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indices de la tabla `direcciones_usuario`
--
ALTER TABLE `direcciones_usuario`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `favoritos`
--
ALTER TABLE `favoritos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unq_usuario_producto` (`usuario_id`,`producto_id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indices de la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `referencia` (`referencia`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `pedido_detalles`
--
ALTER TABLE `pedido_detalles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pedido_id` (`pedido_id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_productos_proveedor` (`proveedor_id`);

--
-- Indices de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  ADD PRIMARY KEY (`id_proveedor`),
  ADD UNIQUE KEY `correo` (`gmail`);

--
-- Indices de la tabla `reportes_venta`
--
ALTER TABLE `reportes_venta`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `reseñas`
--
ALTER TABLE `reseñas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `producto_id` (`producto_id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `soporte`
--
ALTER TABLE `soporte`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `carritos`
--
ALTER TABLE `carritos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT de la tabla `carrito_detalles`
--
ALTER TABLE `carrito_detalles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de la tabla `direcciones_usuario`
--
ALTER TABLE `direcciones_usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT de la tabla `favoritos`
--
ALTER TABLE `favoritos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT de la tabla `pedido_detalles`
--
ALTER TABLE `pedido_detalles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  MODIFY `id_proveedor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `reportes_venta`
--
ALTER TABLE `reportes_venta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `reseñas`
--
ALTER TABLE `reseñas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `soporte`
--
ALTER TABLE `soporte`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `carritos`
--
ALTER TABLE `carritos`
  ADD CONSTRAINT `carritos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `carrito_detalles`
--
ALTER TABLE `carrito_detalles`
  ADD CONSTRAINT `carrito_detalles_ibfk_1` FOREIGN KEY (`carrito_id`) REFERENCES `carritos` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `carrito_detalles_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `direcciones_usuario`
--
ALTER TABLE `direcciones_usuario`
  ADD CONSTRAINT `direcciones_usuario_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `favoritos`
--
ALTER TABLE `favoritos`
  ADD CONSTRAINT `favoritos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `favoritos_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `pedido_detalles`
--
ALTER TABLE `pedido_detalles`
  ADD CONSTRAINT `pedido_detalles_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `pedido_detalles_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `fk_productos_proveedor` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedor` (`id_proveedor`) ON DELETE SET NULL;

--
-- Filtros para la tabla `reseñas`
--
ALTER TABLE `reseñas`
  ADD CONSTRAINT `reseñas_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `reseñas_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `soporte`
--
ALTER TABLE `soporte`
  ADD CONSTRAINT `soporte_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
