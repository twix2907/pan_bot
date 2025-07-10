#!/usr/bin/env python3
"""
Test específico con fecha 'hoy' que antes no se aceptaba
"""
import requests

WEBHOOK_URL = "http://localhost:5000/webhook"

def test_confirmacion_fecha_hoy():
    """Test completo con fecha 'hoy'"""
    
    print("📅 TEST: CONFIRMACIÓN CON FECHA 'HOY'")
    print("=" * 50)
    
    session_id = "test-fecha-hoy"
    
    # Configurar pedido completo con fecha 'hoy'
    print("🛠️ Configurando pedido con fecha 'hoy'...")
    
    # Productos
    requests.post(WEBHOOK_URL, json={
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.productos"},
            "parameters": {"producto": "alfajor", "cantidad": 2},
            "queryText": "Quiero 2 alfajores"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    # Nombre
    requests.post(WEBHOOK_URL, json={
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.nombre"},
            "parameters": {"person": {"name": "Cliente Urgente"}},
            "queryText": "Mi nombre es Cliente Urgente"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    # Fecha HOY (que antes no se aceptaba)
    print("📅 Agregando fecha 'hoy'...")
    response_fecha = requests.post(WEBHOOK_URL, json={
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.fecha"},
            "parameters": {"date": "hoy"},
            "queryText": "Lo necesito para hoy"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    fecha_respuesta = response_fecha.json().get('fulfillmentText', '')
    print(f"Respuesta fecha: {fecha_respuesta}")
    
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
            "parameters": {"direccion": "Calle Urgente 123"},
            "queryText": "Calle Urgente 123"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    # Teléfono
    response_tel = requests.post(WEBHOOK_URL, json={
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.telefono"},
            "parameters": {"phone-number": "999888777"},
            "queryText": "Mi teléfono es 999888777"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    print("\n📋 RESUMEN CON FECHA 'HOY':")
    print(response_tel.json().get('fulfillmentText', ''))
    
    # CONFIRMAR PEDIDO CON FECHA 'HOY'
    print("\n✅ CONFIRMANDO PEDIDO CON FECHA 'HOY'...")
    response_confirm = requests.post(WEBHOOK_URL, json={
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.confirmar"},
            "parameters": {},
            "queryText": "sí, confirmo"
        },
        "session": f"projects/test/agent/sessions/{session_id}"
    })
    
    confirmacion = response_confirm.json().get('fulfillmentText', '')
    
    if "anticipación" in confirmacion or "debe ser" in confirmacion:
        print("❌ FALLÓ: Todavía valida la fecha en confirmación")
        print(f"Respuesta: {confirmacion}")
    else:
        print("✅ ÉXITO: Pedido confirmado sin validar fecha 'hoy'")
        if "confirmado" in confirmacion and "hoy" in confirmacion:
            print("🎉 Confirmación exitosa con fecha 'hoy'!")
        print(f"\n📋 Confirmación completa:\n{confirmacion}")

if __name__ == "__main__":
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor webhook funcionando")
            test_confirmacion_fecha_hoy()
        else:
            print("❌ Servidor webhook no responde")
    except:
        print("❌ No se puede conectar al servidor webhook")
