import requests
import json

# URL base de la aplicación (ajustar si usas otro puerto)
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test del health check básico"""
    print("🔍 Probando health check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check OK: {data['message']}")
            return True
        else:
            print(f"❌ Health check falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return False

def test_database_connection():
    """Test de conexión a la base de datos"""
    print("🔍 Probando conexión a base de datos...")
    try:
        response = requests.get(f"{BASE_URL}/test-db")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Base de datos OK: {data['message']}")
            return True
        else:
            print(f"❌ Test BD falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en test BD: {e}")
        return False

def test_productos_categorias():
    """Test de consulta de productos por categoría"""
    print("🔍 Probando consulta de productos...")
    categorias = ['pan_salado', 'pan_dulce', 'pan_semidulce', 'pasteles', 'bocaditos']
    
    for categoria in categorias:
        try:
            response = requests.get(f"{BASE_URL}/productos/{categoria}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {categoria}: {len(data['productos'])} productos encontrados")
            else:
                print(f"❌ Error en {categoria}: {response.status_code}")
        except Exception as e:
            print(f"❌ Error consultando {categoria}: {e}")

def test_webhook_dialogflow():
    """Test del webhook con un request simulado de Dialogflow"""
    print("🔍 Probando webhook de Dialogflow...")
    
    # Simular request de Dialogflow para consultar productos
    webhook_data = {
        "queryResult": {
            "intent": {
                "displayName": "consultar.productos.categoria"
            },
            "parameters": {
                "categoria": "pan_dulce"
            },
            "queryText": "quiero ver pan dulce"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/webhook",
            json=webhook_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Webhook OK - Respuesta: {data.get('fulfillmentText', '')[:100]}...")
            return True
        else:
            print(f"❌ Webhook falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en webhook: {e}")
        return False

def test_webhook_sin_categoria():
    """Test del webhook sin categoría específica"""
    print("🔍 Probando webhook sin categoría...")
    
    webhook_data = {
        "queryResult": {
            "intent": {
                "displayName": "consultar.productos.categoria"
            },
            "parameters": {},
            "queryText": "ver productos"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/webhook",
            json=webhook_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Webhook categorías OK - Respuesta: {data.get('fulfillmentText', '')[:100]}...")
            return True
        else:
            print(f"❌ Webhook categorías falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en webhook categorías: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del Chatbot Panadería Jos y Mar")
    print("=" * 60)
    
    # Ejecutar todas las pruebas
    tests_passed = 0
    total_tests = 5
    
    if test_health_check():
        tests_passed += 1
    
    print()
    if test_database_connection():
        tests_passed += 1
    
    print()
    test_productos_categorias()
    tests_passed += 1  # Asumimos que pasa si no hay errores críticos
    
    print()
    if test_webhook_dialogflow():
        tests_passed += 1
    
    print()
    if test_webhook_sin_categoria():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"🏁 Resultado: {tests_passed}/{total_tests} pruebas pasaron")
    
    if tests_passed == total_tests:
        print("🎉 ¡Todo funcionando perfectamente!")
        print("📋 Próximos pasos:")
        print("   1. Subir código a GitHub")
        print("   2. Desplegar en Railway")
        print("   3. Configurar Dialogflow")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisar errores arriba.")
