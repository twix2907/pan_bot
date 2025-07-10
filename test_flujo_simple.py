#!/usr/bin/env python3
"""
Prueba simple del flujo del webhook
"""
import requests
import json
import time

WEBHOOK_URL = "http://localhost:5000/webhook"

def test_intent(intent_name, parameters, session_id="test-session-123"):
    """Función helper para testear un intent"""
    payload = {
        "queryResult": {
            "intent": {
                "displayName": intent_name
            },
            "parameters": parameters,
            "queryText": "texto de prueba"
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        return {
            "status": response.status_code,
            "data": response.json(),
            "text": response.json().get('fulfillmentText', 'Sin respuesta')
        }
    except Exception as e:
        return {"error": str(e)}

def main():
    """Prueba simple del flujo completo"""
    print("🧪 PRUEBA SIMPLE DEL FLUJO")
    print("=" * 50)
    
    # Test 1: Consultar categorías
    print("\n1️⃣ Consultando categorías...")
    result = test_intent("consultar.productos.categoria", {})
    print(f"Respuesta: {result.get('text', result)}")
    
    # Test 2: Agregar nombre
    print("\n2️⃣ Agregando nombre...")
    result = test_intent("hacer.pedido.nombre", {"person": {"name": "Ana García"}})
    print(f"Respuesta: {result.get('text', result)}")
    
    # Test 3: Agregar fecha
    print("\n3️⃣ Agregando fecha...")
    result = test_intent("hacer.pedido.fecha", {"date": "2025-07-11"})
    print(f"Respuesta: {result.get('text', result)}")
    
    # Test 4: Elegir delivery
    print("\n4️⃣ Eligiendo delivery...")
    result = test_intent("hacer.pedido.delivery", {"tipo_entrega": "delivery"})
    print(f"Respuesta: {result.get('text', result)}")
    
    # Test 5: Agregar dirección (usando queryText)
    print("\n5️⃣ Agregando dirección...")
    payload = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.direccion"},
            "parameters": {},
            "queryText": "Av. Los Olivos 123, San Isidro"
        },
        "session": "projects/test-project/agent/sessions/test-session-123"
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        result = response.json()
        print(f"Respuesta: {result.get('fulfillmentText', result)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 6: Agregar teléfono
    print("\n6️⃣ Agregando teléfono...")
    result = test_intent("hacer.pedido.telefono", {"phone-number": "987654321"})
    print(f"Respuesta: {result.get('text', result)}")
    
    print("\n✅ PRUEBA COMPLETADA!")

if __name__ == "__main__":
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor webhook funcionando")
            main()
        else:
            print("❌ Servidor webhook no responde correctamente")
    except:
        print("❌ No se puede conectar al servidor webhook")
        print("Por favor asegúrate de que el servidor esté corriendo en http://localhost:5000")
