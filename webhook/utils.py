import re
from datetime import datetime, timedelta

def validar_telefono(telefono):
    """
    Valida formato de número de teléfono peruano
    """
    # Remover espacios y caracteres especiales
    telefono_limpio = re.sub(r'[^\d+]', '', telefono)
    
    # Validar formato peruano: +51 seguido de 9 dígitos
    patron = r'^\+51\d{9}$'
    
    if re.match(patron, telefono_limpio):
        return telefono_limpio
    
    # Si no tiene código de país, agregarlo
    if re.match(r'^\d{9}$', telefono_limpio):
        return f'+51{telefono_limpio}'
    
    return None

def validar_fecha_entrega(fecha_str):
    """
    Valida que la fecha de entrega sea válida (mínimo 1 día de anticipación)
    """
    try:
        fecha_entrega = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        fecha_minima = (datetime.now() + timedelta(days=1)).date()
        
        if fecha_entrega >= fecha_minima:
            return fecha_entrega
        else:
            return None
    except ValueError:
        return None

def formatear_producto_texto(producto):
    """
    Formatea un producto para mostrar en texto
    """
    precio_texto = f"S/ {producto['precio']:.2f}" if producto['precio'] > 0 else "Consultar precio"
    return f"• {producto['nombre']} - {precio_texto}\n  {producto['descripcion']}"

def formatear_lista_productos(productos):
    """
    Formatea una lista de productos para mostrar en el chat
    """
    if not productos:
        return "No hay productos disponibles en esta categoría."
    
    texto = ""
    for producto in productos:
        texto += formatear_producto_texto(producto) + "\n\n"
    
    return texto.strip()

def calcular_total_pedido(items):
    """
    Calcula el total de un pedido basado en sus items
    """
    total = 0
    for item in items:
        total += item['cantidad'] * item['precio_unitario']
    return total

def formatear_categoria_display(categoria):
    """
    Convierte el nombre de categoría de la BD a texto amigable
    """
    categorias_display = {
        'pan_salado': '🥖 Pan Salado',
        'pan_dulce': '🍰 Pan Dulce',
        'pan_semidulce': '🥐 Panes Semidulces',
        'pasteles': '🎂 Pasteles',
        'bocaditos': '🥟 Bocaditos'
    }
    return categorias_display.get(categoria, categoria)

def limpiar_texto_usuario(texto):
    """
    Limpia y normaliza texto del usuario
    """
    # Remover espacios extra y convertir a minúsculas
    texto_limpio = ' '.join(texto.strip().lower().split())
    return texto_limpio

def generar_mensaje_pedido_confirmacion(pedido):
    """
    Genera mensaje de confirmación de pedido
    """
    mensaje = f"✅ **Pedido Confirmado #{pedido['id']}**\n\n"
    mensaje += f"👤 Cliente: {pedido['cliente_nombre']}\n"
    mensaje += f"📞 Teléfono: {pedido['cliente_telefono']}\n"
    mensaje += f"📅 Fecha de entrega: {pedido['fecha_entrega']}\n"
    mensaje += f"🚚 Tipo: {pedido['tipo_entrega'].title()}\n"
    
    if pedido['direccion_entrega']:
        mensaje += f"📍 Dirección: {pedido['direccion_entrega']}\n"
    
    mensaje += "\n**Productos:**\n"
    for item in pedido['items']:
        mensaje += f"• {item['cantidad']}x {item['producto_nombre']} - S/ {item['precio_unitario']:.2f}\n"
    
    mensaje += f"\n💰 **Total: S/ {pedido['total']:.2f}**\n\n"
    mensaje += "📝 Tu pedido está siendo procesado. Te contactaremos pronto para coordinar el pago y entrega."
    
    return mensaje
