import mysql.connector
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def get_db_connection():
    """
    Establece conexión con la base de datos MySQL
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
        return connection
    except mysql.connector.Error as error:
        print(f"Error conectando a MySQL: {error}")
        return None

def execute_query(query, params=None):
    """
    Ejecuta una consulta SELECT y retorna los resultados
    """
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    except mysql.connector.Error as error:
        print(f"Error ejecutando consulta: {error}")
        return None

def execute_insert(query, params=None):
    """
    Ejecuta una consulta INSERT y retorna el ID del registro creado
    """
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        insert_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return insert_id
    except mysql.connector.Error as error:
        print(f"Error ejecutando insert: {error}")
        return None

def test_connection():
    """
    Prueba la conexión a la base de datos
    """
    connection = get_db_connection()
    if connection:
        print("✅ Conexión exitosa a la base de datos")
        connection.close()
        return True
    else:
        print("❌ Error en la conexión a la base de datos")
        return False
