"""
Script de prueba para verificar el flujo completo del chatbot con storage temporal por sesión
Panadería Jos y Mar - Flujo de Pedidos
"""

import requests
import json
import time

# URL del webhook local
WEBHOOK_URL = "http://localhost:5000/webhook"

def simular_request_dialogflow(intent_name, parameters={}, session_id="test-session-123"):
    """
    Simula un request de Dialogflow al webhook
    """
    payload = {
        "queryResult": {
            "intent": {
                "displayName": intent_name
            },
            "parameters": parameters,
            "queryText": ""
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    return payload

def test_flujo_completo():
    """
    Prueba el flujo completo de un pedido paso a paso
    """
    session_id = f"test-session-{int(time.time())}"
    
    print("🧪 INICIANDO TEST DEL FLUJO COMPLETO")
    print(f"📋 Session ID: {session_id}")
    print("=" * 60)
    
    # 1. Agregar productos
    print("\n1️⃣ PASO: Agregar productos")
    payload = simular_request_dialogflow(
        "hacer.pedido.productos",
        {
            "producto": ["baguette", "torta de chocolate"],
            "number": [2, 1]
        },
        session_id
    )
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        result = response.json()
        print(f"✅ Respuesta: {result.get('fulfillmentText', 'Sin respuesta')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    time.sleep(1)
    
    # 2. Agregar nombre
    print("\n2️⃣ PASO: Agregar nombre")
    payload = simular_request_dialogflow(
        "hacer.pedido.nombre",
        {
            "person": {"name": "Juan Pérez"}
        },
        session_id
    )
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        result = response.json()
        print(f"✅ Respuesta: {result.get('fulfillmentText', 'Sin respuesta')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    time.sleep(1)
    
    # 3. Agregar fecha
    print("\n3️⃣ PASO: Agregar fecha")
    payload = simular_request_dialogflow(
        "hacer.pedido.fecha",
        {
            "date": "mañana"
        },
        session_id
    )
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        result = response.json()
        print(f"✅ Respuesta: {result.get('fulfillmentText', 'Sin respuesta')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    time.sleep(1)
    
    # 4. Elegir delivery
    print("\n4️⃣ PASO: Elegir delivery")
    payload = simular_request_dialogflow(
        "hacer.pedido.delivery",
        {},
        session_id
    )
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        result = response.json()
        print(f"✅ Respuesta: {result.get('fulfillmentText', 'Sin respuesta')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    time.sleep(1)
    
    # 5. Agregar dirección
    print("\n5️⃣ PASO: Agregar dirección")
    payload = simular_request_dialogflow(
        "hacer.pedido.direccion",
        {
            "direccion_entrega": "Av. Larco 123, Miraflores"
        },
        session_id
    )
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        result = response.json()
        print(f"✅ Respuesta: {result.get('fulfillmentText', 'Sin respuesta')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    time.sleep(1)
    
    # 6. Agregar nota
    print("\n6️⃣ PASO: Agregar nota")
    payload = simular_request_dialogflow(
        "hacer.pedido.nota",
        {
            "notas": "Sin azúcar extra"
        },
        session_id
    )
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        result = response.json()
        print(f"✅ Respuesta: {result.get('fulfillmentText', 'Sin respuesta')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    time.sleep(1)
    
    # 7. Agregar teléfono
    print("\n7️⃣ PASO: Agregar teléfono")
    payload = simular_request_dialogflow(
        "hacer.pedido.telefono",
        {
            "phone-number": "987654321"
        },
        session_id
    )
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        result = response.json()
        print(f"✅ Respuesta: {result.get('fulfillmentText', 'Sin respuesta')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    time.sleep(1)
    
    # 8. Confirmar pedido
    print("\n8️⃣ PASO: Confirmar pedido")
    payload = simular_request_dialogflow(
        "hacer.pedido.confirmar",
        {},
        session_id
    )
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        result = response.json()
        print(f"✅ Respuesta: {result.get('fulfillmentText', 'Sin respuesta')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 TEST COMPLETADO")

def test_debug_sesiones():
    """
    Prueba el endpoint de debug para ver las sesiones activas
    """
    print("\n🔍 VERIFICANDO SESIONES ACTIVAS")
    try:
        response = requests.get("http://localhost:5000/debug/sesiones")
        result = response.json()
        print(f"📊 Total sesiones: {result.get('total_sesiones', 0)}")
        for session_id, data in result.get('sesiones', {}).items():
            print(f"  📋 Sesión: {session_id[:12]}...")
            print(f"    🛒 Productos: {data.get('productos_count', 0)}")
            print(f"    ⏰ Última actividad: {data.get('timestamp', '')}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🏪 PANADERÍA JOS Y MAR - TEST DEL SISTEMA DE STORAGE TEMPORAL")
    print("="*60)
    
    # Verificar que el webhook esté funcionando
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            print("✅ Webhook en funcionamiento")
        else:
            print("❌ Error: Webhook no responde")
            exit(1)
    except:
        print("❌ Error: No se puede conectar al webhook")
        print("💡 Asegúrate de ejecutar: python webhook/app.py")
        exit(1)
    
    # Ejecutar pruebas
    test_flujo_completo()
    test_debug_sesiones()
