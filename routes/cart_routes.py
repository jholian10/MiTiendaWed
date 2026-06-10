from flask import Blueprint, render_template, session, redirect, url_for, request, flash, jsonify
from models.cart_model import agregar_producto_al_carrito, obtener_detalles_carrito, eliminar_del_carrito

cart_blueprint = Blueprint('cart', __name__, url_prefix='/carrito')

@cart_blueprint.route('/')
def ver_carrito():
    if 'usuario' not in session:
        flash('Debes iniciar sesión para ver tu carrito.', 'warning')
        return redirect(url_for('auth.login'))
        
    items = obtener_detalles_carrito(session['usuario']['id'])
    
    # Calcular el total general de la compra
    total_general = sum(item['subtotal'] for item in items)
    
    return render_template('carrito.html', items=items, total=total_general, usuario_sesion=session.get('usuario'))

@cart_blueprint.route('/agregar/<int:producto_id>', methods=['POST'])
def agregar(producto_id):
    if 'usuario' not in session:
        # Si es una petición AJAX/Fetch, respondemos con JSON informando que requiere login
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'status': 'login_required', 'message': 'Inicia sesión primero'}), 401
        flash('Debes iniciar sesión para añadir productos al carrito.', 'warning')
        return redirect(url_for('auth.login'))
        
    agregar_producto_al_carrito(session['usuario']['id'], producto_id, cantidad=1)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'status': 'success', 'message': 'Producto añadido al carrito'})
        
    return redirect(url_for('products.index'))

@cart_blueprint.route('/eliminar/<int:detalle_id>', methods=['POST'])
def eliminar(detalle_id):
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))
        
    eliminar_del_carrito(detalle_id)
    flash('Producto removido del carrito.', 'success')
    return redirect(url_for('cart.ver_carrito'))

@cart_blueprint.route('/api/cantidad')
def obtener_cantidad_api():
    """Devuelve la suma total de piezas en el carrito para actualizar el AppBar de forma asíncrona."""
    if 'usuario' not in session:
        return jsonify({'cantidad': 0})
    
    items = obtener_detalles_carrito(session['usuario']['id'])
    cantidad_total = sum(item['cantidad'] for item in items)
    return jsonify({'cantidad': cantidad_total})