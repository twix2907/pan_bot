#!/usr/bin/env python3
"""
Test de conexión a la base de datos Railway
"""
import os
from dotenv import load_dotenv
import mysql.connector

# Cargar variables de entorno
load_dotenv()

def test_connection():
    """Test directo de conexión"""
    
    print("🔧 VERIFICANDO VARIABLES DE ENTORNO")
    print("=" * 50)
    
    # Verificar que las variables se cargan
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    
    print(f"DB_HOST: {db_host}")
    print(f"DB_PORT: {db_port}")
    print(f"DB_USER: {db_user}")
    print(f"DB_PASSWORD: {'*' * len(db_password) if db_password else 'None'}")
    print(f"DB_NAME: {db_name}")
    
    if not all([db_host, db_port, db_user, db_password, db_name]):
        print("❌ Faltan variables de entorno!")
        return False
    
    print("\n🔗 PROBANDO CONEXIÓN A RAILWAY...")
    print("=" * 50)
    
    try:
        connection = mysql.connector.connect(
            host=db_host,
            port=int(db_port),
            user=db_user,
            password=db_password,
            database=db_name,
            autocommit=True
        )
        
        print("✅ Conexión exitosa!")
        
        # Probar una consulta simple
        cursor = connection.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        print(f"✅ Consulta de prueba: {result}")
        
        # Verificar tablas
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"📊 Tablas encontradas: {[table[0] for table in tables]}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except mysql.connector.Error as error:
        print(f"❌ Error de conexión: {error}")
        return False

if __name__ == "__main__":
    success = test_connection()
    if success:
        print("\n🎉 Base de datos Railway lista para usar!")
    else:
        print("\n❌ Hay problemas con la conexión a Railway")
