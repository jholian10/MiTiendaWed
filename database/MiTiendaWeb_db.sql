CREATE DATABASE IF NOT EXISTS mitiendaweb_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mitiendaweb_db;

SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE usuarios (
  id int(11) NOT NULL AUTO_INCREMENT,
  nombre varchar(100) NOT NULL,
  correo varchar(150) NOT NULL,
  password_hash varchar(255) NOT NULL,
  rol ENUM('superadmin', 'admin', 'cliente') NOT NULL DEFAULT 'cliente',
  activo tinyint(1) NOT NULL DEFAULT 1,
  creado_el timestamp NOT NULL DEFAULT current_timestamp(),
  codigo_recuperacion varchar(6) DEFAULT NULL,
  codigo_expira datetime DEFAULT NULL,
  telefono varchar(20) DEFAULT NULL,
  direccion varchar(255) DEFAULT NULL,
  ciudad varchar(100) DEFAULT NULL,
  foto_perfil varchar(255) DEFAULT 'default.png',
  foto_perfil_url varchar(255) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY correo_unique (correo)
);

CREATE TABLE productos (
  id int(11) NOT NULL AUTO_INCREMENT,
  nombre varchar(120) NOT NULL,
  descripcion text DEFAULT NULL,
  precio_compra decimal(10,2) NOT NULL,
  precio_venta decimal(10,2) NOT NULL,
  stock int(11) NOT NULL DEFAULT 0,
  stock_minimo int(11) NOT NULL DEFAULT 0,
  imagen_url varchar(255) DEFAULT NULL,
  estado tinyint(1) NOT NULL DEFAULT 1,
  creado_el timestamp NOT NULL DEFAULT current_timestamp(),
  actualizado_el timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (id)
);

CREATE TABLE direcciones_usuario (
  id int(11) NOT NULL AUTO_INCREMENT,
  usuario_id int(11) NOT NULL,
  departamento varchar(100) NOT NULL,
  ciudad varchar(100) NOT NULL,
  direccion_detallada varchar(255) NOT NULL,
  telefono_contacto varchar(20) DEFAULT NULL,
  es_principal tinyint(1) NOT NULL DEFAULT 0,
  barrio varchar(100) DEFAULT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_dir_usuario_id FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
);

CREATE TABLE direcciones (
  id int(11) NOT NULL AUTO_INCREMENT,
  usuario_id int(11) NOT NULL,
  departamento varchar(100) NOT NULL,
  barrio varchar(100) DEFAULT NULL,
  numero_casa varchar(50) DEFAULT NULL,
  telefono varchar(20) DEFAULT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_direcciones_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
);

CREATE TABLE carritos (
  id int(11) NOT NULL AUTO_INCREMENT,
  usuario_id int(11) NOT NULL,
  actualizado_el timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (id),
  CONSTRAINT fk_carritos_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
);

CREATE TABLE carrito_detalles (
  id int(11) NOT NULL AUTO_INCREMENT,
  carrito_id int(11) NOT NULL,
  producto_id int(11) NOT NULL,
  cantidad int(11) NOT NULL DEFAULT 1,
  agregado_el timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id),
  CONSTRAINT fk_detalles_carrito FOREIGN KEY (carrito_id) REFERENCES carritos (id) ON DELETE CASCADE,
  CONSTRAINT fk_detalles_producto FOREIGN KEY (producto_id) REFERENCES productos (id) ON DELETE CASCADE
);

CREATE TABLE carrito (
  id int(11) NOT NULL AUTO_INCREMENT,
  usuario_id int(11) NOT NULL,
  producto_id int(11) NOT NULL,
  cantidad int(11) NOT NULL DEFAULT 1,
  created_at datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id),
  CONSTRAINT fk_carrito_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE,
  CONSTRAINT fk_carrito_producto FOREIGN KEY (producto_id) REFERENCES productos (id) ON DELETE CASCADE
);

CREATE TABLE favoritos (
  id int(11) NOT NULL AUTO_INCREMENT,
  usuario_id int(11) NOT NULL,
  producto_id int(11) NOT NULL,
  agregado_el timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id),
  CONSTRAINT fk_favoritos_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE,
  CONSTRAINT fk_favoritos_producto FOREIGN KEY (producto_id) REFERENCES productos (id) ON DELETE CASCADE
);

CREATE TABLE pedidos (
  id int(11) NOT NULL AUTO_INCREMENT,
  usuario_id int(11) NOT NULL,
  referencia varchar(100) NOT NULL,
  total decimal(10,2) NOT NULL,
  estado ENUM('PENDIENTE', 'PAGADO', 'EMPACANDO', 'EN_TRANSITO', 'ENTREGADO') NOT NULL DEFAULT 'PENDIENTE',
  direccion_envio varchar(255) NOT NULL,
  ciudad_envio varchar(100) NOT NULL,
  telefono_contacto varchar(20) DEFAULT NULL,
  fecha_creacion timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id),
  CONSTRAINT fk_pedidos_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
);

CREATE TABLE pedido_detalles (
  id int(11) NOT NULL AUTO_INCREMENT,
  pedido_id int(11) NOT NULL,
  producto_id int(11) NOT NULL,
  cantidad int(11) NOT NULL DEFAULT 1,
  precio_unitario decimal(10,2) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_detalles_pedido FOREIGN KEY (pedido_id) REFERENCES pedidos (id) ON DELETE CASCADE,
  CONSTRAINT fk_detalles_ped_producto FOREIGN KEY (producto_id) REFERENCES productos (id) ON DELETE CASCADE
);

CREATE TABLE reseñas (
  id int(11) NOT NULL AUTO_INCREMENT,
  producto_id int(11) NOT NULL,
  usuario_id int(11) NOT NULL,
  calificacion int(11) NOT NULL,
  comentario text DEFAULT NULL,
  fecha_creacion timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id),
  CONSTRAINT fk_reseñas_producto FOREIGN KEY (producto_id) REFERENCES productos (id) ON DELETE CASCADE,
  CONSTRAINT fk_reseñas_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
);

CREATE TABLE soporte (
  id int(11) NOT NULL AUTO_INCREMENT,
  usuario_id int(11) DEFAULT NULL,
  remitente varchar(50) NOT NULL DEFAULT 'cliente',
  nombre varchar(100) DEFAULT NULL,
  correo varchar(150) DEFAULT NULL,
  asunto varchar(150) DEFAULT NULL,
  mensaje text NOT NULL,
  estado ENUM('PENDIENTE', 'EN_PROCESO', 'RESUELTO') NOT NULL DEFAULT 'PENDIENTE',
  fecha_creacion timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id),
  CONSTRAINT fk_soporte_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE SET NULL
);

CREATE TABLE notificaciones (
  id int(11) NOT NULL AUTO_INCREMENT,
  mensaje text NOT NULL,
  fecha_creacion timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id)
);

SET FOREIGN_KEY_CHECKS = 1;