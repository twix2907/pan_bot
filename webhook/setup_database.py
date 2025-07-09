import mysql.connector
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def setup_database():
    """
    Configura la base de datos con esquema y datos de ejemplo
    """
    try:
        # Conectar a MySQL
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
        
        # Leer y ejecutar schema.sql
        print("📊 Creando esquema de base de datos...")
        with open('../database/schema.sql', 'r', encoding='utf-8') as file:
            schema_content = file.read()
        
        # Dividir por statements y ejecutar uno por uno
        statements = schema_content.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--') and 'CREATE DATABASE' not in statement and 'USE ' not in statement:
                try:
                    cursor.execute(statement)
                    print(f"✅ Ejecutado: {statement[:50]}...")
                except mysql.connector.Error as e:
                    if "Table" in str(e) and "already exists" in str(e):
                        print(f"⚠️  Tabla ya existe: {statement[:50]}...")
                    else:
                        print(f"❌ Error en: {statement[:50]}... - {e}")
        
        # Leer y ejecutar sample_data.sql
        print("📝 Insertando datos de ejemplo...")
        with open('../database/sample_data.sql', 'r', encoding='utf-8') as file:
            data_content = file.read()
        
        # Dividir por statements y ejecutar uno por uno
        statements = data_content.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--') and 'USE ' not in statement and 'SELECT' not in statement:
                try:
                    cursor.execute(statement)
                    print(f"✅ Insertado: {statement[:50]}...")
                except mysql.connector.Error as e:
                    if "Duplicate entry" in str(e):
                        print(f"⚠️  Dato ya existe: {statement[:50]}...")
                    else:
                        print(f"❌ Error insertando: {statement[:50]}... - {e}")
        
        # Verificar datos
        print("\n📋 Verificando datos insertados:")
        cursor.execute("SELECT categoria, COUNT(*) as cantidad FROM productos GROUP BY categoria")
        results = cursor.fetchall()
        for categoria, cantidad in results:
            print(f"  - {categoria}: {cantidad} productos")
        
        cursor.execute("SELECT COUNT(*) as total_clientes FROM clientes")
        total_clientes = cursor.fetchone()[0]
        print(f"  - Clientes: {total_clientes}")
        
        cursor.execute("SELECT COUNT(*) as total_pedidos FROM pedidos")
        total_pedidos = cursor.fetchone()[0]
        print(f"  - Pedidos: {total_pedidos}")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 ¡Base de datos configurada exitosamente!")
        return True
        
    except mysql.connector.Error as error:
        print(f"❌ Error configurando base de datos: {error}")
        return False

if __name__ == "__main__":
    setup_database()
