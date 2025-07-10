#!/usr/bin/env python3
"""
Prueba final del flujo completo con productos reales
"""
import requests

WEBHOOK_URL = "http://localhost:5000/webhook"

def test_flujo_completo_real():
    """Flujo completo con productos que existen en la BD"""
    
    print("🎯 FLUJO COMPLETO CON PRODUCTOS REALES")
    print("=" * 50)
    
    session_id = "flujo-final-real"
    
    # 1. Productos reales
    print("1️⃣ Agregando productos reales...")
    payload1 = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.productos"},
            "parameters": {
                "producto": ["baguette", "alfajor", "torta de chocolate"],
                "cantidad": [2, 4, 1]
            },
            "queryText": "Quiero 2 baguettes, 4 alfajores y 1 torta de chocolate"
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    response = requests.post(WEBHOOK_URL, json=payload1)
    print(f"📦 Productos: {response.json().get('fulfillmentText', '')}")
    
    # 2. Nombre
    print("\n2️⃣ Agregando nombre...")
    payload2 = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.nombre"},
            "parameters": {"person": {"name": "María González"}},
            "queryText": "Mi nombre es María González"
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    response = requests.post(WEBHOOK_URL, json=payload2)
    print(f"👤 Nombre: {response.json().get('fulfillmentText', '')}")
    
    # 3. Fecha
    print("\n3️⃣ Agregando fecha...")
    payload3 = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.fecha"},
            "parameters": {"date": "2025-07-12"},
            "queryText": "Para mañana 12 de julio"
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    response = requests.post(WEBHOOK_URL, json=payload3)
    print(f"📅 Fecha: {response.json().get('fulfillmentText', '')}")
    
    # 4. Delivery
    print("\n4️⃣ Eligiendo delivery...")
    payload4 = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.delivery"},
            "parameters": {"tipo_entrega": "delivery"},
            "queryText": "Prefiero delivery"
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    response = requests.post(WEBHOOK_URL, json=payload4)
    print(f"🚚 Delivery: {response.json().get('fulfillmentText', '')}")
    
    # 5. Dirección
    print("\n5️⃣ Agregando dirección...")
    payload5 = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.direccion"},
            "parameters": {"direccion": "Av. Arequipa 2845, San Isidro"},
            "queryText": "Av. Arequipa 2845, San Isidro"
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    response = requests.post(WEBHOOK_URL, json=payload5)
    print(f"📍 Dirección: {response.json().get('fulfillmentText', '')}")
    
    # 6. Notas
    print("\n6️⃣ Agregando notas...")
    payload6 = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.nota"},
            "parameters": {"notas": "Por favor tocar el timbre 2 veces"},
            "queryText": "Por favor tocar el timbre 2 veces"
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    response = requests.post(WEBHOOK_URL, json=payload6)
    print(f"📝 Notas: {response.json().get('fulfillmentText', '')}")
    
    # 7. Teléfono (para ver resumen completo)
    print("\n7️⃣ Agregando teléfono...")
    payload7 = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.telefono"},
            "parameters": {"phone-number": "987123456"},
            "queryText": "Mi teléfono es 987123456"
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    response = requests.post(WEBHOOK_URL, json=payload7)
    print(f"📞 Teléfono y resumen:\n{response.json().get('fulfillmentText', '')}")

if __name__ == "__main__":
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor webhook funcionando")
            test_flujo_completo_real()
        else:
            print("❌ Servidor webhook no responde correctamente")
    except:
        print("❌ No se puede conectar al servidor webhook")
