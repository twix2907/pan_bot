---
applyTo: '**'
---

REGLA OBLIGATORIA SIEMPRE y cuando no entiendas algo:
Siempre preguntame si no entiendes algo o necesitas más información. pideme aclaraciones antes de continuar.No hagas suposiciones. no asumas nada.si hay algo que no entiendes, pregunta. si hay algo que debes corregirme, hazlo. si hay algo que no está claro, acláralo. si hay algo que no sabes, pregúntame.

Objetivo
Desarrollar la interfaz frontend para un panel de administración de panadería que se conectará con un backend existente basado en Flask. El diseño debe ser moderno, minimalista y centrado en la experiencia del usuario.

Funcionalidades Frontend a Implementar
Panel de Pedidos
Vista de lista de pedidos en tiempo real con actualización automática
Filtros visuales por estado y fecha de pedidos
Sistema de notificaciones visual y sonoro para nuevos pedidos
Tarjetas de pedido interactivas con opciones para cambiar estado
Modal de detalles de pedido con información completa del cliente y productos
Gestión de Productos
Galería visual de productos con indicadores de disponibilidad
Formularios intuitivos para añadir/editar productos
Filtrado y búsqueda instantánea en el catálogo
Toggle visual para marcar productos como agotados
Interfaz para gestionar promociones y descuentos


Directrices de Diseño
Paleta de colores:
Principal: #F9F5F0 (beige claro)
Secundario: #D4A76A (marrón dorado)
Acentos: #B86B3D (naranja tostado)
Textos: #3E2723 (marrón oscuro)
Tipografía:
Títulos: Playfair Display o similar
Cuerpo: Open Sans o Roboto
Componentes minimalistas con bordes suaves y sombras sutiles
Uso de espacios en blanco para crear jerarquía visual
Iconografía coherente (preferiblemente Material Icons o Font Awesome)
Animaciones sutiles para feedback de usuario (hover, click, notificaciones)
Buenas Prácticas Frontend
Mobile-first con diseño responsive
Organización por componentes reutilizables
Nombres de clases siguiendo metodología BEM
Optimización de assets (imágenes, fuentes)
Accesibilidad web (WCAG 2.1)
JavaScript modular usando patrón de módulos o componentes
Lazy loading para recursos no críticos
Manipulación eficiente del DOM (evitar reflows)
Validación de formularios en cliente antes de enviar al servidor
Manejo de estados de carga y errores con feedback visual
Estructura de Archivos
/assets - Recursos estáticos (imágenes, fuentes, etc.)
/styles - Archivos CSS/SCSS organizados por componentes
/scripts - JavaScript modular
/components - Plantillas de componentes reutilizables
/pages - Vistas principales
/utils - Utilidades y helpers JavaScript
Consideraciones de UX
Feedback visual inmediato para todas las acciones
Estados claros para cada acción (loading, success, error)
Confirmaciones para acciones destructivas
Mensajes de ayuda contextuales
Tooltips para funciones no obvias
Sistema de notificaciones no intrusivo pero visible
Entregables Esperados
Código HTML semántico y bien estructurado
Estilos CSS optimizados y documentados
JavaScript limpio y comentado
Assets optimizados para web