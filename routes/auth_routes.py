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
        
        # 1. Determinación de Rol (Lógica de negocio clara)
        # Si es tu correo, eres superadmin, si no, cliente.
        rol = 'superadmin' if correo == "jholianmanuel10@gmail.com" else 'cliente'
        
        # 2. Intentar registrar (pasando el nuevo parámetro rol)
        # NOTA: Asegúrate de que registrar_usuario en models/auth_model.py acepte 4 argumentos
        if registrar_usuario(nombre, correo, password, rol):
            
            # 3. Notificación (Si falla, no bloquea el registro del usuario)
            try:
                enviar_correo_bienvenida_dunaka(correo, nombre)
            except Exception as e:
                print(f"Error enviando correo: {e}")
            
            flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        
        flash('Error al registrar. Verifica si el correo ya está en uso.', 'danger')
            
    return render_template('auth/register.html')

def enviar_correo_bienvenida_dunaka(correo, nombre):
    msg = Message("¡Bienvenido a Dunaka!",
                  sender=os.getenv('MAIL_USERNAME'),
                  recipients=[correo])
    
    # Aquí puedes pegar el diseño HTML que definimos antes
    msg.html = f"""
    <div style="background-color: #f4f7fa; padding: 40px 20px; font-family: sans-serif;">
        <div style="max-width: 600px; margin: auto; background: #ffffff; border-radius: 20px; text-align: center; padding: 40px;">
            <h1 style="color: #5d58ef;">Dunaka</h1>
            <h2>¡Hola, {nombre}!</h2>
            <p>Tu cuenta ha sido creada con éxito. Estamos felices de tenerte.</p>
            <a href="{url_for('auth.login', _external=True)}" style="padding: 15px 30px; background-color: #5d58ef; color: #ffffff; text-decoration: none; border-radius: 50px;">
                Ir a la Tienda
            </a>
        </div>
    </div>
    """
    current_app.extensions['mail'].send(msg)

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

def enviar_correo_bienvenida(correo_destino, nombre_usuario):
    msg = Message("¡Bienvenido a DUYNBACA!",
                  sender=os.environ.get('MAIL_USERNAME'),
                  recipients=[correo_destino])
    
    msg.html = f"""
    <div style="background-color: #f4f7fa; padding: 40px 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
    <div style="max-width: 600px; margin: auto; background: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #eef2f6;">
        
        <div style="padding: 40px 30px 20px 30px; text-align: center;">
            <h1 style="color: #5d58ef; margin: 0; font-size: 28px; font-weight: 700;">Dunaka</h1>
        </div>

        <div style="padding: 20px 40px 40px 40px; text-align: center;">
            <h2 style="color: #1e293b; margin: 0 0 15px 0; font-size: 24px;">¡Hola, {nombre_usuario}!</h2>
            <p style="color: #64748b; line-height: 1.6; font-size: 16px; margin: 0 0 30px 0;">
                Gracias por unirte a Dunaka. Estamos muy emocionados de tenerte aquí.
                Explora nuestro catálogo y descubre piezas únicas que hemos seleccionado para ti.
            </p>

            <a href="http://192.168.1.8:3000" style="display: inline-block; padding: 16px 40px; background-color: #5d58ef; color: #ffffff; text-decoration: none; border-radius: 50px; font-weight: 600; font-size: 16px; transition: background 0.3s ease;">
                Ir a la Tienda
            </a>
        </div>

        <div style="background-color: #fcfcfc; padding: 25px; text-align: center; border-top: 1px solid #f1f5f9;">
            <p style="color: #94a3b8; font-size: 12px; margin: 0;">
                ¿Tienes alguna pregunta? Contáctanos a través de nuestro panel de soporte.<br>
                &copy; 2026 Dunaka. Todos los derechos reservados.
            </p>
        </div>
    </div>
</div>
    """
    mail.send(msg)

try:
    enviar_correo_bienvenida(correo, nombre)
except Exception as e:
    print(f"Error enviando correo: {e}")