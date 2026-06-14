from flask import Blueprint, render_template, session, redirect, url_for, request, flash, jsonify
from models.cart_model import agregar_producto_al_carrito, obtener_carrito_usuario, eliminar_del_carrito
from models.auth_model import obtener_datos_envio_usuario
from models.direccion_model import guardar_direccion

cart_blueprint = Blueprint('cart', __name__, url_prefix='/carrito')

@cart_blueprint.route('/')
def ver_carrito():
    if 'usuario' not in session:
        flash('Debes iniciar sesión para ver tu carrito.', 'warning')
        return redirect(url_for('auth.login'))
    
    carrito_data = obtener_carrito_usuario(session['usuario']['id'])
    items = carrito_data.get('items', [])
    total = carrito_data.get('total', 0)
    return render_template('carrito.html', items=items, total=total, usuario_sesion=session.get('usuario'))

@cart_blueprint.route('/agregar/<int:producto_id>', methods=['POST'])
def agregar(producto_id):
    if 'usuario' not in session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'status': 'login_required', 'message': 'Inicia sesión primero'}), 401
        flash('Debes iniciar sesión para añadir productos al carrito.', 'warning')
        return redirect(url_for('auth.login'))
        
    cantidad = request.form.get('cantidad', 1, type=int)
    
    try:
        agregar_producto_al_carrito(session['usuario']['id'], producto_id, cantidad=cantidad)
    except Exception:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'status': 'error', 'message': 'No se pudo agregar al carrito'}), 500
        flash('Error al agregar el producto al carrito.', 'danger')
        return redirect(url_for('products.ver_producto', producto_id=producto_id))
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'status': 'success', 'message': f'{cantidad} producto(s) añadido(s)'})
    
    if request.form.get('comprar_ahora') == 'true':
        return redirect(url_for('cart.ver_carrito'))
        
    flash(f'¡Se agregaron ({cantidad}) unidades con éxito al carrito!', 'success')
    return redirect(url_for('products.ver_producto', producto_id=producto_id))

@cart_blueprint.route('/eliminar/<int:detalle_id>', methods=['POST'])
def eliminar(detalle_id):
    if 'usuario' not in session:
        flash('Debes iniciar sesión para modificar tu carrito.', 'warning')
        return redirect(url_for('auth.login'))
        
    try:
        eliminar_del_carrito(detalle_id)
        flash('Producto retirado de la bolsa con éxito.', 'success')
    except Exception:
        flash('No se pudo remover el producto en este momento.', 'danger')
        
    return redirect(url_for('cart.ver_carrito'))

@cart_blueprint.route('/api/cantidad')
def obtener_cantidad_api():
    if 'usuario' not in session:
        return jsonify({'cantidad': 0})
    carrito_data = obtener_carrito_usuario(session['usuario']['id'])
    total_unidades = sum(item['cantidad'] for item in carrito_data.get('items', []))
    return jsonify({'cantidad': total_unidades})

@cart_blueprint.route('/configurar-direccion')
def configurar_direccion():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))
    return render_template('direccion.html')

@cart_blueprint.route('/validar-envio')
def validar_envio():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))
    
    datos_usuario = obtener_datos_envio_usuario(session['usuario']['id'])
    
    if not datos_usuario or not datos_usuario.get('direccion'):
        flash('Por favor, configura tu dirección de entrega.', 'info')
        return redirect(url_for('cart.configurar_direccion'))
    
    return redirect(url_for('payment.procesar_pago'))

@cart_blueprint.route('/guardar-direccion', methods=['POST'])
def guardar_direccion_route():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))
        
    # 1. Capturamos los datos del formulario
    departamento = request.form.get('departamento')
    ciudad = request.form.get('ciudad')
    barrio = request.form.get('barrio')
    direccion = request.form.get('direccion')
    
    # 2. Validación básica
    if not departamento or not ciudad or not barrio or not direccion:
        flash('Por favor, completa todos los campos de la dirección.', 'danger')
        return redirect(url_for('cart.configurar_direccion'))
    
    # 3. Intentamos guardar en la base de datos usando el modelo
    try:
        # Llamamos al modelo pasando los parámetros capturados
        exito = guardar_direccion(session['usuario']['id'], departamento, ciudad, barrio, direccion)
        
        if exito:
            flash('Dirección guardada correctamente.', 'success')
            return redirect(url_for('payment.procesar_pago'))
        else:
            flash('Hubo un error al guardar en la base de datos.', 'danger')
            return redirect(url_for('cart.configurar_direccion'))
            
    except Exception as e:
        # Manejo de errores inesperados
        print(f"Error al guardar dirección: {e}")
        flash('Ocurrió un error al procesar tu solicitud.', 'danger')
        return redirect(url_for('cart.configurar_direccion'))