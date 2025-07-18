# Descripción Técnica y Análisis del Sistema

Este proyecto implementa un sistema de chatbot avanzado para la Panadería Jos y Mar, diseñado para automatizar la atención al cliente, la consulta de productos y la gestión de pedidos a través de WhatsApp, integrando múltiples tecnologías cloud y de procesamiento de lenguaje natural.

## Componentes y Arquitectura

- **Backend principal (`webhook/app.py`)**: Desarrollado en Flask, expone endpoints REST para Dialogflow y Twilio, maneja la lógica de negocio, la gestión de sesiones de usuario en memoria y la integración con la base de datos MySQL. Incluye endpoints de salud, pruebas de conexión, consulta de productos y depuración de sesiones.
- **Integración con Dialogflow**: El endpoint `/webhook` recibe peticiones POST de Dialogflow, procesa intents y parámetros, y responde con mensajes personalizados según el flujo conversacional. El intent de confirmación de pedido responde con un resumen detallado y real del pedido, incluyendo productos, totales y datos del cliente.
- **Integración con Twilio**: El endpoint `/twilio` recibe mensajes de WhatsApp, los reenvía a Dialogflow usando el SDK oficial, y responde a los usuarios en formato TwiML. El session_id de Twilio se usa para mantener la conversación personalizada y persistente.
- **Gestión de sesiones**: El sistema mantiene un almacenamiento en memoria por sesión de usuario, permitiendo flujos conversacionales complejos y persistencia temporal de datos de pedido, productos, cliente y estado del flujo. Incluye limpieza automática de sesiones inactivas y endpoints de depuración.
- **Base de datos MySQL**: Gestiona productos, clientes, pedidos y sus items. Los scripts SQL (`schema.sql`, `sample_data.sql`) definen la estructura y datos de ejemplo, permitiendo una gestión robusta y escalable de la información.
- **Módulos auxiliares**: `models.py` (acceso a datos y lógica de negocio), `utils.py` (validaciones, formateo de mensajes), `database.py` (conexión y utilidades de BD), `setup_database.py` y `setup_db_complete.py` (automatización de la inicialización de la base de datos).
- **Configuración y despliegue**: El sistema está preparado para Railway, con variables de entorno, scripts de setup y documentación detallada en `docs/`. Incluye archivos de ejemplo para configuración rápida y segura.
- **Agente Dialogflow**: Configurado con intents y entities exportados en `josy_bot (3)/`, permitiendo un flujo conversacional natural y flexible, con soporte para slot filling, contextos y manejo de excepciones.

## Experiencia de Usuario y Flujos Conversacionales

- El usuario inicia la conversación por WhatsApp o la web, el mensaje llega a Twilio y luego a Dialogflow.
- Dialogflow detecta el intent y, si corresponde, llama al webhook Flask, que procesa la lógica y responde con el mensaje adecuado.
- El sistema guía al usuario por el flujo de consulta de productos, registro de datos, armado de pedido, confirmación y resumen final, gestionando cada paso y validando los datos.
- El almacenamiento de sesión permite que el usuario pueda agregar productos, modificar datos, cancelar o confirmar el pedido en cualquier momento del flujo.
- El sistema maneja errores, validaciones y respuestas personalizadas para cada caso, asegurando una experiencia fluida y robusta.
- El usuario puede ser transferido a un humano en cualquier momento, y el sistema está preparado para futuras integraciones de soporte humano.

## Pruebas, Monitoreo y Mantenimiento

- El proyecto incluye scripts y documentación para pruebas unitarias y de integración (`test_*.py`, `docs/testing.md`).
- Los logs detallados permiten monitorear el estado de las sesiones, la interacción con Dialogflow y la base de datos, y detectar errores o cuellos de botella.
- El sistema está preparado para ser desplegado y monitoreado en Railway, con health checks y endpoints de prueba.
- La modularidad del código y la documentación facilitan la incorporación de nuevos desarrolladores y la extensión de funcionalidades.

## Casos de Uso y Escenarios Soportados

- Consulta de productos y precios por categoría.
- Registro y validación de clientes.
- Armado y confirmación de pedidos personalizados.
- Elección de modalidad de entrega (delivery o recojo en tienda).
- Manejo de notas especiales y direcciones personalizadas.
- Respuestas automáticas a preguntas frecuentes e información de la panadería.
- Transferencia a humano y manejo de mensajes no entendidos.

## Visión de Futuro y Extensibilidad

- El sistema está preparado para integrar pagos automáticos, paneles administrativos y notificaciones automáticas.
- Puede escalarse fácilmente a otros canales de mensajería (Telegram, Facebook Messenger) y a nuevas sucursales o negocios.
- La estructura de intents y entities en Dialogflow permite agregar nuevos productos, promociones y flujos sin modificar el backend.
- El uso de variables de entorno y scripts de setup permite migrar o replicar el sistema en otros entornos cloud de forma sencilla.

---

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
