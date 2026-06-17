-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 17-06-2026 a las 23:56:17
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
-- Estructura de tabla para la tabla `carrito`
--

CREATE TABLE `carrito` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL DEFAULT 1,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carritos`
--

CREATE TABLE `carritos` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `actualizado_el` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `carritos`
--

INSERT INTO `carritos` (`id`, `usuario_id`, `actualizado_el`) VALUES
(6, 8, '2026-06-12 19:24:02'),
(7, 10, '2026-06-12 20:16:09'),
(8, 11, '2026-06-13 20:36:13'),
(10, 13, '2026-06-16 06:08:07'),
(11, 14, '2026-06-17 18:17:59'),
(13, 12, '2026-06-17 20:57:15');

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `carrito_detalles`
--

INSERT INTO `carrito_detalles` (`id`, `carrito_id`, `producto_id`, `cantidad`, `agregado_el`) VALUES
(52, 7, 14, 1, '2026-06-12 23:20:59');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `direcciones`
--

CREATE TABLE `direcciones` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `departamento` varchar(100) NOT NULL,
  `barrio` varchar(100) NOT NULL,
  `numero_casa` varchar(50) NOT NULL,
  `telefono` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `telefono_contacto` varchar(20) DEFAULT NULL,
  `es_principal` tinyint(1) DEFAULT 1,
  `barrio` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `direcciones_usuario`
--

INSERT INTO `direcciones_usuario` (`id`, `usuario_id`, `departamento`, `ciudad`, `direccion_detallada`, `telefono_contacto`, `es_principal`, `barrio`) VALUES
(1, 12, 'Atlántico', 'Candelaria', 'op{', 'N/A', 1, 'po'),
(2, 12, 'Boyacá', 'Belén', 'ghjgh', 'N/A', 1, 'ghfj'),
(3, 12, 'Cesar', 'Gamarra', 'Asdadx', 'N/A', 1, 'asxsa'),
(4, 12, 'Caquetá', 'Morelia', 'asd', 'N/A', 1, 'wd'),
(5, 12, 'Caquetá', 'Puerto Rico', 'RGERG', 'N/A', 1, 'SEFR'),
(6, 12, 'Boyacá', 'Buenavista', 'FGH', 'N/A', 1, 'GFH'),
(7, 12, 'Chocó', 'El Carmen del Darién', 'aS', 'N/A', 1, 'aSAs'),
(8, 12, 'Quindío', 'Quimbaya', 'fdsfds', 'N/A', 1, 'fds'),
(9, 12, 'Cauca', 'Florencia', 'ghjgh', 'N/A', 1, 'wd');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `favoritos`
--

CREATE TABLE `favoritos` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `agregado_el` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notificaciones`
--

