from flask import Flask, request, jsonify
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging
from database import test_connection
from models import (
    get_productos_por_categoria, 
    crear_cliente, 
    crear_pedido, 
    agregar_item_pedido,
    get_pedido_completo,
    get_todas_categorias,
    buscar_producto_por_nombre
)
from utils import (
    validar_telefono,
    validar_fecha_entrega,
    formatear_lista_productos,
    formatear_categoria_display,
    generar_mensaje_pedido_confirmacion
)

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación Flask
app = Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    """
    Health check básico
    """
    return jsonify({
        'status': 'ok',
        'message': 'Webhook Panadería Jos y Mar funcionando',
        'version': '1.0.0'
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook principal para Dialogflow
    """
    try:
        # Obtener datos del request de Dialogflow
        req = request.get_json()
        
        # Extraer información básica
        intent_name = req.get('queryResult', {}).get('intent', {}).get('displayName', '')
        parameters = req.get('queryResult', {}).get('parameters', {})
        query_text = req.get('queryResult', {}).get('queryText', '')
        
        logger.info(f"Intent recibido: {intent_name}")
        logger.info(f"Parámetros: {parameters}")
        
        # Procesar según el intent
        if intent_name == 'consultar.productos.categoria':
            return handle_consultar_productos(parameters)
        elif intent_name == 'hacer.pedido.productos':
            return handle_pedido_productos(parameters, req)
        elif intent_name == 'hacer.pedido.telefono':
            return handle_pedido_telefono(parameters, req)
        elif intent_name == 'hacer.pedido.confirmar':
            return handle_confirmar_pedido(parameters, req)
        elif intent_name == 'registrar.cliente':
            return handle_registrar_cliente(parameters)
        else:
            return jsonify({
                'fulfillmentText': 'Lo siento, no pude procesar tu solicitud. ¿Puedes intentar de nuevo?'
            })
            
    except Exception as e:
        logger.error(f"Error en webhook: {str(e)}")
        return jsonify({
            'fulfillmentText': 'Ocurrió un error técnico. Por favor intenta nuevamente en unos momentos.'
        })

def handle_consultar_productos(parameters):
    """
    Maneja consultas de productos por categoría
    """
    categoria = parameters.get('categoria_producto', '')
    
    # Convertir el formato de categoría para que coincida con la BD
    if categoria:
        categoria = categoria.replace(' ', '_')
    
    if not categoria:
        # Mostrar todas las categorías disponibles
        categorias = get_todas_categorias()
        if categorias:
            texto = "¿Qué tipo de producto te interesa?\n\n"
            for cat in categorias:
                texto += f"{formatear_categoria_display(cat['categoria'])}\n"
            return jsonify({'fulfillmentText': texto})
        else:
            return jsonify({'fulfillmentText': 'No hay productos disponibles en este momento.'})
    
    # Obtener productos de la categoría específica
    productos = get_productos_por_categoria(categoria)
    
    if productos:
        texto = f"{formatear_categoria_display(categoria)}:\n\n"
        texto += formatear_lista_productos(productos)
        texto += "\n\n¿Te gustaría hacer un pedido o ver otra categoría?"
    else:
        texto = f"No tenemos productos disponibles en la categoría {formatear_categoria_display(categoria)} en este momento."
    
    return jsonify({'fulfillmentText': texto})

def handle_registrar_cliente(parameters):
    """
    Maneja el registro de un nuevo cliente
    """
    # Extraer parámetros con nombres correctos de Dialogflow
    person = parameters.get('person', {})
    if isinstance(person, dict):
        nombre = person.get('name', '').strip()
    else:
        nombre = person.strip() if person else ''
    
    telefono = parameters.get('phone-number', '').strip()
    direccion = parameters.get('direccion', '').strip()  # Opcional
    
    # Validar datos requeridos
    if not nombre or not telefono:
        return jsonify({
            'fulfillmentText': 'Necesito tu nombre y número de teléfono para registrarte.'
        })
    
    # Validar formato de teléfono
    telefono_valido = validar_telefono(telefono)
    if not telefono_valido:
        return jsonify({
            'fulfillmentText': 'El número de teléfono no es válido. Por favor proporciona un número peruano válido.'
        })
    
    # Crear cliente
    cliente_id = crear_cliente(nombre, telefono_valido, direccion)
    
    if cliente_id:
        return jsonify({
            'fulfillmentText': f'¡Perfecto {nombre}! Te hemos registrado con éxito. ¿En qué más puedo ayudarte?'
        })
    else:
        return jsonify({
            'fulfillmentText': 'Hubo un problema al registrarte. Por favor intenta nuevamente.'
        })

def handle_confirmar_pedido(parameters, req):
    """
    Maneja la confirmación final de un pedido (cuando el usuario dice "sí")
    """
    # Extraer datos de parámetros directos y contextos
    datos_directos = {
        'telefono': parameters.get('telefono', '') or parameters.get('phone-number', ''),
        'fecha_entrega': parameters.get('fecha_entrega', '') or parameters.get('date', ''),
        'tipo_entrega': parameters.get('tipo_entrega', ''),
        'direccion_entrega': parameters.get('direccion_entrega', ''),
        'nombre': parameters.get('nombre', '') or (parameters.get('person', {}).get('name', '') if isinstance(parameters.get('person'), dict) else parameters.get('person', '')),
        'notas': parameters.get('notas', '')
    }
    
    # Combinar con datos de contexto
    datos_contexto = extraer_datos_contexto(req)
    
    # Usar datos directos como prioridad, contexto como fallback
    datos_finales = {}
    for key in ['telefono', 'fecha_entrega', 'tipo_entrega', 'direccion_entrega', 'nombre', 'notas']:
        datos_finales[key] = datos_directos.get(key) or datos_contexto.get(key, '')
    
    logger.info(f"Confirmación de pedido - Datos finales: {datos_finales}")
    
    # Validaciones básicas
    if not datos_finales['telefono']:
        return jsonify({
            'fulfillmentText': 'Necesito un número de teléfono válido para procesar el pedido.'
        })
    
    telefono_valido = validar_telefono(datos_finales['telefono'])
    if not telefono_valido:
        return jsonify({
            'fulfillmentText': 'El número de teléfono no es válido. Por favor proporciona un número peruano válido.'
        })
    
    if not datos_finales['fecha_entrega']:
        return jsonify({
            'fulfillmentText': 'Necesito la fecha de entrega para procesar el pedido.'
        })
    
    # Validar fecha
    try:
        fecha_valida = validar_fecha_entrega(datos_finales['fecha_entrega'])
        if not fecha_valida:
            return jsonify({
                'fulfillmentText': 'La fecha de entrega debe ser con al menos 1 día de anticipación.'
            })
    except:
        # Si hay error en validación de fecha, usar fecha de mañana por defecto
        fecha_valida = (datetime.now() + timedelta(days=1)).date()
        logger.warning(f"Error validando fecha {datos_finales['fecha_entrega']}, usando fecha por defecto: {fecha_valida}")
    
    if not datos_finales['tipo_entrega'] or datos_finales['tipo_entrega'] not in ['delivery', 'recojo']:
        return jsonify({
            'fulfillmentText': 'Por favor especifica si prefieres delivery o recoger en tienda.'
        })
    
    # Crear confirmación del pedido
    try:
        nombre_cliente = datos_finales['nombre'] or "Cliente"
        
        # Generar número de pedido simple
        import random
        numero_pedido = f"PED{random.randint(1000, 9999)}"
        
        mensaje_final = f"¡Excelente! 🎉\n\n"
        mensaje_final += f"Tu pedido #{numero_pedido} ha sido confirmado:\n\n"
        mensaje_final += f"👤 Cliente: {nombre_cliente}\n"
        mensaje_final += f"📞 Teléfono: {telefono_valido}\n"
        mensaje_final += f"📅 Fecha de entrega: {datos_finales['fecha_entrega']}\n"
        mensaje_final += f"🚚 Modalidad: {datos_finales['tipo_entrega'].title()}\n"
        
        if datos_finales['direccion_entrega'] and datos_finales['tipo_entrega'] == 'delivery':
            mensaje_final += f"📍 Dirección: {datos_finales['direccion_entrega']}\n"
        
        if datos_finales['notas']:
            mensaje_final += f"📝 Notas especiales: {datos_finales['notas']}\n"
        
        mensaje_final += f"\nNos pondremos en contacto contigo para coordinar los detalles.\n"
        mensaje_final += f"¡Gracias por elegir Panadería Jos y Mar! 🥖✨"
        
        return jsonify({
            'fulfillmentText': mensaje_final
        })
        
    except Exception as e:
        logger.error(f"Error procesando pedido: {str(e)}")
        return jsonify({
            'fulfillmentText': 'Hubo un problema al procesar tu pedido. Por favor intenta nuevamente.'
        })

def handle_pedido_telefono(parameters, req):
    """
    Maneja específicamente cuando se recibe el teléfono en el flujo de pedido
    """
    # Extraer datos de parámetros directos y contextos
    datos_directos = {
        'telefono': parameters.get('telefono', '') or parameters.get('phone-number', ''),
        'fecha_entrega': parameters.get('fecha_entrega', '') or parameters.get('date', ''),
        'tipo_entrega': parameters.get('tipo_entrega', ''),
        'direccion_entrega': parameters.get('direccion_entrega', ''),
        'nombre': parameters.get('nombre', '') or (parameters.get('person', {}).get('name', '') if isinstance(parameters.get('person'), dict) else parameters.get('person', '')),
        'notas': parameters.get('notas', '')
    }
    
    # Combinar con datos de contexto
    datos_contexto = extraer_datos_contexto(req)
    
    # Usar datos directos como prioridad, contexto como fallback
    datos_finales = {}
    for key in ['telefono', 'fecha_entrega', 'tipo_entrega', 'direccion_entrega', 'nombre', 'notas']:
        datos_finales[key] = datos_directos.get(key) or datos_contexto.get(key, '')
    
    logger.info(f"Datos del pedido en teléfono - Datos finales: {datos_finales}")
    
    # Validar teléfono
    if not datos_finales['telefono']:
        return jsonify({
            'fulfillmentText': 'Por favor proporciona tu número de teléfono para continuar con el pedido.'
        })
    
    telefono_valido = validar_telefono(datos_finales['telefono'])
    if not telefono_valido:
        return jsonify({
            'fulfillmentText': 'El número de teléfono no es válido. Por favor proporciona un número peruano válido (ej: 987654321).'
        })
    
    # Crear mensaje de confirmación con todos los datos disponibles
    mensaje_confirmacion = f"Perfecto! He registrado tu teléfono: {telefono_valido}\n\n"
    mensaje_confirmacion += "Resumen de tu pedido:\n"
    
    if datos_finales['nombre']:
        mensaje_confirmacion += f"👤 Cliente: {datos_finales['nombre']}\n"
    if datos_finales['fecha_entrega']:
        mensaje_confirmacion += f"📅 Fecha: {datos_finales['fecha_entrega']}\n"
    if datos_finales['tipo_entrega']:
        mensaje_confirmacion += f"🚚 Tipo: {datos_finales['tipo_entrega'].title()}\n"
    if datos_finales['direccion_entrega'] and datos_finales['tipo_entrega'] == 'delivery':
        mensaje_confirmacion += f"📍 Dirección: {datos_finales['direccion_entrega']}\n"
    if datos_finales['notas']:
        mensaje_confirmacion += f"📝 Notas: {datos_finales['notas']}\n"
    
    mensaje_confirmacion += f"📞 Teléfono: {telefono_valido}\n\n"
    mensaje_confirmacion += "¿Confirmas este pedido? Responde 'sí' para confirmar o 'no' para cancelar."
    
    return jsonify({'fulfillmentText': mensaje_confirmacion})

def handle_pedido_productos(parameters, req):
    """
    Maneja la captura de productos cuando el usuario especifica qué quiere comprar
    """
    productos = parameters.get('producto', [])
    cantidades = parameters.get('number', [])
    
    # Asegurar que sean listas
    if not isinstance(productos, list):
        productos = [productos] if productos else []
    if not isinstance(cantidades, list):
        cantidades = [cantidades] if cantidades else []
    
    # Validar que tengamos productos
    if not productos:
        return jsonify({
            'fulfillmentText': 'No pude identificar los productos que deseas. ¿Puedes especificar qué productos te gustaría comprar?\n\nEjemplo: "Quiero 2 baguettes y 1 torta de chocolate"'
        })
    
    # Crear lista de productos del pedido
    items_pedido = []
    mensaje_productos = ""
    total_items = 0
    productos_no_encontrados = []
    
    # Procesar cada producto
    for i, producto_nombre in enumerate(productos):
        # Obtener cantidad correspondiente, o 1 por defecto
        cantidad = 1
        if i < len(cantidades):
            try:
                cantidad = int(float(cantidades[i]))
            except (ValueError, TypeError):
                cantidad = 1
        
        # Buscar el producto en la base de datos
        producto_info = buscar_producto_por_nombre(producto_nombre)
        
        if producto_info:
            # Agregar a la lista
            items_pedido.append({
                'producto': producto_nombre,
                'cantidad': cantidad,
                'producto_id': producto_info['id'],
                'precio': producto_info['precio']
            })
            
            # Construir mensaje con precio
            precio_unitario = producto_info['precio']
            precio_total = precio_unitario * cantidad
            
            if cantidad == 1:
                mensaje_productos += f"• {cantidad} {producto_info['nombre']} - S/ {precio_total:.2f}\n"
            else:
                mensaje_productos += f"• {cantidad} {producto_info['nombre']}s - S/ {precio_total:.2f}\n"
            
            total_items += cantidad
        else:
            # Producto no encontrado
            productos_no_encontrados.append(producto_nombre)
    
    # Crear mensaje de respuesta
    if items_pedido:
        precio_total_pedido = sum(item['precio'] * item['cantidad'] for item in items_pedido)
        
        mensaje = f"Perfecto! He agregado a tu pedido:\n\n{mensaje_productos}"
        mensaje += f"\nTotal de productos: {total_items}\n"
        mensaje += f"💰 Subtotal: S/ {precio_total_pedido:.2f}\n\n"
        
        if productos_no_encontrados:
            mensaje += f"⚠️ No pude encontrar: {', '.join(productos_no_encontrados)}\n"
            mensaje += "¿Podrías especificar estos productos de otra manera?\n\n"
        
        mensaje += "¿Deseas agregar algo más o continuamos con los datos del pedido?\n\n"
        mensaje += "Puedes decir:\n"
        mensaje += "• \"Agregar más productos\" para seguir agregando\n"
        mensaje += "• \"Continuar\" o \"Confirmar\" para proceder con tus datos"
    else:
        mensaje = f"No pude encontrar los productos: {', '.join(productos_no_encontrados)}\n\n"
        mensaje += "¿Podrías especificar los productos de otra manera?\n"
        mensaje += "Por ejemplo: 'baguette', 'pan francés', 'torta de chocolate', etc."
    
    return jsonify({
        'fulfillmentText': mensaje
    })

@app.route('/productos/<categoria>', methods=['GET'])
def get_productos_categoria(categoria):
    """
    Endpoint directo para consultar productos por categoría
    """
    productos = get_productos_por_categoria(categoria)
    return jsonify({
        'categoria': categoria,
        'productos': productos
    })

@app.route('/test-db', methods=['GET'])
def test_database():
    """
    Endpoint para probar la conexión a la base de datos
    """
    if test_connection():
        return jsonify({'status': 'success', 'message': 'Conexión a base de datos exitosa'})
    else:
        return jsonify({'status': 'error', 'message': 'Error en conexión a base de datos'}), 500

def extraer_datos_contexto(req):
    """
    Función auxiliar para extraer datos de los contextos de Dialogflow
    """
    contexts = req.get('queryResult', {}).get('outputContexts', [])
    datos = {}
    
    for context in contexts:
        ctx_params = context.get('parameters', {})
        
        # Extraer todos los parámetros posibles
        if 'date' in ctx_params or 'fecha_entrega' in ctx_params:
            datos['fecha_entrega'] = ctx_params.get('date', '') or ctx_params.get('fecha_entrega', '')
        
        if 'tipo_entrega' in ctx_params:
            tipo = ctx_params.get('tipo_entrega', '')
            if isinstance(tipo, list) and tipo:
                datos['tipo_entrega'] = tipo[0]
            else:
                datos['tipo_entrega'] = tipo
        
        if 'person' in ctx_params or 'nombre' in ctx_params:
            person = ctx_params.get('person', {})
            if isinstance(person, dict):
                datos['nombre'] = person.get('name', '')
            else:
                datos['nombre'] = person or ctx_params.get('nombre', '')
        
        if 'direccion_entrega' in ctx_params or 'direccion' in ctx_params:
            direccion = ctx_params.get('direccion_entrega', {})
            if isinstance(direccion, dict):
                datos['direccion_entrega'] = f"{direccion.get('business-name', '')} {direccion.get('street-address', '')}".strip()
            else:
                datos['direccion_entrega'] = direccion or ctx_params.get('direccion', '')
        
        if 'notas' in ctx_params:
            datos['notas'] = ctx_params.get('notas', '')
        
        if 'phone-number' in ctx_params or 'telefono' in ctx_params:
            datos['telefono'] = ctx_params.get('phone-number', '') or ctx_params.get('telefono', '')
        
        # Extraer productos si existen
        if 'producto' in ctx_params:
            datos['productos'] = ctx_params.get('producto', [])
        
        if 'number' in ctx_params:
            datos['cantidades'] = ctx_params.get('number', [])
    
    return datos

if __name__ == '__main__':
    # Verificar conexión a BD al iniciar
    logger.info("Iniciando webhook Panadería Jos y Mar...")
    if test_connection():
        logger.info("✅ Conexión a base de datos verificada")
    else:
        logger.warning("⚠️  No se pudo conectar a la base de datos")
    
    # Obtener puerto desde variable de entorno
    port = int(os.getenv('PORT', 5000))
    
    # Ejecutar aplicación
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')
