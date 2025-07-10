#!/usr/bin/env python3
"""
Debug de captura de dirección
"""
import requests
import json

WEBHOOK_URL = "http://localhost:5000/webhook"

def test_direccion_debug():
    """Prueba específica para debuggear la captura de dirección"""
    
    session_id = "debug-session-123"
    
    # Primero configuramos el flujo hasta llegar a la dirección
    print("🔧 CONFIGURANDO FLUJO HASTA DIRECCIÓN...")
    
    # 1. Nombre
    payload1 = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.nombre"},
            "parameters": {"person": {"name": "Test User"}},
            "queryText": "Mi nombre es Test User"
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    response1 = requests.post(WEBHOOK_URL, json=payload1)
    print(f"1. Nombre: {response1.json().get('fulfillmentText', '')}")
    
    # 2. Fecha
    payload2 = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.fecha"},
            "parameters": {"date": "2025-07-11"},
            "queryText": "Para el 11 de julio"
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    response2 = requests.post(WEBHOOK_URL, json=payload2)
    print(f"2. Fecha: {response2.json().get('fulfillmentText', '')}")
    
    # 3. Delivery
    payload3 = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.delivery"},
            "parameters": {"tipo_entrega": "delivery"},
            "queryText": "Prefiero delivery"
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    response3 = requests.post(WEBHOOK_URL, json=payload3)
    print(f"3. Delivery: {response3.json().get('fulfillmentText', '')}")
    
    print("\n" + "="*50)
    print("🏠 PROBANDO DIFERENTES FORMAS DE CAPTURAR DIRECCIÓN...")
    
    # Test 1: Con parámetro direccion
    print("\n📍 Test 1: Con parámetro 'direccion'")
    payload_dir1 = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.direccion"},
            "parameters": {"direccion": "Av. Los Olivos 123, San Isidro"},
            "queryText": "Av. Los Olivos 123, San Isidro"
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    response_dir1 = requests.post(WEBHOOK_URL, json=payload_dir1)
    print(f"Respuesta: {response_dir1.json().get('fulfillmentText', '')}")
    print(f"Status: {response_dir1.status_code}")
    
    # Test 2: Con parámetro direccion_entrega
    print("\n📍 Test 2: Con parámetro 'direccion_entrega'")
    payload_dir2 = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.direccion"},
            "parameters": {"direccion_entrega": "Calle Las Flores 456"},
            "queryText": "Calle Las Flores 456"
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    response_dir2 = requests.post(WEBHOOK_URL, json=payload_dir2)
    print(f"Respuesta: {response_dir2.json().get('fulfillmentText', '')}")
    print(f"Status: {response_dir2.status_code}")
    
    # Test 3: Solo con queryText (sin parámetros)
    print("\n📍 Test 3: Solo con queryText")
    payload_dir3 = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.direccion"},
            "parameters": {},
            "queryText": "Jr. Independencia 789, Lima"
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    response_dir3 = requests.post(WEBHOOK_URL, json=payload_dir3)
    print(f"Respuesta: {response_dir3.json().get('fulfillmentText', '')}")
    print(f"Status: {response_dir3.status_code}")
    
    # Test 4: Con diferentes parámetros que Dialogflow podría usar
    print("\n📍 Test 4: Con parámetros alternativos")
    payload_dir4 = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.direccion"},
            "parameters": {
                "location": "Av. Universitaria 321",
                "address": "Av. Universitaria 321",
                "geo-city": "Lima",
                "street-address": "Av. Universitaria 321"
            },
            "queryText": "Av. Universitaria 321"
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    response_dir4 = requests.post(WEBHOOK_URL, json=payload_dir4)
    print(f"Respuesta: {response_dir4.json().get('fulfillmentText', '')}")
    print(f"Status: {response_dir4.status_code}")

if __name__ == "__main__":
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor webhook funcionando")
            test_direccion_debug()
        else:
            print("❌ Servidor webhook no responde correctamente")
    except:
        print("❌ No se puede conectar al servidor webhook")
        print("Por favor asegúrate de que el servidor esté corriendo en http://localhost:5000")
