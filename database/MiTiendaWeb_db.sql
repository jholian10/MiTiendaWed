CREATE DATABASE IF NOT EXISTS MiTiendaWeb_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE MiTiendaWeb_db;

-- 1. TABLA DE PRODUCTOS
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,         
    nombre VARCHAR(120) NOT NULL,                  
    descripcion TEXT NULL,                                                                           
    precio_compra DECIMAL(10, 2) NOT NULL,         
    precio_venta DECIMAL(10, 2) NOT NULL,           
    stock INT NOT NULL DEFAULT 0,                    
    stock_minimo INT NOT NULL DEFAULT 5,           
    imagen_url VARCHAR(255) NULL,                     
    estado TINYINT(1) NOT NULL DEFAULT 1,            
    creado_el TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_el TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. TABLA DE USUARIOS Y ROLES
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL, 
    rol ENUM('admin', 'cliente') NOT NULL DEFAULT 'cliente',
    activo TINYINT(1) NOT NULL DEFAULT 1,
    creado_el TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. TABLA DE FAVORITOS
CREATE TABLE IF NOT EXISTS favoritos (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    usuario_id INT NOT NULL,
    producto_id INT NOT NULL,
    agregado_el TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unq_usuario_producto (usuario_id, producto_id), 
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. TABLA DE CARRITOS
CREATE TABLE IF NOT EXISTS carritos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE, 
    actualizado_el TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. TABLA DE DETALLE DEL CARRITO
CREATE TABLE IF NOT EXISTS carrito_detalles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    carrito_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    agregado_el TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unq_carrito_producto (carrito_id, producto_id), 
    FOREIGN KEY (carrito_id) REFERENCES carritos(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS reseñas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    usuario_id INT NOT NULL,
    calificacion INT NOT NULL CHECK (calificacion >= 1 AND calificacion <= 5),
    comentario TEXT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);


-- =========================================================================
-- INSERCIÓN DE 10 PRODUCTOS (BOLSOS Y ACCESORIOS)
-- =========================================================================

INSERT INTO productos (nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_url, estado) VALUES
(
    'Bolso Tote Ejecutivo Cuero', 
    'Bolso de mano amplio confeccionado en cuero genuino con compartimento acolchado para laptop de hasta 14 pulgadas. Ideal para la oficina.', 
    45.00, 89.99, 15, 3, 
    'https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=600&q=80', 
    1
),
(
    'Mochira Urbana Minimalista', 
    'Mochila ligera e impermeable con cierres de seguridad ocultos y puerto de carga USB integrado. Perfecta para el día a día.', 
    20.00, 45.50, 25, 5, 
    'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=600&q=80', 
    1
),
(
    'Cartera de Hombro Casual', 
    'Cartera versátil con correa ajustable. Diseño contemporáneo texturizado con múltiples bolsillos internos organizadores.', 
    18.50, 39.99, 30, 5, 
    'https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&w=600&q=80', 
    1
),
(
    'Bolso Crossbody Elegante', 
    'Bolso cruzado pequeño con cadena dorada y solapa magnética. Forro interior de gamuza suave para salidas nocturnas.', 
    15.00, 34.99, 12, 4, 
    'https://images.unsplash.com/photo-1566150905458-1bf1fc113f0d?auto=format&fit=crop&w=600&q=80', 
    1
),
(
    'Billetera Clásica de Piel', 
    'Billetera compacta de cuero para hombre con protección RFID integrada y espacio optimizado para 8 tarjetas y billetes.', 
    8.00, 19.99, 50, 10, 
    'https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=600&q=80', 
    1
),
(
    'Bolso de Viaje Duffel Premium', 
    'Maletín de viaje espacioso de lona reforzada con detalles de cuero. Compartimento separado para calzado.', 
    35.00, 75.00, 10, 2, 
    'https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=600&q=80', 
    1
),
(
    'Cangurera Deportiva Ajustable', 
    'Riñonera ergonómica de nailon de alta densidad resistente al agua con salida para audífonos y franja reflectiva.', 
    6.50, 15.99, 40, 8, 
    'https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?auto=format&fit=crop&w=600&q=80', 
    1
),
(
    'Bolso de Mano Clutch Satín', 
    'Elegante clutch rígido con acabado satinado y broche de cristal. Incluye cadena desmontable para usar al hombro.', 
    12.00, 29.99, 18, 3, 
    'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=600&q=80', 
    1
),
(
    'Mochila Escolar Estampada', 
    'Mochila juvenil con costuras reforzadas, base acolchada y estampados geométricos. Espacio dedicado para cuadernos y carpetas.', 
    14.00, 28.50, 22, 5, 
    'https://images.unsplash.com/photo-1581605405669-fcdf81165afa?auto=format&fit=crop&w=600&q=80', 
    1
),
(
    'Neceser de Viaje Organizador', 
    'Bolsa de aseo colgante con gancho resistente y bolsillos de malla transparente para organizar artículos de cuidado personal.', 
    7.00, 18.00, 35, 5, 
    'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=600&q=80', 
    1
);