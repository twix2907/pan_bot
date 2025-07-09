# Chatbot Panadería Jos y Mar

Chatbot para WhatsApp que permite a los clientes consultar productos y realizar pedidos, integrado con Dialogflow, MySQL y desplegado en Railway.

## 🏗️ Arquitectura

```
WhatsApp → Twilio → Dialogflow → Webhook (Flask) → MySQL (Railway)
```

## 🚀 Instalación y Configuración

### 1. Prerrequisitos
- Python 3.8+
- Cuenta en Railway
- Cuenta en Google Cloud (Dialogflow)
- Cuenta en Twilio (opcional para WhatsApp)

### 2. Instalación Local
```bash
# Clonar repositorio
git clone <tu-repositorio>
cd chatbot-panaderia-jos-y-mar

# Instalar dependencias
cd webhook
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar aplicación
python app.py
```

### 3. Variables de Entorno Requeridas
```env
# Base de datos
DB_HOST=tu-host-mysql
DB_PORT=3306
DB_USER=tu-usuario
DB_PASSWORD=tu-password
DB_NAME=panaderia_jos_y_mar

# Flask
FLASK_ENV=production
PORT=5000
```

## 📊 Base de Datos

### Estructura de Tablas
- **productos**: Catálogo de productos por categorías
- **clientes**: Información de clientes registrados
- **pedidos**: Pedidos realizados por clientes
- **pedido_items**: Items específicos de cada pedido

### Categorías de Productos
- 🥖 Pan Salado
- 🍰 Pan Dulce
- 🥐 Panes Semidulces
- 🎂 Pasteles
- 🥟 Bocaditos

## 🔗 API Endpoints

### Health Check
```
GET / → Estado de la aplicación
GET /test-db → Test de conexión a BD
```

### Productos
```
GET /productos/<categoria> → Lista productos por categoría
```

### Webhook Principal
```
POST /webhook → Endpoint para Dialogflow
```

## 💬 Flujos de Conversación

### 1. Saludo Inicial
```
Bot: ¡Hola! Bienvenido a Panadería Jos y Mar 🍞
     ¿En qué puedo ayudarte hoy?
     
     1️⃣ Ver productos y precios
     2️⃣ Hacer un pedido
     3️⃣ Información de la panadería
     4️⃣ Hablar con una persona
```

### 2. Consultar Productos
```
Bot: ¿Qué tipo de producto te interesa?
     🥖 Pan salado | 🍰 Pan dulce | 🥐 Panes semidulces
     🎂 Pasteles | 🥟 Bocaditos
```

### 3. Hacer Pedido
```
Bot: Para hacer tu pedido necesito:
     1. ¿Cuál es tu nombre?
     2. ¿Para qué fecha? (mínimo 1 día de anticipación)
     3. ¿Delivery o recojo en tienda?
     4. [Si delivery] ¿Cuál es tu dirección?
```

## 🤖 Configuración Dialogflow

### Intents Principales
- `Default Welcome Intent`: Saludo inicial
- `consultar.productos.categoria`: Mostrar productos (→ webhook)
- `hacer.pedido.inicio`: Iniciar pedido
- `hacer.pedido.confirmar`: Confirmar pedido (→ webhook)
- `registrar.cliente`: Registrar cliente (→ webhook)
- `informacion.panaderia`: Info de la panadería
- `transferir.humano`: Transferir a humano

### Webhook URL
```
https://tu-app.railway.app/webhook
```

## 🚀 Despliegue en Railway

### 1. Configurar Base de Datos
- Crear servicio MySQL en Railway
- Ejecutar `database/schema.sql`
- Ejecutar `database/sample_data.sql`

### 2. Desplegar Aplicación
- Conectar repositorio GitHub
- Configurar variables de entorno
- Railway detectará Flask automáticamente

### 3. Verificación
```bash
# Health check
curl https://tu-app.railway.app/

# Test base de datos
curl https://tu-app.railway.app/test-db

# Test productos
curl https://tu-app.railway.app/productos/pan_salado
```

## 🧪 Testing

### Tests Básicos
```bash
# Ejecutar desde directorio docs/
python test_basic.py
```

### Cases de Prueba
- ✅ Consultar productos por categoría
- ✅ Realizar pedido completo (delivery)
- ✅ Realizar pedido completo (recojo)
- ✅ Transferir a humano
- ✅ Consultar información de panadería
- ✅ Manejar mensajes no entendidos

## 📁 Estructura del Proyecto

```
chatbot-panaderia-jos-y-mar/
├── README.md                          # Este archivo
├── especificaciones_chatbot_panaderia_jos_y_mar.md
├── .github/
│   └── copilot-instructions.md        # Instrucciones de desarrollo
├── webhook/                           # Aplicación Flask
│   ├── app.py                        # Aplicación principal
│   ├── database.py                   # Conexión MySQL
│   ├── models.py                     # Funciones de BD
│   ├── utils.py                      # Utilidades
│   ├── requirements.txt              # Dependencias
│   └── .env.example                  # Variables de entorno
├── database/                         # Scripts de BD
│   ├── schema.sql                    # Estructura de tablas
│   └── sample_data.sql               # Datos de ejemplo
└── docs/                            # Documentación
    ├── deployment.md                # Guía de despliegue
    └── testing.md                   # Plan de pruebas
```

## 🔧 Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de Datos**: MySQL
- **Conversación**: Google Dialogflow
- **WhatsApp**: Twilio (opcional)
- **Hosting**: Railway
- **Dependencias**: Ver `requirements.txt`

## 📝 Notas Importantes

### Limitaciones Actuales
- Pedidos solo con 1 día de anticipación mínimo
- No modificación de pedidos via chatbot
- Precios en datos de ejemplo están en 0.00 (actualizar con precios reales)
- Pago manual (requiere confirmación humana)

### Próximas Mejoras
- Integración completa con Twilio WhatsApp
- Sistema de pagos automático
- Panel administrativo para gestión
- Notificaciones automáticas

## 👥 Equipo de Desarrollo

- **Desarrollador Principal**: twix2907
- **Fecha Límite**: 2025-01-10
- **Objetivo**: Chatbot funcional para consultas y pedidos

## 📞 Soporte

Para issues técnicos o preguntas sobre el código, revisar:
1. `docs/testing.md` para casos de prueba
2. `docs/deployment.md` para problemas de despliegue
3. `.github/copilot-instructions.md` para lineamientos de desarrollo

---

**¡Panadería Jos y Mar - Conectando tradición con tecnología! 🍞**
