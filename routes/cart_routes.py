from flask import Blueprint, render_template, session, redirect, url_for, request, flash, jsonify
from models.cart_model import agregar_producto_al_carrito, obtener_carrito_usuario, eliminar_del_carrito

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