import os
import random
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
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
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')
        usuario = obtener_usuario_por_correo(correo)
        if usuario and check_password_hash(usuario['password_hash'], password):
            session['usuario'] = usuario
            return redirect(url_for('products.index'))
        flash('Credenciales incorrectas.', 'danger')
    return render_template('auth/login.html')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if registrar_usuario(request.form.get('nombre'), request.form.get('correo'), request.form.get('password')):
            flash('Usuario registrado.', 'success')
            return redirect(url_for('auth.login'))
        flash('Error al registrar.', 'danger')
    return render_template('auth/register.html')

@auth_blueprint.route('/recuperar', methods=['GET', 'POST'])
def recuperar_password():
    if request.method == 'POST':
        correo = request.form.get('correo')
        if obtener_usuario_por_correo(correo):
            codigo = str(random.randint(100000, 999999))
            guardar_codigo_recuperacion(correo, codigo)
            session['recuperacion_email'] = correo
            flash(f'Tu código es: {codigo}', 'info')
            return redirect(url_for('auth.verificar_codigo'))
        flash('Correo no encontrado.', 'danger')
    return render_template('auth/recuperar.html')

@auth_blueprint.route('/verificar', methods=['GET', 'POST'])
def verificar_codigo():
    if request.method == 'POST':
        if verificar_codigo_y_correo(session.get('recuperacion_email'), request.form.get('codigo')):
            return redirect(url_for('auth.reset_password_final'))
        flash('Código inválido o expirado.', 'danger')
    return render_template('auth/verificar.html')

@auth_blueprint.route('/reset-final', methods=['GET', 'POST'])
def reset_password_final():
    if request.method == 'POST':
        correo = session.pop('recuperacion_email', None)
        if correo:
            actualizar_password(correo, request.form.get('password'))
            flash('Contraseña actualizada.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('auth/nueva_password.html')

@auth_blueprint.route('/login/google')
def google_login():
    return oauth.google.authorize_redirect(url_for('auth.google_callback', _external=True))

@auth_blueprint.route('/login/google/callback')
def google_callback():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token)
    email = user_info.get('email')
    usuario = obtener_usuario_por_correo(email)
    if not usuario:
        registrar_usuario_oauth(user_info.get('name', 'Usuario'), email)
        usuario = obtener_usuario_por_correo(email)
    session['usuario'] = usuario
    return redirect(url_for('products.index'))

@auth_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('products.index'))