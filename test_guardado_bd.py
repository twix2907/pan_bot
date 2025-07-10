#!/usr/bin/env python3
"""
Test para verificar que el pedido se guarde en la base de datos
"""
import requests
import mysql.connector
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

WEBHOOK_URL = "http://localhost:5000/webhook"

def get_db_config():
    """Obtener configuración de BD desde variables de entorno"""
    return {
        'host': os.getenv('DB_HOST'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }

def verificar_pedido_en_bd(telefono):
    """Verificar que el pedido se guardó en la base de datos"""
    try:
        db_config = get_db_config()
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Buscar cliente por teléfono
        cursor.execute("SELECT * FROM clientes WHERE telefono = %s", (telefono,))
        cliente = cursor.fetchone()
        
        if not cliente:
            print("❌ Cliente no encontrado en BD")
            return False
        
        print(f"✅ Cliente encontrado: ID={cliente['id']}, Nombre={cliente['nombre']}")
        
        # Buscar pedidos del cliente
        cursor.execute("SELECT * FROM pedidos WHERE cliente_id = %s ORDER BY fecha_pedido DESC LIMIT 1", (cliente['id'],))
        pedido = cursor.fetchone()
        
        if not pedido:
            print("❌ Pedido no encontrado en BD")
            return False
        
        print(f"✅ Pedido encontrado: ID={pedido['id']}, Total=S/{pedido['total']}, Fecha={pedido['fecha_entrega']}")
        
        # Buscar items del pedido
        cursor.execute("SELECT pi.*, p.nombre as producto_nombre FROM pedido_items pi JOIN productos p ON pi.producto_id = p.id WHERE pedido_id = %s", (pedido['id'],))
        items = cursor.fetchall()
        
        if not items:
            print("❌ Items del pedido no encontrados en BD")
            return False
        
        print(f"✅ Items del pedido encontrados:")
        for item in items:
            print(f"   • {item['cantidad']}x {item['producto_nombre']} - S/{item['precio_unitario']} c/u")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando BD: {e}")
        return False

def test_guardado_bd():
    """Test completo de guardado en base de datos"""
    
    print("💾 TEST: GUARDADO EN BASE DE DATOS")
    print("=" * 50)
    
    # Usar un teléfono único para este test
    telefono_test = f"999{datetime.now().strftime('%H%M%S')}"
    session_id = f"test-bd-{telefono_test}"
    
    print(f"📱 Teléfono de prueba: {telefono_test}")
    
    # 1. Configurar pedido completo
    print("\n🛠️ Configurando pedido completo...")
    
    # Productos
    requests.post(WEBHOOK_URL, json={
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.productos"},
            "parameters": {"producto": ["baguette", "alfajor"], "cantidad": [2, 3]},
            "queryText": "Quiero 2 baguettes y 3 alfajores"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    # Nombre
    requests.post(WEBHOOK_URL, json={
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.nombre"},
            "parameters": {"person": {"name": "Cliente BD Test"}},
            "queryText": "Mi nombre es Cliente BD Test"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    # Fecha
    requests.post(WEBHOOK_URL, json={
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.fecha"},
            "parameters": {"date": "mañana"},
            "queryText": "Para mañana"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    # Delivery
    requests.post(WEBHOOK_URL, json={
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.delivery"},
            "parameters": {"tipo_entrega": "delivery"},
            "queryText": "Con delivery"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    # Dirección
    requests.post(WEBHOOK_URL, json={
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.direccion"},
            "parameters": {"direccion": "Av. Base de Datos 123"},
            "queryText": "Av. Base de Datos 123"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    # Notas
    requests.post(WEBHOOK_URL, json={
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.nota"},
            "parameters": {"notas": "Test de guardado en BD"},
            "queryText": "Test de guardado en BD"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    # Teléfono
    response_tel = requests.post(WEBHOOK_URL, json={
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.telefono"},
            "parameters": {"phone-number": telefono_test},
            "queryText": f"Mi teléfono es {telefono_test}"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    print("📋 Resumen generado correctamente")
    
    # 2. CONFIRMAR PEDIDO (esto debería guardar en BD)
    print("\n✅ CONFIRMANDO PEDIDO...")
    response_confirm = requests.post(WEBHOOK_URL, json={
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.confirmar"},
            "parameters": {},
            "queryText": "sí, confirmo"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    confirmacion = response_confirm.json().get('fulfillmentText', '')
    print(f"📬 Respuesta de confirmación recibida")
    
    if "confirmado" in confirmacion:
        print("✅ Confirmación exitosa por webhook")
        
        # 3. VERIFICAR EN BASE DE DATOS
        print("\n🔍 VERIFICANDO EN BASE DE DATOS...")
        if verificar_pedido_en_bd(f"+51{telefono_test}"):  # El webhook formatea el teléfono
            print("\n🎉 ¡ÉXITO TOTAL! El pedido se guardó correctamente en la base de datos")
        else:
            print("\n❌ FALLO: El pedido no se guardó en la base de datos")
    else:
        print("❌ Error en confirmación por webhook")
    
    print(f"\n📋 Confirmación completa:\n{confirmacion}")

if __name__ == "__main__":
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor webhook funcionando")
            test_guardado_bd()
        else:
            print("❌ Servidor webhook no responde")
    except:
        print("❌ No se puede conectar al servidor webhook")
        print("Por favor asegúrate de que el servidor esté corriendo")