CREATE TABLE `notificaciones` (
  `id` int(11) NOT NULL,
  `mensaje` text NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `notificaciones`
--

INSERT INTO `notificaciones` (`id`, `mensaje`, `fecha_creacion`) VALUES
(1, '¡Alerta de Inventario! El producto \"Bolso Tote Ejecutivo Cuero\" se ha agotado por completo.', '2026-06-12 20:06:19'),
(2, '¡Alerta de Inventario! El producto \"Bolso Crossbody Elegante\" fue modificado y se ha quedado AGOTADO (0 unidades).', '2026-06-12 20:12:07'),
(3, '¡Alerta de Inventario! El producto \"Bolso Crossbody Elegante\" se ha agotado por completo.', '2026-06-12 20:12:39'),
(4, '¡Alerta de Inventario! El producto \"Bolso Crossbody Elegante\" fue modificado y se ha quedado AGOTADO (0 unidades).', '2026-06-12 20:12:39'),
(5, '¡Producto Actualizado! El administrador modificó los datos de \"Cangurera Deportiva Ajustable\".', '2026-06-12 20:12:55'),
(6, '¡Producto Actualizado! El administrador modificó los datos de \"Bolso Crossbody Elegante\".', '2026-06-12 20:13:09'),
(7, '¡Atención! El producto \"Bolso Crossbody Elegante\" fue modificado y quedó por debajo del stock mínimo. Quedan 10 unidades.', '2026-06-12 20:13:32'),
(8, '¡Producto Eliminado! El administrador removió \"Bolso Crossbody Elegante\" del sistema.', '2026-06-12 20:14:53'),
(9, '¡Producto Actualizado! El administrador modificó los datos de \"Neceser de Viaje Organizador\".', '2026-06-12 20:15:15'),
(10, '¡Nuevo Producto! El administrador registró \"jholian manuel\" con -2 unidades en el inventario.', '2026-06-13 04:26:21'),
(11, '¡Producto Actualizado! El administrador modificó los datos de \"Mochila Wayuu Tradicional Geométrica\".', '2026-06-13 04:29:54'),
(12, '¡Alerta de Inventario! El producto \"Mochila Wayuu Tradicional Geométrica\" se ha agotado por completo.', '2026-06-13 04:38:38'),
(13, '¡Alerta de Inventario! El producto \"Mochila Wayuu Tradicional Geométrica\" fue modificado y se ha quedado AGOTADO (0 unidades).', '2026-06-13 04:38:38'),
(14, '¡Nuevo Producto! El administrador registró \"ytt\" con -1 unidades en el inventario.', '2026-06-13 16:49:17'),
(15, 'Producto registrado: dsger', '2026-06-13 17:00:21'),
(16, 'Producto registrado: sedf', '2026-06-13 17:00:43'),
(17, '¡Producto Eliminado! El administrador removió \"Mochila Wayuu Tradicional Geométrica\" del sistema.', '2026-06-13 17:55:21'),
(18, '¡Producto Eliminado! El administrador removió \"sedf\" del sistema.', '2026-06-13 17:59:50'),
(19, '¡Producto Eliminado! El administrador removió \"dsger\" del sistema.', '2026-06-13 18:00:04'),
(20, '¡Producto Eliminado! El administrador removió \"dsger\" del sistema.', '2026-06-13 18:00:08'),
(21, '¡Producto Eliminado! El administrador removió \"dsger\" del sistema.', '2026-06-13 18:00:12'),
(22, '¡Producto Eliminado! El administrador removió \"jholian manuel\" del sistema.', '2026-06-13 18:00:18'),
(23, '¡Producto Eliminado! El administrador removió \"ytt\" del sistema.', '2026-06-13 18:00:21'),
(24, '¡Producto Eliminado! El administrador removió \"Bolso de Caña Flecha Zenú\" del sistema.', '2026-06-16 06:49:25'),
(25, 'Producto registrado: wqd', '2026-06-16 06:50:06'),
(26, '¡Alerta de Inventario! El producto \"Cartera de Palma de Iraca Natural\" fue modificado y se ha quedado AGOTADO (0 unidades).', '2026-06-16 07:09:48'),
(27, '¡Alerta de Inventario! El producto \"Mochila Arhuaca de Lana Pura\" se ha agotado por completo.', '2026-06-16 07:10:26'),
(28, '¡Atención! El producto \"Mochila Arhuaca de Lana Pura\" fue modificado y quedó por debajo del stock mínimo. Quedan -67 unidades.', '2026-06-16 07:10:26'),
(29, '¡Alerta de Inventario! El producto \"Mochila Arhuaca de Lana Pura\" fue modificado y se ha quedado AGOTADO (0 unidades).', '2026-06-17 21:06:21'),
(30, 'Producto registrado: jholian manuel', '2026-06-17 21:09:03');

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `pedidos`
--

INSERT INTO `pedidos` (`id`, `usuario_id`, `referencia`, `total`, `estado`, `direccion_envio`, `ciudad_envio`, `telefono_contacto`, `fecha_creacion`) VALUES
(3, 8, 'ORD_8_1781301058278', 185000.00, 'PENDIENTE', '', '', '', '2026-06-12 21:50:58'),
(4, 12, 'ORD_12_1781420046009', 329900.00, 'PENDIENTE', '', '', '', '2026-06-14 06:54:06'),
(5, 12, 'ORD_12_1781420649302', 329900.00, 'PENDIENTE', '', '', '', '2026-06-14 07:04:09'),
(6, 12, 'ORD_12_1781420654603', 329900.00, 'PENDIENTE', '', '', '', '2026-06-14 07:04:14'),
(7, 12, 'ORD_12_1781421094034', 329900.00, 'PENDIENTE', '', '', '', '2026-06-14 07:11:34'),
(8, 12, 'ORD_12_1781454046575', 329900.00, 'PENDIENTE', '', '', '', '2026-06-14 16:20:46'),
(9, 12, 'ORD_12_1781723482636', 54933.00, 'PENDIENTE', '', '', '', '2026-06-17 19:11:22'),
(10, 12, 'ORD_12_1781724592448', 418000.00, 'PENDIENTE', '', '', '', '2026-06-17 19:29:52'),
(11, 12, 'ORD_12_1781726111421', 144900.00, 'PENDIENTE', '', '', '', '2026-06-17 19:55:11'),
(18, 12, 'ORD_12_1781729427500', 144900.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-17 20:50:27'),
(19, 12, 'ORD_12_1781729444931', 144900.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-17 20:50:44'),
(20, 12, 'ORD_12_1781729850847', 275000.00, 'PENDIENTE', 'No especificada', 'No especificada', 'No especificado', '2026-06-17 20:57:30');

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio_compra` decimal(10,2) NOT NULL,
  `precio_venta` decimal(10,2) NOT NULL,
  `stock` int(11) NOT NULL DEFAULT 0,
  `stock_minimo` int(11) NOT NULL DEFAULT 5,
  `imagen_url` varchar(255) DEFAULT NULL,
  `estado` tinyint(1) NOT NULL DEFAULT 1,
  `creado_el` timestamp NOT NULL DEFAULT current_timestamp(),
  `actualizado_el` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `nombre`, `descripcion`, `precio_compra`, `precio_venta`, `stock`, `stock_minimo`, `imagen_url`, `estado`, `creado_el`, `actualizado_el`) VALUES
(13, 'Mochila Wayuu Tradicional Geométrica', '120000.00', 15.00, 0.00, 0, 0, '60000.00', 0, '2026-06-12 20:38:11', '2026-06-13 17:55:21'),
(14, 'Bolso de Caña Flecha Zenú', 'Elegante bolso de hombro elaborado con la tradicional técnica de trenzado de caña flecha. Estructura rígida y duradera.', 75000.00, 145000.00, 10, 2, 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=600&q=80', 0, '2026-06-12 20:38:11', '2026-06-16 06:49:25'),
(15, 'Cartera de Palma de Iraca Natural', '45000.00', 89900.00, 0.00, 1, 0, 'Cartera artesanal tejida en palma de iraca fina por artesanos de Sandoná, Nariño. Ideal para días soleados y eventos casuales.', 1, '2026-06-12 20:38:11', '2026-06-16 07:09:48'),
(16, 'Mochila Arhuaca de Lana Pura', '185000.00', 0.00, 0.00, 0, 0, '90000.00', 1, '2026-06-12 20:38:11', '2026-06-17 21:06:21'),
(17, 'Bolso Tote en Macramé Algodón', 'Bolso amplio estilo tote tejido en hilos de algodón con la técnica de nudos macramé. Incluye forro interno de tela protectora.', 25000.00, 55000.00, 25, 5, 'https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?auto=format&fit=crop&w=600&q=80', 1, '2026-06-12 20:38:11', '2026-06-12 20:38:11'),
(18, 'Cartera de Cuero Repujado a Mano', 'Bolso de cuero de alta calidad con grabados precolombinos repujados artesanalmente. Herrajes de larga duración.', 110000.00, 220000.00, 12, 3, 'https://images.unsplash.com/photo-1566150905458-1bf1fc113f0d?auto=format&fit=crop&w=600&q=80', 1, '2026-06-12 20:38:11', '2026-06-12 20:38:11'),
(19, 'Mochila Wayuu Unicolor Pastel', 'Mochila tejida a mano en un solo tono suave, ideal para combinar con outfits modernos manteniendo el toque tradicional.', 55000.00, 110000.00, 14, 3, 'https://images.unsplash.com/photo-1581605405669-fcdf81165afa?auto=format&fit=crop&w=600&q=80', 1, '2026-06-12 20:38:11', '2026-06-12 20:38:11'),
(20, 'Bolso Playero de Fique Rústico', 'Bolso espacioso fabricado con fibras naturales de fique tinturadas con extractos orgánicos. Resistente y ecoamigable.', 30000.00, 65000.00, 30, 5, 'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=600&q=80', 1, '2026-06-12 20:38:11', '2026-06-12 20:38:11'),
(21, 'Canasto de Mimbre con Apliques', 'Canasto artesanal de mimbre tejido con asas reforzadas en cuero y pompones decorativos de colores vibrantes.', 38000.00, 78000.00, 18, 4, 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=600&q=80', 1, '2026-06-12 20:38:11', '2026-06-12 20:38:11'),
(22, 'Bandolera en Telar Indígena', 'Bolso estilo manos libres con correa ajustable confeccionado a partir de lienzos tejidos en telar vertical guambiano.', 40000.00, 85000.00, 16, 4, 'https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=600&q=80', 1, '2026-06-12 20:38:11', '2026-06-12 20:38:11'),
(23, 'Bolso de Lujo en Werregue', 'Pieza exclusiva tejida con la finísima fibra de la palma de werregue por la comunidad Emberá Wounaan del Chocó.', 150000.00, 320000.00, 5, 1, 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=600&q=80', 1, '2026-06-12 20:38:11', '2026-06-12 20:38:11'),
(24, 'Mochila de Fique y Cuero Premium', 'Fusión perfecta entre el tejido artesanal de fique y acabados elegantes en cuero legítimo. Cierre de cordón ajustable.', 65000.00, 130000.00, 10, 2, 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=600&q=80', 1, '2026-06-12 20:38:11', '2026-06-12 20:38:11'),
(25, 'Cartera Sobre de Palma de Iraca', 'Clutch plano tipo sobre tejido a mano en iraca tinturada. Perfecto para acompañar vestidos en celebraciones de playa.', 22000.00, 49900.00, 22, 5, 'https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&w=600&q=80', 1, '2026-06-12 20:38:11', '2026-06-12 20:38:11'),
(26, 'Bolso Tote Étnico Jacquard', 'Bolso amplio con patrones étnicos en tela jacquard pesada y cargaderas de cuero trenzado muy resistentes.', 45000.00, 95000.00, 15, 3, 'https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=600&q=80', 1, '2026-06-12 20:38:11', '2026-06-12 20:38:11'),
(27, 'Cangurera de Tela Artesanal', 'Riñonera compacta hecha con retazos de telares andinos tradicionales. Dos compartimentos seguros con cremallera.', 18000.00, 39000.00, 40, 6, 'https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?auto=format&fit=crop&w=600&q=80', 1, '2026-06-12 20:38:11', '2026-06-12 20:38:11'),
(28, 'Bolso de Mano Mola Guna', 'Bolso estructurado que incorpora una mola original en la parte frontal, cosida en capas de telas de colores por artesanas Guna.', 70000.00, 150000.00, 11, 2, 'https://images.unsplash.com/photo-1566150905458-1bf1fc113f0d?auto=format&fit=crop&w=600&q=80', 1, '2026-06-12 20:38:11', '2026-06-12 20:38:11'),
(29, 'Mochila Wayuu con Pedrería Fina', 'Edición especial de mochila Wayuu decorada con cristales y mostacillas cosidas a mano sobre las figuras del tejido.', 95000.00, 199900.00, 7, 2, 'https://images.unsplash.com/photo-1581605405669-fcdf81165afa?auto=format&fit=crop&w=600&q=80', 1, '2026-06-12 20:38:11', '2026-06-12 20:38:11'),
(30, 'Maletín de Viaje en Cuero y Telar', 'Maletín viajero amplio de lona gruesa combinada con cuero vacuno y apliques laterales de tejidos nativos.', 130000.00, 260000.00, 6, 2, 'https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=600&q=80', 1, '2026-06-12 20:38:11', '2026-06-12 20:38:11'),
(31, 'Canasto de Iraca Calado Elegante', 'Bolso de mano tipo cesta con un intrincado patrón calado en palma de iraca. Manija superior rígida circular.', 50000.00, 115000.00, 13, 3, 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=600&q=80', 1, '2026-06-12 20:38:11', '2026-06-12 20:38:11'),
(32, 'Bolso Crossbody de Fique Negro', 'Pequeño bolso manos libres elaborado en fique tinturado de color negro con broche magnético y correa de cadena.', 32000.00, 69900.00, 20, 5, 'https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=600&q=80', 1, '2026-06-12 20:38:11', '2026-06-12 20:38:11'),
(33, 'jholian manuel', '-0.06', -0.04, -2.00, -1, 0, 'hgjg', 0, '2026-06-13 04:26:21', '2026-06-13 18:00:18'),
(34, 'ytt', '-0.01', -0.01, -1.00, 4, 0, '', 0, '2026-06-13 16:49:17', '2026-06-13 18:00:21'),
(35, 'dsger', 'fxghfg', 67.00, 456.00, 4564, 5456, NULL, 0, '2026-06-13 16:55:58', '2026-06-13 18:00:12'),
(36, 'dsger', 'fxghfg', 67.00, 456.00, 4564, 5456, NULL, 0, '2026-06-13 16:56:23', '2026-06-13 18:00:08'),
(37, 'dsger', 'fxghfg', 67.00, 456.00, 4564, 5456, 'uploads/Captura_de_pantalla_2026-06-12_153320.png', 0, '2026-06-13 17:00:21', '2026-06-13 18:00:04'),
(38, 'sedf', '', 0.02, 0.04, 2, 5, 'uploads/Captura_de_pantalla_2026-06-12_153320.png', 0, '2026-06-13 17:00:43', '2026-06-13 17:59:50'),
(39, 'wqd', 'sad', 0.03, 0.03, 4, 5, 'uploads/Captura_de_pantalla_2026-06-12_153320.png', 1, '2026-06-16 06:50:06', '2026-06-16 06:50:06'),
(40, 'jholian manuel', 'esfdsedrf', 0.01, 0.01, 1, 5, 'uploads/Screenshot_2026.06.11_13.31.10.293.png', 1, '2026-06-17 21:09:03', '2026-06-17 21:09:03');

--
-- Disparadores `productos`
--
DELIMITER $$
CREATE TRIGGER `alerta_nuevo_sin_stock` AFTER INSERT ON `productos` FOR EACH ROW BEGIN
    -- Si el producto se crea directamente en 0
    IF NEW.stock = 0 THEN
        INSERT INTO notificaciones (mensaje, fecha_creacion)
        VALUES (CONCAT('¡Alerta de Inventario! El nuevo producto "', NEW.nombre, '" se ha registrado sin existencias (0 unidades).'), NOW());
    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `alerta_stock_agotado` AFTER UPDATE ON `productos` FOR EACH ROW BEGIN
    -- 1. Si el stock llegó a 0 y antes era mayor a 0, creamos alerta de AGOTADO
    IF NEW.stock = 0 AND OLD.stock > 0 THEN
        INSERT INTO notificaciones (mensaje, fecha_creacion)
        VALUES (CONCAT('¡Alerta de Inventario! El producto "', NEW.nombre, '" se ha agotado por completo.'), NOW());
    
    -- 2. Si baja del stock mínimo, creamos alerta de STOCK BAJO
    ELSEIF NEW.stock <= NEW.stock_minimo AND OLD.stock > NEW.stock_minimo AND NEW.stock > 0 THEN
        INSERT INTO notificaciones (mensaje, fecha_creacion)
        VALUES (CONCAT('¡Atención! El producto "', NEW.nombre, '" está por debajo del límite mínimo. Quedan solo ', NEW.stock, ' unidades.'), NOW());
    END IF;
END
$$
DELIMITER ;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `reseñas`
--

INSERT INTO `reseñas` (`id`, `producto_id`, `usuario_id`, `calificacion`, `comentario`, `fecha_creacion`) VALUES
(1, 27, 8, 5, 'jm,hj', '2026-06-12 22:08:59');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `soporte`
--

CREATE TABLE `soporte` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `mensaje` text DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `estado` varchar(20) DEFAULT 'pendiente',
  `tipo` varchar(50) DEFAULT 'general',
  `remitente` varchar(20) DEFAULT 'cliente',
  `leido` tinyint(4) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(150) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `rol` enum('admin','cliente') NOT NULL DEFAULT 'cliente',
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `creado_el` timestamp NOT NULL DEFAULT current_timestamp(),
  `codigo_recuperacion` varchar(6) DEFAULT NULL,
  `codigo_expira` datetime DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `foto_perfil` varchar(255) DEFAULT 'default.png',
  `foto_perfil_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `correo`, `password_hash`, `rol`, `activo`, `creado_el`, `codigo_recuperacion`, `codigo_expira`, `telefono`, `direccion`, `ciudad`, `foto_perfil`, `foto_perfil_url`) VALUES
(7, 'Administrador Principal', 'admin@dunaka.com', 'pbkdf2:sha256:600000$h6w4dJbA$7c5e9f8a3b2d1e4c6a8b0d9f2e4a6c8b0d9f2e4a6c8b0d9f2e4a6c8b0d9f2e4a', 'admin', 1, '2026-06-12 18:17:28', NULL, NULL, NULL, NULL, NULL, 'default.png', NULL),
(8, 'Admin Nuevo', 'nuevoadmin@dunaka.com', 'scrypt:32768:8:1$b8X3lSRtysONM3v7$6116bfc7b704937d874db36735af277638e5acf58547174f983b0639b59975d44e74a15d8ad02f804814d3a6f2f3681513abd15b3d4e490df342116a9a0bcb48', 'admin', 1, '2026-06-12 18:31:22', NULL, NULL, '', '', 'soladas', 'default.png', '/static/uploads/perfiles/user_8.png'),
(10, 'Eliad Suarez', 'eliadsuarez8@gmail.com', 'google_auth', 'cliente', 1, '2026-06-12 20:16:08', NULL, NULL, NULL, NULL, NULL, 'default.png', NULL),
(11, 'Angi', 'agutierrezreales@gmail.com', 'scrypt:32768:8:1$ZwIboherOZkbWubS$9820fd3c7292bedea759dcb9a39bacc0c20ce9e742aeabeb59b8e47996bbdcb33d83e7814027f6492acb12a5d31f43fa63928dfe7ef5228a50370ccbf5043052', 'cliente', 1, '2026-06-13 20:36:10', NULL, NULL, NULL, NULL, NULL, 'default.png', NULL),
(12, 'jholian manuel', 'jholianmanuel10@gmail.com', 'google_auth', 'cliente', 1, '2026-06-14 05:44:18', NULL, NULL, '', '', '', 'default.png', '/static/uploads/perfiles/user_12.png'),
(13, 'LUCIANA SOFIA', 'lucianasofia2605@gmail.com', 'google_auth', 'cliente', 1, '2026-06-16 06:08:06', NULL, NULL, NULL, NULL, NULL, 'default.png', NULL),
(14, 'Jholian', 'manuel@gmail.com', 'scrypt:32768:8:1$0GI8cpaatqZgFnXd$3e654dcaa79048459a12d3998b6ad7ef7b574bfeccd504f906914b65ee401ddc702a31cf9c12578b752a85953efa5767e858ab2632b32d97e7e51a1c9e6ec620', 'cliente', 1, '2026-06-17 18:17:53', NULL, NULL, NULL, NULL, NULL, 'default.png', NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `producto_id` (`producto_id`);

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
-- Indices de la tabla `direcciones`
--
ALTER TABLE `direcciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

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
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `idx_pedidos_referencia` (`referencia`);

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
  ADD KEY `idx_productos_estado` (`estado`);

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
  ADD PRIMARY KEY (`id`);

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
-- AUTO_INCREMENT de la tabla `carrito`
--
ALTER TABLE `carrito`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `carritos`
--
ALTER TABLE `carritos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `carrito_detalles`
--
ALTER TABLE `carrito_detalles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=75;

--
-- AUTO_INCREMENT de la tabla `direcciones`
--
ALTER TABLE `direcciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `direcciones_usuario`
--
ALTER TABLE `direcciones_usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `favoritos`
--
ALTER TABLE `favoritos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `pedido_detalles`
--
ALTER TABLE `pedido_detalles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT de la tabla `reseñas`
--
ALTER TABLE `reseñas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `soporte`
--
ALTER TABLE `soporte`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=76;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD CONSTRAINT `carrito_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `carrito_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE;

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
-- Filtros para la tabla `direcciones`
--
ALTER TABLE `direcciones`
  ADD CONSTRAINT `direcciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

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
  ADD CONSTRAINT `fk_usuario_pedido` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `pedido_detalles`
--
ALTER TABLE `pedido_detalles`
  ADD CONSTRAINT `pedido_detalles_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `pedido_detalles_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `reseñas`
--
ALTER TABLE `reseñas`
  ADD CONSTRAINT `reseñas_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `reseñas_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
