#!/usr/bin/env python3
"""
Test simple y directo de confirmación
"""
import requests

WEBHOOK_URL = "http://localhost:5000/webhook"

def test_confirmacion_simple():
    """Test directo de confirmación"""
    
    print("🎯 TEST SIMPLE DE CONFIRMACIÓN")
    print("=" * 50)
    
    session_id = "test-confirmacion-simple"
    
    # 1. Crear pedido completo paso a paso
    print("🛠️ Configurando pedido...")
    
    # Productos
    requests.post(WEBHOOK_URL, json={
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.productos"},
            "parameters": {"producto": "baguette", "cantidad": 2},
            "queryText": "Quiero 2 baguettes"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    # Nombre
    requests.post(WEBHOOK_URL, json={
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.nombre"},
            "parameters": {"person": {"name": "Ana Test"}},
            "queryText": "Mi nombre es Ana Test"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    # Fecha
    requests.post(WEBHOOK_URL, json={
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.fecha"},
            "parameters": {"date": "2025-07-15"},
            "queryText": "Para el 15 de julio"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    # Recojo
    requests.post(WEBHOOK_URL, json={
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.recojo"},
            "parameters": {"tipo_entrega": "recojo"},
            "queryText": "Recojo en tienda"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    # Teléfono (debe mostrar resumen)
    response_tel = requests.post(WEBHOOK_URL, json={
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.telefono"},
            "parameters": {"phone-number": "987654321"},
            "queryText": "Mi teléfono es 987654321"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    print("📞 Resumen después del teléfono:")
    print(response_tel.json().get('fulfillmentText', ''))
    
    print("\n" + "="*50)
    print("✅ PROBANDO CONFIRMACIÓN...")
    
    # 2. CONFIRMAR PEDIDO
    response_confirm = requests.post(WEBHOOK_URL, json={
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.confirmar"},
            "parameters": {},
            "queryText": "sí"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    print("🎉 RESPUESTA DE CONFIRMACIÓN:")
    print(f"Status: {response_confirm.status_code}")
    print(f"Texto: {response_confirm.json().get('fulfillmentText', 'Sin respuesta')}")
    
    # Verificar si menciona número de pedido
    confirmacion_texto = response_confirm.json().get('fulfillmentText', '')
    if "pedido" in confirmacion_texto.lower() and "confirmado" in confirmacion_texto.lower():
        print("✅ Confirmación exitosa - se generó respuesta de pedido confirmado")
    else:
        print("⚠️ La confirmación no parece completa")

if __name__ == "__main__":
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor webhook funcionando")
            test_confirmacion_simple()
        else:
            print("❌ Servidor webhook no responde")
    except:
        print("❌ No se puede conectar al servidor webhook")
