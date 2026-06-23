from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models.support_model import (
    guardar_mensaje_soporte,
    obtener_clientes_soporte,
    obtener_historial_chat,
    guardar_respuesta_admin
)

support_blueprint = Blueprint('support', __name__)

@support_blueprint.route('/support', methods=['GET'])
def index():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))
    
    usuario_id = session.get('usuario', {}).get('id')
    nombre = session.get('usuario', {}).get('nombre', 'Cliente')
    historial = obtener_historial_chat(usuario_id)
    
    return render_template('support.html', nombre_usuario=nombre, mensajes=historial)

@support_blueprint.route('/support/api', methods=['POST'])
def api_support():
    if 'usuario' not in session:
        return jsonify({"error": "No autorizado"}), 403
    
    data = request.json
    mensaje = data.get('mensaje')
    usuario_id = session.get('usuario', {}).get('id')
    
    if not mensaje or not mensaje.strip():
        return jsonify({"error": "Mensaje vacío"}), 400
    
    guardar_mensaje_soporte(usuario_id, mensaje)
    
    return jsonify({"respuesta": "Gracias por contactarnos. Un administrador revisará tu caso pronto."})

@support_blueprint.route('/admin/soporte', methods=['GET'])
def admin_soporte_panel():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))
    
    usuario_info = session.get('usuario', {})
    
    # CORRECCIÓN: Permite acceso si el rol es admin o superadmin
    if usuario_info.get('rol') not in ['admin', 'superadmin']:
        return redirect(url_for('auth.login'))
    
    clientes = obtener_clientes_soporte()
    return render_template('admin/admin_mensajes.html', clientes=clientes)

@support_blueprint.route('/admin/soporte/historial/<int:usuario_id>', methods=['GET'])
def api_historial_chat(usuario_id):
    if 'usuario' not in session:
        return jsonify({"error": "No autorizado"}), 403
    
    usuario_info = session.get('usuario', {})
    
    # CORRECCIÓN: Permite acceso si el rol es admin o superadmin
    if usuario_info.get('rol') not in ['admin', 'superadmin']:
        return jsonify({"error": "Acceso denegado. Se requiere nivel de administrador."}), 403
    
    historial = obtener_historial_chat(usuario_id)
    datos = [dict(msg) if hasattr(msg, 'keys') else msg for msg in (historial or [])]
    return jsonify(datos)

@support_blueprint.route('/admin/soporte/responder', methods=['POST'])
def api_responder_soporte():
    if 'usuario' not in session:
        return jsonify({"error": "No autorizado"}), 403
    
    usuario_info = session.get('usuario', {})
    
    # CORRECCIÓN: Permite acceso si el rol es admin o superadmin
    if usuario_info.get('rol') not in ['admin', 'superadmin']:
        return jsonify({"error": "Solo los administradores pueden responder."}), 403
    
    data = request.json
    usuario_id = data.get('usuario_id')
    mensaje = data.get('mensaje')
    
    if not usuario_id or not mensaje or not mensaje.strip():
        return jsonify({"status": "error", "mensaje": "Datos incompletos"}), 400
    
    if guardar_respuesta_admin(usuario_id, mensaje):
        return jsonify({"status": "success", "mensaje": "Enviado"})
    return jsonify({"status": "error", "mensaje": "Fallo al enviar"}), 500