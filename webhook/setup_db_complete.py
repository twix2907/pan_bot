import mysql.connector
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def create_tables():
    """
    Crea las tablas de la base de datos una por una
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            autocommit=True
        )
        
        cursor = connection.cursor()
        print("✅ Conexión exitosa a MySQL")
        
        # Tabla productos
        print("📊 Creando tabla productos...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL,
            categoria ENUM('pan_salado', 'pan_dulce', 'pan_semidulce', 'pasteles', 'bocaditos') NOT NULL,
            precio DECIMAL(8,2) NOT NULL,
            descripcion TEXT,
            disponible BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("✅ Tabla productos creada")
        
        # Tabla clientes
        print("📊 Creando tabla clientes...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL,
            telefono VARCHAR(20) UNIQUE NOT NULL,
            direccion TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("✅ Tabla clientes creada")
        
        # Tabla pedidos
        print("📊 Creando tabla pedidos...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
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
        )
        """)
        print("✅ Tabla pedidos creada")
        
        # Tabla pedido_items
        print("📊 Creando tabla pedido_items...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedido_items (
            id INT PRIMARY KEY AUTO_INCREMENT,
            pedido_id INT NOT NULL,
            producto_id INT NOT NULL,
            cantidad INT NOT NULL,
            precio_unitario DECIMAL(8,2) NOT NULL,
            notas TEXT,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
        """)
        print("✅ Tabla pedido_items creada")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 ¡Todas las tablas creadas exitosamente!")
        return True
        
    except mysql.connector.Error as error:
        print(f"❌ Error creando tablas: {error}")
        return False

def insert_sample_data():
    """
    Inserta datos de ejemplo
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            autocommit=True
        )
        
        cursor = connection.cursor()
        print("📝 Insertando datos de ejemplo...")
        
        # Pan Salado
        productos_pan_salado = [
            ('Ciabatti', 'pan_salado', 1.50, 'Pan salado tradicional italiano, crujiente por fuera y suave por dentro'),
            ('Francés', 'pan_salado', 0.50, 'Pan francés clásico, perfecto para desayunos'),
            ('Baguette', 'pan_salado', 2.00, 'Pan baguette crujiente, ideal para acompañar comidas')
        ]
        
        # Pan Dulce
        productos_pan_dulce = [
            ('Bizcocho', 'pan_dulce', 1.20, 'Bizcocho suave y esponjoso, tradicional de panadería'),
            ('Chancay', 'pan_dulce', 0.80, 'Pan dulce tradicional peruano, suave y ligeramente dulce'),
            ('Wawas', 'pan_dulce', 3.00, 'Pan en forma de muñeca, especial para festividades'),
            ('Caramanduca', 'pan_dulce', 1.80, 'Pan dulce con caramelo, delicioso y suave'),
            ('Panetones', 'pan_dulce', 25.00, 'Panetón tradicional, disponible en temporada navideña')
        ]
        
        # Panes Semidulces
        productos_semidulces = [
            ('Yema', 'pan_semidulce', 1.00, 'Pan con yema, ligeramente dulce y muy nutritivo'),
            ('Caracol', 'pan_semidulce', 1.50, 'Pan en forma de caracol con azúcar'),
            ('Integral', 'pan_semidulce', 2.50, 'Pan integral saludable, rico en fibra'),
            ('Camote', 'pan_semidulce', 2.00, 'Pan de camote, naturalmente dulce y nutritivo'),
            ('Petipanes', 'pan_semidulce', 0.60, 'Panes pequeños variados, perfectos para meriendas')
        ]
        
        # Pasteles
        productos_pasteles = [
            ('Torta de chocolate', 'pasteles', 35.00, 'Torta de chocolate húmeda - Precio base para 6 personas, personalizable en peso y diseño'),
            ('Tres Leches', 'pasteles', 40.00, 'Torta tres leches cremosa - Precio base para 6 personas, personalizable'),
            ('Torta helada', 'pasteles', 45.00, 'Torta helada refrescante - Precio base para 6 personas, personalizable'),
            ('Torta de naranja', 'pasteles', 32.00, 'Torta de naranja fresca - Precio base para 6 personas, personalizable'),
            ('Torta Marmoleado', 'pasteles', 38.00, 'Torta marmoleada clásica - Precio base para 6 personas, personalizable')
        ]
        
        # Bocaditos
        productos_bocaditos = [
            ('Empanaditas dulces', 'bocaditos', 1.20, 'Empanaditas dulces horneadas, rellenas de manjar'),
            ('Empanaditas de pollo', 'bocaditos', 1.50, 'Empanaditas saladas rellenas de pollo deshilachado'),
            ('Empanaditas de carne', 'bocaditos', 1.50, 'Empanaditas saladas rellenas de carne molida'),
            ('Enrolladitos de queso', 'bocaditos', 1.00, 'Enrollados de masa con queso derretido'),
            ('Enrolladitos de hot dog', 'bocaditos', 1.20, 'Enrollados de masa con hot dog'),
            ('Alfajor', 'bocaditos', 2.50, 'Alfajor tradicional relleno de manjar blanco'),
            ('Pionono', 'bocaditos', 3.00, 'Pionono dulce enrollado con manjar y coco')
        ]
        
        # Insertar todos los productos
        all_productos = productos_pan_salado + productos_pan_dulce + productos_semidulces + productos_pasteles + productos_bocaditos
        
        for producto in all_productos:
            try:
                cursor.execute("""
                INSERT INTO productos (nombre, categoria, precio, descripcion) 
                VALUES (%s, %s, %s, %s)
                """, producto)
                print(f"✅ Insertado: {producto[0]}")
            except mysql.connector.Error as e:
                if "Duplicate entry" in str(e):
                    print(f"⚠️  Ya existe: {producto[0]}")
                else:
                    print(f"❌ Error insertando {producto[0]}: {e}")
        
        # Insertar clientes de ejemplo
        clientes = [
            ('Juan Pérez', '+51999999999', 'Av. Ejemplo 123, Lima'),
            ('María García', '+51888888888', 'Jr. Prueba 456, San Isidro'),
            ('Carlos López', '+51777777777', 'Calle Test 789, Miraflores')
        ]
        
        for cliente in clientes:
            try:
                cursor.execute("""
                INSERT INTO clientes (nombre, telefono, direccion) 
                VALUES (%s, %s, %s)
                """, cliente)
                print(f"✅ Cliente insertado: {cliente[0]}")
            except mysql.connector.Error as e:
                if "Duplicate entry" in str(e):
                    print(f"⚠️  Cliente ya existe: {cliente[0]}")
                else:
                    print(f"❌ Error insertando cliente {cliente[0]}: {e}")
        
        # Verificar datos
        print("\n📋 Verificando datos insertados:")
        cursor.execute("SELECT categoria, COUNT(*) as cantidad FROM productos GROUP BY categoria")
        results = cursor.fetchall()
        for categoria, cantidad in results:
            print(f"  - {categoria}: {cantidad} productos")
        
        cursor.execute("SELECT COUNT(*) as total FROM clientes")
        total_clientes = cursor.fetchone()[0]
        print(f"  - Clientes: {total_clientes}")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 ¡Datos insertados exitosamente!")
        return True
        
    except mysql.connector.Error as error:
        print(f"❌ Error insertando datos: {error}")
        return False

if __name__ == "__main__":
    print("🚀 Configurando base de datos para Panadería Jos y Mar...")
    
    if create_tables():
        insert_sample_data()
    else:
        print("❌ No se pudieron crear las tablas")
