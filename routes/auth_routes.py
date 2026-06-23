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
    if request.method == 'POST':
        correo = request.form.get('correo')
        password_plana = request.form.get('password')
        
        usuario = obtener_usuario_por_correo(correo)
        
        if usuario:
            hash_en_bd = usuario.get('password_hash')
            
            # --- PROTECCIÓN CONTRA VALOR VACÍO O FORMATOS INVÁLIDOS ---
            if not hash_en_bd or ":" not in hash_en_bd:
                flash('Error de seguridad: El formato de la contraseña es inválido. Por favor, usa la recuperación de contraseña.', 'danger')
                return render_template('auth/login.html')

            try:
                # Validar la contraseña de forma segura
                if check_password_hash(hash_en_bd, password_plana):
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
                    
                    # Redirección según rol (Acepta 'admin' y el nuevo 'superadmin')
                    if usuario['rol'] in ['admin', 'superadmin']:
                        flash(f"Bienvenido, {usuario['nombre']}.", 'success')
                        return redirect(url_for('admin.panel_admin'))
                    
                    return redirect(url_for('products.index'))
                else:
                    flash('Credenciales incorrectas.', 'danger')
            except ValueError:
                flash('Error crítico al validar las credenciales. Contacta soporte.', 'danger')
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
            # --- ENVÍO DE CORREO DE BIENVENIDA ---
            try:
                msg = Message(
                    '¡Bienvenido a la comunidad Dunaka!',
                    sender=os.getenv('MAIL_USERNAME'),
                    recipients=[correo]
                )
                # Diseño profesional del correo en HTML
                msg.html = f"""
                <div style="font-family: 'Poppins', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 30px; border: 1px solid #f0f0f0; border-radius: 12px; background-color: #ffffff;">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <h1 style="color: #1a1a1a; margin: 0; font-size: 28px; letter-spacing: 1px;">Dunaka</h1>
                        <span style="font-size: 12px; color: #888888; text-transform: uppercase;">Panel de Gestión</span>
                    </div>
                    <hr style="border: 0; border-top: 1px solid #eeeeee; margin-bottom: 25px;">
                    <h2 style="color: #2c3e50; font-size: 20px;">¡Hola, {nombre}!</h2>
                    <p style="color: #555555; font-size: 15px; line-height: 1.6;">
                        Te damos una gran bienvenida a nuestra plataforma. Tu cuenta ha sido creada exitosamente como parte de nuestra comunidad artesanal.
                    </p>
                    <p style="color: #555555; font-size: 15px; line-height: 1.6;">
                        A partir de ahora podrás gestionar tus pedidos, guardar tus favoritos y explorar todo nuestro catálogo personalizado.
                    </p>
                    <div style="text-align: center; margin: 35px 0;">
                        <a href="{url_for('auth.login', _external=True)}" style="background-color: #000000; color: #ffffff; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: 500; font-size: 15px; display: inline-block;">Acceder a mi Cuenta</a>
                    </div>
                    <hr style="border: 0; border-top: 1px solid #eeeeee; margin-top: 30px;">
                    <p style="font-size: 12px; color: #aaaaaa; text-align: center; margin-top: 15px;">
                        Este es un correo automático, por favor no respondas a este mensaje.<br>&copy; 2026 Dunaka. Todos los derechos reservados.
                    </p>
                </div>
                """
                current_app.extensions['mail'].send(msg)
                flash('Usuario registrado exitosamente. Se ha enviado un correo de bienvenida.', 'success')
            except Exception as e:
                # Si el correo falla por configuración de red, el usuario igual fue creado sin tumbar la app
                print(f"Error enviando correo de bienvenida: {e}")
                flash('Usuario registrado exitosamente, pero hubo un inconveniente al enviar el correo.', 'warning')
                
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
    
    session['usuario'] = usuario
    return redirect(url_for('products.index'))

@auth_blueprint.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('products.index'))