#!/usr/bin/env python3
"""
Test de fecha sin validaciones
"""
import requests

WEBHOOK_URL = "http://localhost:5000/webhook"

def test_fecha_sin_validaciones():
    """Probar diferentes formatos de fecha sin validaciones"""
    
    print("📅 TEST DE FECHA SIN VALIDACIONES")
    print("=" * 50)
    
    fechas_test = [
        "mañana",
        "pasado mañana", 
        "el lunes",
        "este fin de semana",
        "la próxima semana",
        "2025-07-10",
        "10 de julio",
        "hoy mismo",
        "en 3 días"
    ]
    
    for i, fecha in enumerate(fechas_test, 1):
        print(f"\n{i}️⃣ Probando fecha: '{fecha}'")
        
        payload = {
            "queryResult": {
                "intent": {"displayName": "hacer.pedido.fecha"},
                "parameters": {"date": fecha},
                "queryText": f"Para {fecha}"
            },
            "session": f"projects/test/agent/sessions/fecha-test-{i}"
        }
        
        response = requests.post(WEBHOOK_URL, json=payload)
        result = response.json()
        
        print(f"📬 Respuesta: {result.get('fulfillmentText', 'Sin respuesta')}")
        print(f"🔢 Status: {response.status_code}")

def test_fecha_con_query_text():
    """Probar captura desde queryText"""
    
    print("\n" + "="*50)
    print("🗣️ TEST CON SOLO TEXTO DE USUARIO")
    print("="*50)
    
    payload = {
        "queryResult": {
            "intent": {"displayName": "hacer.pedido.fecha"},
            "parameters": {},
            "queryText": "Para el viernes que viene por favor"
        },
        "session": "projects/test/agent/sessions/fecha-texto"
    }
    
    response = requests.post(WEBHOOK_URL, json=payload)
    result = response.json()
    
    print(f"📝 Texto del usuario: 'Para el viernes que viene por favor'")
    print(f"📬 Respuesta: {result.get('fulfillmentText', 'Sin respuesta')}")
    print(f"🔢 Status: {response.status_code}")

if __name__ == "__main__":
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor webhook funcionando")
            test_fecha_sin_validaciones()
            test_fecha_con_query_text()
        else:
            print("❌ Servidor webhook no responde")
    except:
        print("❌ No se puede conectar al servidor webhook")
