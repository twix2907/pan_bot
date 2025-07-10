#!/usr/bin/env python3
"""
Test para ver productos disponibles en la BD
"""
import requests

WEBHOOK_URL = "http://localhost:5000/webhook"

def test_productos_disponibles():
    """Ver qué productos están disponibles"""
    
    print("🔍 CONSULTANDO PRODUCTOS DISPONIBLES EN LA BD")
    print("=" * 50)
    
    categorias = ["pan_salado", "pan_dulce", "panes_semidulces", "pasteles", "bocaditos"]
    
    for categoria in categorias:
        print(f"\n📁 Categoría: {categoria}")
        payload = {
            "queryResult": {
                "intent": {"displayName": "consultar.productos.categoria"},
                "parameters": {"categoria_producto": categoria},
                "queryText": f"¿Qué productos hay en {categoria}?"
            },
            "session": "projects/test-project/agent/sessions/consulta-productos"
        }
        
        try:
            response = requests.post(WEBHOOK_URL, json=payload)
            result = response.json()
            print(result.get('fulfillmentText', 'Sin respuesta'))
        except Exception as e:
            print(f"Error: {e}")

def test_productos_existentes():
    """Probar con productos que sabemos que existen"""
    
    print("\n" + "="*60)
    print("🛍️ PROBANDO CON PRODUCTOS QUE SÍ EXISTEN")
    print("="*60)
    
    # Basándonos en los resultados anteriores, sabemos que estos funcionan:
    productos_conocidos = [
        {"nombre": "torta de chocolate", "cantidad": 1},
        {"nombre": "baguette", "cantidad": 2}
    ]
    
    session_id = "test-productos-existentes"
    
    for i, producto in enumerate(productos_conocidos, 1):
        print(f"\n{i}️⃣ Agregando: {producto['cantidad']} {producto['nombre']}")
        
        payload = {
            "queryResult": {
                "intent": {"displayName": "hacer.pedido.productos"},
                "parameters": {
                    "producto": producto["nombre"],
                    "cantidad": producto["cantidad"]
                },
                "queryText": f"Quiero {producto['cantidad']} {producto['nombre']}"
            },
            "session": f"projects/test-project/agent/sessions/{session_id}"
        }
        
        response = requests.post(WEBHOOK_URL, json=payload)
        result = response.json()
        print(f"Respuesta: {result.get('fulfillmentText', 'Sin respuesta')}")

if __name__ == "__main__":
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor webhook funcionando")
            test_productos_disponibles()
            test_productos_existentes()
        else:
            print("❌ Servidor webhook no responde correctamente")
    except:
        print("❌ No se puede conectar al servidor webhook")
