# Plan de Pruebas - Chatbot Panadería Jos y Mar

## 🧪 Casos de Prueba Principales

### 1. Health Check y Conexión BD
```
✅ GET / → Respuesta 200 con status ok
✅ GET /test-db → Conexión exitosa a MySQL
✅ Verificar que todas las tablas existen
```

### 2. Consulta de Productos
```
✅ GET /productos/pan_salado → Lista de panes salados
✅ GET /productos/pan_dulce → Lista de panes dulces
✅ GET /productos/pasteles → Lista de pasteles
✅ Webhook consultar.productos.categoria → Respuesta formateada
```

### 3. Flujo de Pedidos (Webhook)
```
✅ Intent: registrar.cliente
   - Datos válidos → Cliente creado
   - Teléfono inválido → Error de validación
   - Cliente existente → Reutilizar ID

✅ Intent: hacer.pedido.confirmar
   - Todos los datos completos → Pedido creado
   - Fecha inválida → Error de validación
   - Tipo entrega inválido → Error de validación
```

### 4. Integración con Dialogflow
```
✅ Webhook recibe POST de Dialogflow
✅ Extrae intent y parámetros correctamente
✅ Devuelve respuesta en formato JSON correcto
✅ Maneja errores sin romper conversación
```

## 📋 Datos de Prueba

### Clientes de Prueba
```json
{
  "nombre": "Juan Pérez",
  "telefono": "+51999999999",
  "direccion": "Av. Test 123, Lima"
}
```

### Pedidos de Prueba
```json
{
  "fecha_entrega": "2025-01-11",
  "tipo_entrega": "delivery",
  "direccion_entrega": "Av. Test 123, Lima"
}
```

## 🔄 Tests Automatizados Básicos

### Script de Test Python (test_basic.py)
```python
import requests
import json

BASE_URL = "https://tu-app.railway.app"

def test_health():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_db_connection():
    response = requests.get(f"{BASE_URL}/test-db")
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_productos():
    response = requests.get(f"{BASE_URL}/productos/pan_salado")
    assert response.status_code == 200
    data = response.json()
    assert "productos" in data
    assert data["categoria"] == "pan_salado"

def test_webhook():
    webhook_data = {
        "queryResult": {
            "intent": {
                "displayName": "consultar.productos.categoria"
            },
            "parameters": {
                "categoria": "pan_dulce"
            }
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/webhook",
        json=webhook_data,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 200
    assert "fulfillmentText" in response.json()

if __name__ == "__main__":
    test_health()
    test_db_connection()
    test_productos()
    test_webhook()
    print("✅ Todos los tests pasaron")
```

## 📱 Tests de Dialogflow

### 1. Configurar Agent de Prueba
```
- Crear proyecto Dialogflow nuevo
- Configurar webhook URL
- Importar intents básicos
```

### 2. Tests de Conversación
```
Usuario: "Hola"
Bot: Mensaje de bienvenida con opciones

Usuario: "Ver productos"
Bot: Lista de categorías disponibles

Usuario: "Pan dulce"
Bot: Lista de productos de pan dulce

Usuario: "Hacer pedido"
Bot: Solicitud de datos del cliente
```

### 3. Validaciones
```
✅ Bot responde en menos de 3 segundos
✅ Mensajes son claros y bien formateados
✅ Errores se manejan graciosamente
✅ Fallback funciona correctamente
```

## 🔍 Checklist de Calidad

### Funcionalidad Básica
- [ ] Health check responde
- [ ] Conexión a BD funciona
- [ ] Consulta de productos por categoría
- [ ] Registro de clientes
- [ ] Creación de pedidos básicos

### Validaciones
- [ ] Números de teléfono válidos
- [ ] Fechas de entrega válidas
- [ ] Tipos de entrega válidos
- [ ] Manejo de datos faltantes

### Integración
- [ ] Webhook responde a Dialogflow
- [ ] Formato de respuestas correcto
- [ ] Logging funciona
- [ ] Errores se capturan

### Performance
- [ ] Respuestas en menos de 3 segundos
- [ ] No memory leaks evidentes
- [ ] Conexiones BD se cierran correctamente

## 📝 Reporte de Bugs

### Formato de Reporte
```
**Título**: Descripción breve del problema
**Pasos**: Como reproducir el error
**Esperado**: Qué debería pasar
**Actual**: Qué pasa realmente
**Logs**: Logs relevantes del error
**Prioridad**: Alta/Media/Baja
```

### Issues Conocidos
```
- Precios en 0.00 en datos de ejemplo
- Validación de productos en pedidos pendiente
- Integración con Twilio pendiente
```

## ✅ Criterios de Aceptación

### Para pasar a producción:
1. **Todos los tests básicos pasan**
2. **Webhook responde correctamente a Dialogflow**
3. **Base de datos funciona sin errores**
4. **Logging captura errores importantes**
5. **Documentación está actualizada**

### Performance mínima:
- Respuesta del webhook < 3 segundos
- Uptime > 99%
- Errores < 1% de requests
