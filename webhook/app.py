from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import logging
from database import test_connection
from models import (
    get_productos_por_categoria, 
    crear_cliente, 
    crear_pedido, 
    agregar_item_pedido,
    get_pedido_completo,
    get_todas_categorias
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
        elif intent_name == 'hacer.pedido.confirmar':
            return handle_confirmar_pedido(parameters)
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
    nombre = parameters.get('nombre', '').strip()
    telefono = parameters.get('telefono', '').strip()
    direccion = parameters.get('direccion', '').strip()
    
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

def handle_confirmar_pedido(parameters):
    """
    Maneja la confirmación de un pedido
    """
    # Extraer parámetros del pedido
    cliente_telefono = parameters.get('telefono', '')
    fecha_entrega = parameters.get('fecha_entrega', '')
    tipo_entrega = parameters.get('tipo_entrega', '')
    direccion_entrega = parameters.get('direccion_entrega', '')
    
    # Validaciones básicas
    telefono_valido = validar_telefono(cliente_telefono)
    if not telefono_valido:
        return jsonify({
            'fulfillmentText': 'Necesito un número de teléfono válido para procesar el pedido.'
        })
    
    fecha_valida = validar_fecha_entrega(fecha_entrega)
    if not fecha_valida:
        return jsonify({
            'fulfillmentText': 'La fecha de entrega debe ser con al menos 1 día de anticipación.'
        })
    
    if tipo_entrega not in ['delivery', 'recojo']:
        return jsonify({
            'fulfillmentText': 'Por favor especifica si prefieres delivery o recoger en tienda.'
        })
    
    # Por simplicidad, crear un pedido de ejemplo
    # En una implementación real, esto vendría de un contexto de conversación
    try:
        # Aquí iría la lógica completa de manejo de pedidos
        # Por ahora retornamos un mensaje de confirmación simple
        return jsonify({
            'fulfillmentText': f'Tu pedido ha sido registrado para el {fecha_entrega} por {tipo_entrega}. Te contactaremos pronto para confirmar los detalles.'
        })
    except Exception as e:
        logger.error(f"Error procesando pedido: {str(e)}")
        return jsonify({
            'fulfillmentText': 'Hubo un problema al procesar tu pedido. Por favor intenta nuevamente.'
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
