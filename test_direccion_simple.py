#!/usr/bin/env python3
"""
Prueba simple de dirección
"""
import requests
import json

WEBHOOK_URL = "http://localhost:5000/webhook"

def test_direccion_simple():
    """Prueba super simple de dirección"""
    
    # Test directo con parámetro direccion
    payload = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.direccion"},
            "parameters": {"direccion": "Av. Los Olivos 123"},
            "queryText": "Av. Los Olivos 123"
        },
        "session": "projects/test-project/agent/sessions/test-123"
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        result = response.json()
        
        print("📋 PAYLOAD ENVIADO:")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        print("\n📬 RESPUESTA RECIBIDA:")
        print(f"Status: {response.status_code}")
        print(f"Texto: {result.get('fulfillmentText', 'Sin respuesta')}")
        
        # También probar con queryText
        print("\n" + "="*50)
        print("🔄 PROBANDO SOLO CON QUERYTEXT...")
        
        payload2 = {
            "queryResult": {
                "intent": {"displayName": "hacer.pedido.direccion"},
                "parameters": {},
                "queryText": "Mi dirección es Calle Las Flores 456"
            },
            "session": "projects/test-project/agent/sessions/test-456"
        }
        
        response2 = requests.post(WEBHOOK_URL, json=payload2, timeout=10)
        result2 = response2.json()
        
        print("📋 PAYLOAD ENVIADO:")
        print(json.dumps(payload2, indent=2, ensure_ascii=False))
        print("\n📬 RESPUESTA RECIBIDA:")
        print(f"Status: {response2.status_code}")
        print(f"Texto: {result2.get('fulfillmentText', 'Sin respuesta')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor webhook funcionando")
            test_direccion_simple()
        else:
            print("❌ Servidor webhook no responde correctamente")
    except:
        print("❌ No se puede conectar al servidor webhook")
        print("Por favor asegúrate de que el servidor esté corriendo en http://localhost:5000")
