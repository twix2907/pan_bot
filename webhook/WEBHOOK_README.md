# Configuración del Webhook Panadería Jos y Mar

## Variables de Entorno Necesarias

Crea un archivo `.env` en la carpeta `webhook/` con el siguiente contenido:

```
# Base de datos
DATABASE_URL=postgresql://username:password@host:port/database_name

# Flask
FLASK_ENV=development
PORT=5000

# Dialogflow
PROJECT_ID=tu-proyecto-dialogflow

# Opcional - para logs
LOG_LEVEL=INFO
```

## Intents que usan Webhook

1. **consultar.productos.categoria**
   - Función: `handle_consultar_productos()`
   - Propósito: Mostrar productos por categoría

2. **hacer.pedido.productos**
   - Función: `handle_pedido_productos()`
   - Propósito: Capturar y validar productos del pedido

3. **hacer.pedido.telefono**
   - Función: `handle_pedido_telefono()`
   - Propósito: Procesar teléfono y mostrar resumen pre-confirmación

4. **hacer.pedido.confirmar**
   - Función: `handle_confirmar_pedido()`
   - Propósito: Confirmar pedido final y generar número de pedido

5. **registrar.cliente** (opcional)
   - Función: `handle_registrar_cliente()`
   - Propósito: Registrar cliente nuevo

## Flujo de Datos

### Contextos de Dialogflow utilizados:
- `esperando_productos` → captura productos
- `esperando_confirmacion_productos` → confirma productos
- `esperando_nombre` → captura nombre
- `esperando_fecha` → captura fecha
- `esperando_tipo_entrega` → delivery/recojo
- `esperando_direccion` → solo para delivery
- `esperando_nota` → notas especiales
- `esperando_telefono` → teléfono final
- `esperando_confirmacion_pedido` → confirmación final

### Parámetros principales:
- `@producto` - nombres de productos
- `@sys.number` - cantidades
- `@sys.person` - nombre del cliente
- `@sys.date` - fecha de entrega
- `@tipo_entrega` - delivery/recojo
- `@sys.location` - dirección
- `@sys.any` - notas
- `@sys.phone-number` - teléfono

## Endpoints Disponibles

- `GET /` - Health check
- `POST /webhook` - Webhook principal de Dialogflow
- `GET /productos/<categoria>` - Consulta directa de productos
- `GET /test-db` - Test de conexión a base de datos

## Validaciones Implementadas

1. **Teléfono**: Formato peruano (+51xxxxxxxxx)
2. **Fecha**: Mínimo 1 día de anticipación
3. **Productos**: Búsqueda en base de datos
4. **Contextos**: Extracción automática de datos previos

## Funciones de Utilidad

- `extraer_datos_contexto()` - Extrae datos de contextos Dialogflow
- `validar_telefono()` - Valida formato telefónico
- `validar_fecha_entrega()` - Valida fechas de entrega
- `buscar_producto_por_nombre()` - Búsqueda flexible de productos
- `formatear_lista_productos()` - Formatea productos para chat

## Respuesta Típica del Webhook

```json
{
  "fulfillmentText": "Mensaje para el usuario"
}
```

## Logging

El webhook registra:
- Intents recibidos
- Parámetros procesados
- Errores de validación
- Datos finales de pedidos

## Manejo de Errores

- Errores de validación → Mensajes específicos al usuario
- Errores de BD → Mensaje genérico + log del error
- Errores inesperados → Mensaje de reintentar + log completo
