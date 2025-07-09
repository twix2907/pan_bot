-- Datos de ejemplo para Panadería Jos y Mar
USE panaderia_jos_y_mar;

-- Pan Salado
INSERT INTO productos (nombre, categoria, precio, descripcion) VALUES
('Ciabatti', 'pan_salado', 1.50, 'Pan salado tradicional italiano, crujiente por fuera y suave por dentro'),
('Francés', 'pan_salado', 0.50, 'Pan francés clásico, perfecto para desayunos'),
('Baguette', 'pan_salado', 2.00, 'Pan baguette crujiente, ideal para acompañar comidas');

-- Pan Dulce
INSERT INTO productos (nombre, categoria, precio, descripcion) VALUES
('Bizcocho', 'pan_dulce', 1.20, 'Bizcocho suave y esponjoso, tradicional de panadería'),
('Chancay', 'pan_dulce', 0.80, 'Pan dulce tradicional peruano, suave y ligeramente dulce'),
('Wawas', 'pan_dulce', 3.00, 'Pan en forma de muñeca, especial para festividades'),
('Caramanduca', 'pan_dulce', 1.80, 'Pan dulce con caramelo, delicioso y suave'),
('Panetones', 'pan_dulce', 25.00, 'Panetón tradicional, disponible en temporada navideña');

-- Panes Semidulces
INSERT INTO productos (nombre, categoria, precio, descripcion) VALUES
('Yema', 'pan_semidulce', 1.00, 'Pan con yema, ligeramente dulce y muy nutritivo'),
('Caracol', 'pan_semidulce', 1.50, 'Pan en forma de caracol con azúcar'),
('Integral', 'pan_semidulce', 2.50, 'Pan integral saludable, rico en fibra'),
('Camote', 'pan_semidulce', 2.00, 'Pan de camote, naturalmente dulce y nutritivo'),
('Petipanes', 'pan_semidulce', 0.60, 'Panes pequeños variados, perfectos para meriendas');

-- Pasteles (precios base, se personalizan)
INSERT INTO productos (nombre, categoria, precio, descripcion) VALUES
('Torta de chocolate', 'pasteles', 35.00, 'Torta de chocolate húmeda - Precio base para 6 personas, personalizable en peso y diseño'),
('Tres Leches', 'pasteles', 40.00, 'Torta tres leches cremosa - Precio base para 6 personas, personalizable'),
('Torta helada', 'pasteles', 45.00, 'Torta helada refrescante - Precio base para 6 personas, personalizable'),
('Torta de naranja', 'pasteles', 32.00, 'Torta de naranja fresca - Precio base para 6 personas, personalizable'),
('Torta Marmoleado', 'pasteles', 38.00, 'Torta marmoleada clásica - Precio base para 6 personas, personalizable');

-- Bocaditos
INSERT INTO productos (nombre, categoria, precio, descripcion) VALUES
('Empanaditas dulces', 'bocaditos', 1.20, 'Empanaditas dulces horneadas, rellenas de manjar'),
('Empanaditas de pollo', 'bocaditos', 1.50, 'Empanaditas saladas rellenas de pollo deshilachado'),
('Empanaditas de carne', 'bocaditos', 1.50, 'Empanaditas saladas rellenas de carne molida'),
('Enrolladitos de queso', 'bocaditos', 1.00, 'Enrollados de masa con queso derretido'),
('Enrolladitos de hot dog', 'bocaditos', 1.20, 'Enrollados de masa con hot dog'),
('Alfajor', 'bocaditos', 2.50, 'Alfajor tradicional relleno de manjar blanco'),
('Pionono', 'bocaditos', 3.00, 'Pionono dulce enrollado con manjar y coco');

-- Cliente de ejemplo para pruebas
INSERT INTO clientes (nombre, telefono, direccion) VALUES
('Juan Pérez', '+51999999999', 'Av. Ejemplo 123, Lima'),
('María García', '+51888888888', 'Jr. Prueba 456, San Isidro'),
('Carlos López', '+51777777777', 'Calle Test 789, Miraflores');

-- Pedido de ejemplo
INSERT INTO pedidos (cliente_id, fecha_entrega, tipo_entrega, direccion_entrega, total, notas) VALUES
(1, '2025-01-11', 'delivery', 'Av. Ejemplo 123, Lima', 4.00, 'Pedido de prueba');

-- Items del pedido de ejemplo
INSERT INTO pedido_items (pedido_id, producto_id, cantidad, precio_unitario) VALUES
(1, 2, 2, 0.50),  -- 2 panes francés
(1, 11, 1, 35.00); -- 1 torta de chocolate

-- Mostrar datos insertados
SELECT 'PRODUCTOS POR CATEGORÍA:' as info;
SELECT categoria, COUNT(*) as cantidad FROM productos GROUP BY categoria;

SELECT 'TOTAL DE REGISTROS:' as info;
SELECT 
    (SELECT COUNT(*) FROM productos) as productos,
    (SELECT COUNT(*) FROM clientes) as clientes,
    (SELECT COUNT(*) FROM pedidos) as pedidos,
    (SELECT COUNT(*) FROM pedido_items) as items;
