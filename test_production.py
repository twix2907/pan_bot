import requests
import json

def test_production_app(base_url):
    """
    Prueba la aplicación en producción (Railway)
    """
    print(f"🚀 Probando aplicación en: {base_url}")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Health Check
    print("🔍 Test 1: Health Check...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check OK: {data['message']}")
            tests_passed += 1
        else:
            print(f"❌ Health check falló: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en health check: {e}")
    
    print()
    
    # Test 2: Database Connection
    print("🔍 Test 2: Conexión a Base de Datos...")
    try:
        response = requests.get(f"{base_url}/test-db")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Base de datos OK: {data['message']}")
            tests_passed += 1
        else:
            print(f"❌ Test BD falló: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en test BD: {e}")
    
    print()
    
    # Test 3: Productos
    print("🔍 Test 3: Consulta de Productos...")
    try:
        response = requests.get(f"{base_url}/productos/pan_dulce")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Productos OK: {len(data['productos'])} productos de pan dulce")
            tests_passed += 1
        else:
            print(f"❌ Test productos falló: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en test productos: {e}")
    
    print()
    
    # Test 4: Webhook Dialogflow
    print("🔍 Test 4: Webhook Dialogflow...")
    webhook_data = {
        "queryResult": {
            "intent": {
                "displayName": "consultar.productos.categoria"
            },
            "parameters": {
                "categoria": "pasteles"
            },
            "queryText": "quiero ver pasteles"
        }
    }
    
    try:
        response = requests.post(
            f"{base_url}/webhook",
            json=webhook_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Webhook OK - Respuesta: {data.get('fulfillmentText', '')[:100]}...")
            tests_passed += 1
        else:
            print(f"❌ Webhook falló: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en webhook: {e}")
    
    print("\n" + "=" * 60)
    print(f"🏁 Resultado: {tests_passed}/{total_tests} pruebas pasaron")
    
    if tests_passed == total_tests:
        print("🎉 ¡APLICACIÓN FUNCIONANDO PERFECTAMENTE EN PRODUCCIÓN!")
        print("\n📋 SIGUIENTE PASO: Configurar Dialogflow")
        print("   1. Crear proyecto en Google Cloud")
        print("   2. Configurar Dialogflow ES")
        print("   3. Configurar webhook URL")
        print(f"   4. URL del webhook: {base_url}/webhook")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisar logs de Railway.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    # Cambiar esta URL por la URL real de Railway
    RAILWAY_URL = input("Ingresa la URL de tu aplicación en Railway: ").strip()
    
    if not RAILWAY_URL.startswith('http'):
        RAILWAY_URL = f"https://{RAILWAY_URL}"
    
    test_production_app(RAILWAY_URL)
