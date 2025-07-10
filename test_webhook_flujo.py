#!/usr/bin/env python3
"""
Script de prueba para verificar el flujo completo del webhook
con storage temporal por sesión
"""

import requests
import json
import time

# URL del webhook (ajustar si es necesario)
WEBHOOK_URL = "http://localhost:5000/webhook"

def test_request(intent_name, parameters, session_id="test-session-123", query_text=""):
    """Envía una request simulada al webhook"""
    
    payload = {
        "queryResult": {
            "intent": {
                "displayName": intent_name
            },
            "parameters": parameters,
            "queryText": query_text
        },
        "session": f"projects/test-project/agent/sessions/{session_id}"
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        result = response.json()
        print(f"\n{'='*60}")
        print(f"INTENT: {intent_name}")
        print(f"PARAMS: {parameters}")
        print(f"RESPONSE: {result.get('fulfillmentText', 'No response')}")
        print(f"STATUS: {response.status_code}")
        return result
    except Exception as e:
        print(f"ERROR enviando request para {intent_name}: {e}")
        return None

def test_flujo_completo():
    """Prueba el flujo completo de un pedido"""
    
    print("🚀 INICIANDO PRUEBA DEL FLUJO COMPLETO DEL WEBHOOK")
    session_id = "test-session-" + str(int(time.time()))
    
    # 1. Consultar productos por categoría
    print("\n1️⃣ Consultando productos de panes...")
    test_request("consultar.productos.categoria", 
                {"categoria_producto": "panes"}, 
                session_id, 
                "quiero ver panes")
    
    # 2. Agregar productos al pedido
    print("\n2️⃣ Agregando productos al pedido...")
    test_request("hacer.pedido.productos", 
                {"producto": ["pan francés", "croissant"], "cantidad": [2, 3]}, 
                session_id, 
                "quiero 2 panes francés y 3 croissant")
    
    # 3. Agregar nombre
    print("\n3️⃣ Agregando nombre...")
    test_request("hacer.pedido.nombre", 
                {"person": {"name": "Juan Pérez"}}, 
                session_id, 
                "mi nombre es Juan Pérez")
    
    # 4. Agregar fecha
    print("\n4️⃣ Agregando fecha...")
    test_request("hacer.pedido.fecha", 
                {"date": "2025-07-11"}, 
                session_id, 
                "para el 11 de julio")
    
    # 5. Tipo de entrega - delivery
    print("\n5️⃣ Seleccionando delivery...")
    test_request("hacer.pedido.delivery", 
                {"tipo_entrega": "delivery"}, 
                session_id, 
                "quiero delivery")
    
    # 6. Agregar dirección
    print("\n6️⃣ Agregando dirección...")
    test_request("hacer.pedido.direccion", 
                {"direccion": "Av. Los Olivos 123, San Isidro"}, 
                session_id, 
                "mi dirección es Av. Los Olivos 123, San Isidro")
    
    # 7. Agregar notas
    print("\n7️⃣ Agregando notas especiales...")
    test_request("hacer.pedido.nota", 
                {"notas": "Sin gluten por favor"}, 
                session_id, 
                "sin gluten por favor")
    
    # 8. Agregar teléfono
    print("\n8️⃣ Agregando teléfono...")
    test_request("hacer.pedido.telefono", 
                {"phone-number": "987654321"}, 
                session_id, 
                "mi teléfono es 987654321")
    
    # 9. Confirmar pedido
    print("\n9️⃣ Confirmando pedido...")
    test_request("hacer.pedido.confirmar", 
                {}, 
                session_id, 
                "sí confirmo")
    
    print("\n✅ PRUEBA COMPLETADA!")

def test_flujo_con_recojo():
    """Prueba un flujo alternativo con recojo en tienda"""
    
    print("\n\n🚀 INICIANDO PRUEBA CON RECOJO EN TIENDA")
    session_id = "test-recojo-" + str(int(time.time()))
    
    # Productos
    test_request("hacer.pedido.productos", 
                {"producto": ["torta chocolate"], "cantidad": [1]}, 
                session_id, 
                "quiero 1 torta de chocolate")
    
    # Nombre
    test_request("hacer.pedido.nombre", 
                {"person": {"name": "María González"}}, 
                session_id, 
                "soy María González")
    
    # Fecha
    test_request("hacer.pedido.fecha", 
                {"date": "2025-07-12"}, 
                session_id, 
                "para mañana")
    
    # Recojo
    test_request("hacer.pedido.recojo", 
                {"tipo_entrega": "recojo"}, 
                session_id, 
                "voy a recoger en tienda")
    
    # Teléfono
    test_request("hacer.pedido.telefono", 
                {"phone-number": "999888777"}, 
                session_id, 
                "mi número es 999888777")
    
    # Confirmar
    test_request("hacer.pedido.confirmar", 
                {}, 
                session_id, 
                "confirmo el pedido")
    
    print("\n✅ PRUEBA DE RECOJO COMPLETADA!")

if __name__ == "__main__":
    print("Esperando 2 segundos para que el servidor esté listo...")
    time.sleep(2)
    
    try:
        # Verificar que el servidor esté funcionando
        health_response = requests.get("http://localhost:5000/", timeout=5)
        if health_response.status_code == 200:
            print("✅ Servidor webhook funcionando correctamente")
            
            # Ejecutar pruebas
            test_flujo_completo()
            test_flujo_con_recojo()
            
        else:
            print("❌ Servidor webhook no responde correctamente")
            
    except Exception as e:
        print(f"❌ Error conectando con el servidor: {e}")
        print("Asegúrate de que el webhook esté ejecutándose en http://localhost:5000")
