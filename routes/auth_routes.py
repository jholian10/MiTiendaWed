import os
import random
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from flask_mail import Message
from werkzeug.security import check_password_hash
from authlib.integrations.flask_client import OAuth
from models.auth_model import (
    obtener_usuario_por_correo, registrar_usuario, registrar_usuario_oauth,
    guardar_codigo_recuperacion, verificar_codigo_y_correo, actualizar_password
)

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')
oauth = OAuth()

def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    Ruta reparada: Sin argumentos. Los datos se extraen de request.form.
    """
    if request.method == 'POST':
        correo = request.form.get('correo')
        password_plana = request.form.get('password')
        
        usuario = obtener_usuario_por_correo(correo)
        
        # Validar existencia y hash de contraseña
        if usuario and check_password_hash(usuario['password_hash'], password_plana):
            # Guardamos los campos completos en la sesión para mostrar el perfil correctamente
            session['usuario'] = {
                'id': usuario['id'],
                'nombre': usuario['nombre'],
                'correo': usuario['correo'],
                'rol': usuario['rol'],
                'telefono': usuario.get('telefono'),
                'direccion': usuario.get('direccion'),
                'ciudad': usuario.get('ciudad'),
                'foto_perfil_url': usuario.get('foto_perfil_url')
            }
            
            if usuario['rol'] == 'admin':
                flash('Bienvenido, administrador.', 'success')
                return redirect(url_for('admin.panel_admin'))
            
            return redirect(url_for('products.index'))
        else:
            flash('Credenciales incorrectas.', 'danger')
            
    return render_template('auth/login.html')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        password = request.form.get('password')
        if registrar_usuario(nombre, correo, password):
            flash('Usuario registrado exitosamente.', 'success')
            return redirect(url_for('auth.login'))
        flash('Error al registrar usuario.', 'danger')
    return render_template('auth/register.html')

@auth_blueprint.route('/recuperar', methods=['GET', 'POST'])
def recuperar_password():
    if request.method == 'POST':
        correo = request.form.get('correo')
        usuario = obtener_usuario_por_correo(correo)
        if usuario:
            codigo = str(random.randint(100000, 999999))
            guardar_codigo_recuperacion(correo, codigo)
            session['recuperacion_email'] = correo
            try:
                msg = Message('Tu código de recuperación', sender=os.getenv('MAIL_USERNAME'), recipients=[correo])
                msg.body = f'Tu código es: {codigo}'
                current_app.extensions['mail'].send(msg)
                flash('Código enviado a tu correo.', 'success')
                return redirect(url_for('auth.verificar_codigo'))
            except Exception as e:
                flash(f'Error al enviar correo: {e}', 'danger')
        else:
            flash('Correo no encontrado.', 'danger')
    return render_template('auth/recuperar.html')

@auth_blueprint.route('/verificar', methods=['GET', 'POST'])
def verificar_codigo():
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        if verificar_codigo_y_correo(session.get('recuperacion_email'), codigo):
            return redirect(url_for('auth.reset_password_final'))
        flash('Código inválido.', 'danger')
    return render_template('auth/verificar.html')

@auth_blueprint.route('/reset-final', methods=['GET', 'POST'])
def reset_password_final():
    if request.method == 'POST':
        correo = session.pop('recuperacion_email', None)
        if correo:
            actualizar_password(correo, request.form.get('password'))
            flash('Contraseña actualizada correctamente.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('auth/nueva_password.html')

@auth_blueprint.route('/login/google')
def google_login():
    return oauth.google.authorize_redirect(url_for('auth.google_callback', _external=True))

@auth_blueprint.route('/login/google/callback')
def google_callback():
    token = oauth.google.authorize_access_token()
    user_info = token.get('userinfo') or oauth.google.parse_id_token(token, nonce=token.get('nonce'))
    email = user_info.get('email')
    usuario = obtener_usuario_por_correo(email)
    if not usuario:
        registrar_usuario_oauth(user_info.get('name', 'Usuario'), email)
        usuario = obtener_usuario_por_correo(email)
    
    # Asegurar sesión también para login social
    session['usuario'] = usuario
    return redirect(url_for('products.index'))

@auth_blueprint.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('products.index'))