from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models.support_model import guardar_mensaje_soporte

support_blueprint = Blueprint('support', __name__)

# RUTA 1: La página principal del chat
@support_blueprint.route('/support', methods=['GET'])
def index():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))
    
    nombre = session.get('usuario', {}).get('nombre', 'Cliente')
    return render_template('support.html', nombre_usuario=nombre)

# RUTA 2: La API que recibe los mensajes
@support_blueprint.route('/support/api', methods=['POST'])
def api_support():
    data = request.json
    mensaje = data.get('mensaje')
    usuario_id = session.get('usuario', {}).get('id')
    
    # Guardamos en la base de datos
    guardar_mensaje_soporte(usuario_id, mensaje)
    
    return jsonify({"respuesta": "Gracias por contactarnos. Un administrador revisará tu caso pronto."})