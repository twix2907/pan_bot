#!/usr/bin/env python3
"""
Prueba específica de captura de productos
"""
import requests
import json

WEBHOOK_URL = "http://localhost:5000/webhook"

def test_productos():
    """Prueba específica para la captura de productos"""
    
    print("🛍️ PROBANDO CAPTURA DE PRODUCTOS")
    print("=" * 50)
    
    # Test 1: Productos con cantidades
    print("\n1️⃣ Test: Productos con cantidades específicas")
    payload1 = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.productos"},
            "parameters": {
                "producto": ["pan francés", "croissant"], 
                "cantidad": [2, 3]
            },
            "queryText": "Quiero 2 panes franceses y 3 croissants"
        },
        "session": "projects/test-project/agent/sessions/productos-test-1"
    }
    
    response1 = requests.post(WEBHOOK_URL, json=payload1)
    result1 = response1.json()
    print(f"📋 Parámetros: {payload1['queryResult']['parameters']}")
    print(f"📬 Respuesta: {result1.get('fulfillmentText', 'Sin respuesta')}")
    print(f"🔢 Status: {response1.status_code}")
    
    # Test 2: Un solo producto
    print("\n2️⃣ Test: Un solo producto")
    payload2 = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.productos"},
            "parameters": {
                "producto": "torta de chocolate",
                "cantidad": 1
            },
            "queryText": "Quiero una torta de chocolate"
        },
        "session": "projects/test-project/agent/sessions/productos-test-2"
    }
    
    response2 = requests.post(WEBHOOK_URL, json=payload2)
    result2 = response2.json()
    print(f"📋 Parámetros: {payload2['queryResult']['parameters']}")
    print(f"📬 Respuesta: {result2.get('fulfillmentText', 'Sin respuesta')}")
    print(f"🔢 Status: {response2.status_code}")
    
    # Test 3: Productos sin cantidad explícita
    print("\n3️⃣ Test: Productos sin cantidad")
    payload3 = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.productos"},
            "parameters": {
                "producto": ["baguette", "empanada"]
            },
            "queryText": "Quiero baguette y empanada"
        },
        "session": "projects/test-project/agent/sessions/productos-test-3"
    }
    
    response3 = requests.post(WEBHOOK_URL, json=payload3)
    result3 = response3.json()
    print(f"📋 Parámetros: {payload3['queryResult']['parameters']}")
    print(f"📬 Respuesta: {result3.get('fulfillmentText', 'Sin respuesta')}")
    print(f"🔢 Status: {response3.status_code}")
    
    # Test 4: Solo con queryText
    print("\n4️⃣ Test: Solo texto sin parámetros")
    payload4 = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.productos"},
            "parameters": {},
            "queryText": "Quiero 5 panes franceses y 2 tortas"
        },
        "session": "projects/test-project/agent/sessions/productos-test-4"
    }
    
    response4 = requests.post(WEBHOOK_URL, json=payload4)
    result4 = response4.json()
    print(f"📋 Parámetros: {payload4['queryResult']['parameters']}")
    print(f"📬 Respuesta: {result4.get('fulfillmentText', 'Sin respuesta')}")
    print(f"🔢 Status: {response4.status_code}")

def test_flujo_con_productos():
    """Prueba del flujo completo incluyendo productos reales"""
    
    print("\n" + "="*60)
    print("🔄 FLUJO COMPLETO CON PRODUCTOS")
    print("="*60)
    
    session_id = "flujo-completo-productos"
    
    # 1. Agregar productos
    print("\n1️⃣ Agregando productos...")
    payload_productos = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.productos"},
            "parameters": {
                "producto": ["pan integral", "medialunas"],
                "cantidad": [3, 6]
            },
            "queryText": "Quiero 3 panes integrales y 6 medialunas"
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    response = requests.post(WEBHOOK_URL, json=payload_productos)
    print(f"Respuesta: {response.json().get('fulfillmentText', 'Sin respuesta')}")
    
    # 2. Agregar nombre
    print("\n2️⃣ Agregando nombre...")
    payload_nombre = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.nombre"},
            "parameters": {"person": {"name": "Carlos Mendoza"}},
            "queryText": "Mi nombre es Carlos Mendoza"
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    response = requests.post(WEBHOOK_URL, json=payload_nombre)
    print(f"Respuesta: {response.json().get('fulfillmentText', 'Sin respuesta')}")
    
    # 3. Agregar teléfono para ver resumen
    print("\n3️⃣ Agregando teléfono para ver resumen...")
    payload_telefono = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.telefono"},
            "parameters": {"phone-number": "999888777"},
            "queryText": "Mi teléfono es 999888777"
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    response = requests.post(WEBHOOK_URL, json=payload_telefono)
    print(f"Respuesta: {response.json().get('fulfillmentText', 'Sin respuesta')}")

if __name__ == "__main__":
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor webhook funcionando")
            test_productos()
            test_flujo_con_productos()
        else:
            print("❌ Servidor webhook no responde correctamente")
    except:
        print("❌ No se puede conectar al servidor webhook")
        print("Por favor asegúrate de que el servidor esté corriendo en http://localhost:5000")
