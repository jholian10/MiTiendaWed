from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify
from models.favorite_model import conmutar_favorito, obtener_ids_favoritos, obtener_productos_favoritos

favorite_blueprint = Blueprint('favorites', __name__, url_prefix='/favoritos')

def obtener_usuario_id_sesion():
    if 'usuario_sesion' in session:
        return session['usuario_sesion'].get('id')
    if 'usuario' in session:
        return session['usuario'].get('id')
    return None

@favorite_blueprint.route('/')
def ver_favoritos():
    usuario_id = obtener_usuario_id_sesion()
    if not usuario_id:
        flash('Debes iniciar sesión para ver tus favoritos.', 'warning')
        return redirect(url_for('auth.login'))
        
    productos = obtener_productos_favoritos(usuario_id)
    usuario_datos = session.get('usuario_sesion') or session.get('usuario')
    return render_template('favoritos.html', productos=productos, usuario_sesion=usuario_datos)

@favorite_blueprint.route('/toggle/<int:producto_id>', methods=['POST'])
def toggle(producto_id):
    usuario_id = obtener_usuario_id_sesion()
    if not usuario_id:
        return jsonify({'status': 'login_required', 'message': 'Inicia sesión primero'}), 401
        
    try:
        agregado = conmutar_favorito(usuario_id, producto_id)
        mensaje = "Añadido a tus favoritos" if agregado else "Eliminado de tus favoritos"
        return jsonify({
            'status': 'success', 
            'message': mensaje,
            'agregado': agregado
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@favorite_blueprint.route('/api/cantidad')
def obtener_cantidad_api():
    usuario_id = obtener_usuario_id_sesion()
    if not usuario_id:
        return jsonify({'cantidad': 0, 'ids': []})
        
    try:
        ids = obtener_ids_favoritos(usuario_id)
        return jsonify({'cantidad': len(ids), 'ids': ids})
    except Exception as e:
        return jsonify({'cantidad': 0, 'ids': [], 'error': str(e)}), 500