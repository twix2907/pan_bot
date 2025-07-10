from database import execute_query, execute_insert

def get_productos_por_categoria(categoria):
    """
    Obtiene todos los productos de una categoría específica
    """
    query = """
    SELECT id, nombre, categoria, precio, descripcion, disponible 
    FROM productos 
    WHERE categoria = %s AND disponible = TRUE
    ORDER BY nombre
    """
    return execute_query(query, (categoria,))

def get_producto_por_id(producto_id):
    """
    Obtiene un producto específico por su ID
    """
    query = """
    SELECT id, nombre, categoria, precio, descripcion, disponible 
    FROM productos 
    WHERE id = %s AND disponible = TRUE
    """
    result = execute_query(query, (producto_id,))
    return result[0] if result else None

def crear_cliente(nombre, telefono, direccion=None):
    """
    Crea un nuevo cliente en la base de datos
    """
    # Verificar si el cliente ya existe
    query_check = "SELECT id FROM clientes WHERE telefono = %s"
    cliente_existente = execute_query(query_check, (telefono,))
    
    if cliente_existente:
        return cliente_existente[0]['id']
    
    # Crear nuevo cliente
    query_insert = """
    INSERT INTO clientes (nombre, telefono, direccion) 
    VALUES (%s, %s, %s)
    """
    return execute_insert(query_insert, (nombre, telefono, direccion))

def get_cliente_por_telefono(telefono):
    """
    Obtiene un cliente por su número de teléfono
    """
    query = "SELECT id, nombre, telefono, direccion FROM clientes WHERE telefono = %s"
    result = execute_query(query, (telefono,))
    return result[0] if result else None

def crear_pedido(cliente_id, fecha_entrega, tipo_entrega, direccion_entrega, total, notas=None):
    """
    Crea un nuevo pedido
    """
    # Si fecha_entrega es texto descriptivo, usar fecha de mañana por defecto
    from datetime import datetime, timedelta
    try:
        # Intentar parsear como fecha ISO
        if isinstance(fecha_entrega, str) and '-' in fecha_entrega:
            fecha_entrega_date = datetime.strptime(fecha_entrega, '%Y-%m-%d').date()
        else:
            # Si es texto descriptivo, usar mañana
            fecha_entrega_date = (datetime.now() + timedelta(days=1)).date()
    except:
        # En caso de error, usar mañana
        fecha_entrega_date = (datetime.now() + timedelta(days=1)).date()
    
    query = """
    INSERT INTO pedidos (cliente_id, fecha_entrega, tipo_entrega, direccion_entrega, estado, total, notas) 
    VALUES (%s, %s, %s, %s, 'confirmado', %s, %s)
    """
    return execute_insert(query, (cliente_id, fecha_entrega_date, tipo_entrega, direccion_entrega, total, notas))

def agregar_item_pedido(pedido_id, producto_id, cantidad, precio_unitario, notas=None):
    """
    Agrega un item a un pedido
    """
    query = """
    INSERT INTO pedido_items (pedido_id, producto_id, cantidad, precio_unitario, notas) 
    VALUES (%s, %s, %s, %s, %s)
    """
    return execute_insert(query, (pedido_id, producto_id, cantidad, precio_unitario, notas))

def get_pedido_completo(pedido_id):
    """
    Obtiene un pedido completo con todos sus items
    """
    # Obtener información del pedido
    query_pedido = """
    SELECT p.*, c.nombre as cliente_nombre, c.telefono as cliente_telefono 
    FROM pedidos p 
    JOIN clientes c ON p.cliente_id = c.id 
    WHERE p.id = %s
    """
    pedido = execute_query(query_pedido, (pedido_id,))
    if not pedido:
        return None
    
    # Obtener items del pedido
    query_items = """
    SELECT pi.*, pr.nombre as producto_nombre 
    FROM pedido_items pi 
    JOIN productos pr ON pi.producto_id = pr.id 
    WHERE pi.pedido_id = %s
    """
    items = execute_query(query_items, (pedido_id,))
    
    pedido_completo = pedido[0]
    pedido_completo['items'] = items or []
    
    return pedido_completo

def get_todas_categorias():
    """
    Obtiene todas las categorías disponibles de productos
    """
    query = """
    SELECT DISTINCT categoria 
    FROM productos 
    WHERE disponible = TRUE 
    ORDER BY categoria
    """
    return execute_query(query)

def buscar_producto_por_nombre(nombre_producto):
    """
    Busca un producto por nombre (búsqueda flexible)
    """
    # Primero búsqueda exacta
    query_exacta = """
    SELECT id, nombre, categoria, precio, descripcion, disponible 
    FROM productos 
    WHERE LOWER(nombre) = LOWER(%s) AND disponible = TRUE
    """
    resultado = execute_query(query_exacta, (nombre_producto,))
    
    if resultado:
        return resultado[0]
    
    # Si no encuentra exacto, búsqueda parcial
    query_parcial = """
    SELECT id, nombre, categoria, precio, descripcion, disponible 
    FROM productos 
    WHERE LOWER(nombre) LIKE LOWER(%s) AND disponible = TRUE
    ORDER BY LENGTH(nombre)
    LIMIT 1
    """
    resultado = execute_query(query_parcial, (f'%{nombre_producto}%',))
    
    return resultado[0] if resultado else None

def get_productos_mas_vendidos(limite=5):
    """
    Obtiene los productos más vendidos
    """
    query = """
    SELECT p.id, p.nombre, p.categoria, p.precio, p.descripcion, 
           COUNT(pi.id) as veces_pedido
    FROM productos p
    LEFT JOIN pedido_items pi ON p.id = pi.producto_id
    WHERE p.disponible = TRUE
    GROUP BY p.id, p.nombre, p.categoria, p.precio, p.descripcion
    ORDER BY veces_pedido DESC, p.nombre
    LIMIT %s
    """
    return execute_query(query, (limite,))
