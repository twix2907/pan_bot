-- Crear base de datos (ejecutar primero)
CREATE DATABASE IF NOT EXISTS panaderia_jos_y_mar 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE panaderia_jos_y_mar;

-- Tabla: productos
CREATE TABLE productos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    categoria ENUM('pan_salado', 'pan_dulce', 'pan_semidulce', 'pasteles', 'bocaditos') NOT NULL,
    precio DECIMAL(8,2) NOT NULL,
    descripcion TEXT,
    disponible BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: clientes
CREATE TABLE clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) UNIQUE NOT NULL,
    direccion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: pedidos
CREATE TABLE pedidos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cliente_id INT NOT NULL,
    fecha_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_entrega DATE NOT NULL,
    tipo_entrega ENUM('delivery', 'recojo') NOT NULL,
    direccion_entrega TEXT,
    estado ENUM('pendiente', 'confirmado', 'preparando', 'listo', 'entregado', 'cancelado') DEFAULT 'pendiente',
    total DECIMAL(10,2) NOT NULL,
    notas TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- Tabla: pedido_items
CREATE TABLE pedido_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(8,2) NOT NULL,
    notas TEXT,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Índices para mejorar performance
CREATE INDEX idx_productos_categoria ON productos(categoria);
CREATE INDEX idx_productos_disponible ON productos(disponible);
CREATE INDEX idx_clientes_telefono ON clientes(telefono);
CREATE INDEX idx_pedidos_fecha ON pedidos(fecha_pedido);
CREATE INDEX idx_pedidos_estado ON pedidos(estado);
