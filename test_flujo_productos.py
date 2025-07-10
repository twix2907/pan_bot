#!/usr/bin/env python3
"""
Test simple del flujo de productos para verificar que funciona antes del deploy
"""

import requests
import json

# URL del webhook local
WEBHOOK_URL = "http://localhost:5000/webhook"

def test_productos_flow():
    """
    Simula el flujo de agregar productos y luego el teléfono
    """
    
    # Simular session ID
    session_id = "test-session-12345"
    
    # 1. Simular intent de productos
    print("🧪 Test 1: Agregando productos...")
    
    productos_request = {
        "responseId": "test-response-1",
        "queryResult": {
            "queryText": "quiero 2 baguettes y 1 torta de chocolate",
            "action": "hacer.pedido.productos",
            "parameters": {
                "producto": ["baguette", "torta de chocolate"],
                "number": [2, 1]
            },
            "allRequiredParamsPresent": True,
            "intent": {
                "displayName": "hacer.pedido.productos"
            }
        },
        "session": f"projects/panaderiajosymar/agent/sessions/{session_id}"
    }
    
    response = requests.post(WEBHOOK_URL, json=productos_request)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Respuesta productos: {result.get('fulfillmentText', 'Sin texto')[:100]}...")
    else:
        print(f"❌ Error en productos: {response.text}")
        return False
    
    # 2. Verificar que los productos se guardaron
    print("\n🧪 Test 2: Verificando sesiones...")
    
    debug_response = requests.get("http://localhost:5000/debug/sesiones")
    if debug_response.status_code == 200:
        sesiones = debug_response.json()
        print(f"Total sesiones: {sesiones['total_sesiones']}")
        if session_id in sesiones['sesiones']:
            productos_count = sesiones['sesiones'][session_id]['productos_count']
            print(f"✅ Productos en sesión {session_id}: {productos_count}")
        else:
            print(f"❌ Sesión {session_id} no encontrada")
            return False
    
    # 3. Simular intent de teléfono (debería mostrar productos en resumen)
    print("\n🧪 Test 3: Agregando teléfono...")
    
    telefono_request = {
        "responseId": "test-response-2",
        "queryResult": {
            "queryText": "987654321",
            "action": "hacer.pedido.telefono",
            "parameters": {
                "phone-number": "987654321"
            },
            "allRequiredParamsPresent": True,
            "outputContexts": [
                {
                    "name": f"projects/panaderiajosymar/agent/sessions/{session_id}/contexts/esperando_fecha",
                    "parameters": {
                        "person": {"name": "Test User"},
                        "date": "2025-07-10T12:00:00-05:00"
                    }
                }
            ],
            "intent": {
                "displayName": "hacer.pedido.telefono"
            }
        },
        "session": f"projects/panaderiajosymar/agent/sessions/{session_id}"
    }
    
    response = requests.post(WEBHOOK_URL, json=telefono_request)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        resumen = result.get('fulfillmentText', '')
        print(f"📋 Resumen generado:")
        print(resumen)
        
        # Verificar que el resumen contiene productos
        if "🛒 Productos:" in resumen and "baguette" in resumen:
            print("✅ El resumen contiene los productos correctamente!")
            return True
        else:
            print("❌ El resumen NO contiene los productos")
            return False
    else:
        print(f"❌ Error en teléfono: {response.text}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando test del flujo de productos...")
    
    # Verificar que el webhook está corriendo
    try:
        health = requests.get("http://localhost:5000/")
        if health.status_code != 200:
            print("❌ Webhook no está corriendo. Ejecuta: python webhook/app.py")
            exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al webhook. ¿Está corriendo en puerto 5000?")
        exit(1)
    
    print("✅ Webhook está corriendo\n")
    
    success = test_productos_flow()
    
    if success:
        print("\n🎉 ¡Todos los tests pasaron! El flujo está listo para deploy.")
    else:
        print("\n❌ Hay problemas en el flujo. Revisar antes del deploy.")
