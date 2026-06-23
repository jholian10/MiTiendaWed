import os
import random
import re
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

def enviar_correo_bienvenida(correo_destino, nombre_usuario):
    try:
        msg = Message(
            subject="¡Bienvenido a Dunaka! Descubre lo mejor para ti",
            sender=os.getenv('MAIL_USERNAME'),
            recipients=[correo_destino]
        )

        msg.html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="background-color: #f4f7fa; padding: 40px 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin: 0;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 24px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.08); border: 1px solid #eef2f6;">

                <div style="padding: 40px 30px 20px 30px; text-align: center; border-bottom: 1px solid #f1f5f9;">
                    <h1 style="color: #5d58ef; margin: 0; font-size: 32px; font-weight: 800; letter-spacing: -1px;">Dunaka</h1>
                </div>

                <div style="padding: 40px 40px 30px 40px; text-align: center;">
                    <h2 style="color: #0f172a; margin: 0 0 20px 0; font-size: 24px; font-weight: 700;">¡Hola, {nombre_usuario}! 👋</h2>
                    <p style="color: #475569; line-height: 1.8; font-size: 16px; margin: 0 0 25px 0;">
                        Tu cuenta ha sido creada exitosamente. Estamos emocionados de tenerte en nuestra comunidad.
                        En Dunaka, nos esforzamos por ofrecerte los mejores productos con una experience de compra inigualable.
                    </p>

                    <div style="background-color: #f8fafc; border-radius: 16px; padding: 25px; margin-bottom: 30px; text-align: left; border: 1px solid #e2e8f0;">
                        <h3 style="margin: 0 0 15px 0; color: #1e293b; font-size: 16px;">¿Qué puedes hacer ahora?</h3>
                        <ul style="margin: 0; padding-left: 20px; color: #64748b; font-size: 15px; line-height: 1.6;">
                            <li style="margin-bottom: 8px;">Explorar nuestro catálogo exclusivo.</li>
                            <li style="margin-bottom: 8px;">Guardar tus productos favoritos.</li>
                            <li>Gestionar tus pedidos de forma rápida.</li>
                        </ul>
                    </div>

                    <a href="http://127.0.0.1:5000/auth/login" style="display: inline-block; padding: 16px 45px; background-color: #5d58ef; color: #ffffff; text-decoration: none; border-radius: 50px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 15px rgba(93, 88, 239, 0.4);">
                        Empezar a Comprar
                    </a>
                </div>

                <div style="background-color: #f8fafc; padding: 30px; text-align: center; border-top: 1px solid #e2e8f0;">
                    <p style="color: #94a3b8; font-size: 13px; margin: 0 0 10px 0;">
                        ¿Necesitas ayuda? Contáctanos en nuestro panel de soporte.
                    </p>
                    <p style="color: #cbd5e1; font-size: 12px; margin: 0;">
                        &copy; 2026 Dunaka. Todos los derechos reservados.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        current_app.extensions['mail'].send(msg)
        print(f"DEBUG: Correo de bienvenida enviado a {correo_destino}")
    except Exception as e:
        print(f"ERROR: No se pudo enviar el correo de bienvenida: {e}")

def enviar_correo_recuperacion(correo_destino, codigo):
    try:
        msg = Message(
            subject="Código de Recuperación de Contraseña - Dunaka",
            sender=os.getenv('MAIL_USERNAME'),
            recipients=[correo_destino]
        )

        msg.html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <body style="background-color: #f4f7fa; padding: 40px 20px; font-family: -apple-system, sans-serif; margin: 0;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 24px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.08); border: 1px solid #eef2f6;">
                <div style="padding: 40px 30px 20px 30px; text-align: center;">
                    <h1 style="color: #5d58ef; margin: 0; font-size: 28px; font-weight: 800;">Dunaka</h1>
                </div>
                <div style="padding: 20px 40px 40px 40px; text-align: center;">
                    <h2 style="color: #0f172a; margin: 0 0 20px 0; font-size: 22px;">Recuperación de Contraseña</h2>
                    <p style="color: #475569; line-height: 1.6; font-size: 16px; margin: 0 0 30px 0;">
                        Hemos recibido una solicitud para restablecer tu contraseña. Ingresa el siguiente código de 6 dígitos para continuar:
                    </p>

                    <div style="background-color: #f1f5f9; padding: 20px; border-radius: 16px; display: inline-block; margin-bottom: 30px; border: 2px dashed #cbd5e1;">
                        <span style="font-size: 32px; font-weight: 800; color: #5d58ef; letter-spacing: 5px;">{codigo}</span>
                    </div>

                    <p style="color: #94a3b8; font-size: 14px; margin: 0;">
                        Si no solicitaste este cambio, puedes ignorar este correo de forma segura.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        current_app.extensions['mail'].send(msg)
        print(f"DEBUG: Correo de recuperación enviado a {correo_destino}")
    except Exception as e:
        print(f"ERROR: No se pudo enviar el correo de recuperación: {e}")

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        password_plana = request.form.get('password')

        if not correo or not password_plana:
            flash('Por favor, ingresa tu correo y contraseña.', 'warning')
            return render_template('auth/login.html')

        usuario = obtener_usuario_por_correo(correo)

        if usuario:
            hash_en_bd = usuario.get('password_hash')

            if not hash_en_bd or ":" not in hash_en_bd:
                flash('Error: Formato de contraseña inválido o cuenta de Google. Usa "Olvidé mi contraseña" o inicia con Google.', 'danger')
                return render_template('auth/login.html')

            try:
                if check_password_hash(hash_en_bd, password_plana):
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

                    if usuario['rol'] in ['admin', 'superadmin']:
                        flash(f"Bienvenido de nuevo, {usuario['nombre']}. Tienes acceso administrativo.", 'success')
                        return redirect(url_for('admin.panel_admin'))

                    flash(f"¡Qué gusto verte de nuevo, {usuario['nombre']}!", 'success')
                    return redirect(url_for('products.index'))
                else:
                    flash('Contraseña incorrecta. Intenta de nuevo.', 'danger')

            except ValueError:
                flash('Error al validar las credenciales. Contacta a soporte técnico.', 'danger')
        else:
            flash('No existe una cuenta asociada a este correo.', 'danger')

    return render_template('auth/login.html')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        password = request.form.get('password', '')

        if len(nombre) < 3:
            flash('El nombre debe tener al menos 3 caracteres.', 'warning')
            return render_template('auth/register.html')

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres por seguridad.', 'warning')
            return render_template('auth/register.html')

        rol = 'superadmin' if correo == "jholianmanuel10@gmail.com" else 'cliente'

        if registrar_usuario(nombre, correo, password, rol):
            enviar_correo_bienvenida(correo, nombre)
            flash('¡Registro exitoso! Por favor, inicia sesión.', 'success')
            return redirect(url_for('auth.login'))

        flash('Error al registrar. Es probable que el correo ya esté en uso.', 'danger')

    return render_template('auth/register.html')

@auth_blueprint.route('/recuperar', methods=['GET', 'POST'])
def recuperar_password():
    if request.method == 'POST':
        correo = request.form.get('correo', '').strip()

        if not correo:
            flash('Ingresa un correo electrónico.', 'warning')
            return render_template('auth/recuperar.html')

        usuario = obtener_usuario_por_correo(correo)

        if usuario:
            codigo = str(random.randint(100000, 999999))

            if guardar_codigo_recuperacion(correo, codigo):
                session['recuperacion_email'] = correo
                enviar_correo_recuperacion(correo, codigo)
                flash('Código de seguridad enviado a tu correo.', 'success')
                return redirect(url_for('auth.verificar_codigo'))
            else:
                flash('Ocurrió un error al generar el código en el sistema.', 'danger')
        else:
            flash('No encontramos una cuenta con ese correo electrónico.', 'danger')

    return render_template('auth/recuperar.html')

@auth_blueprint.route('/verificar', methods=['GET', 'POST'])
def verificar_codigo():
    if 'recuperacion_email' not in session:
        flash('Por favor, solicita un código de recuperación primero.', 'warning')
        return redirect(url_for('auth.recuperar_password'))

    if request.method == 'POST':
        codigo = request.form.get('codigo', '').strip()
        correo_en_sesion = session.get('recuperacion_email')

        if verificar_codigo_y_correo(correo_en_sesion, codigo):
            flash('Código verificado con éxito. Ingresa tu nueva contraseña.', 'success')
            return redirect(url_for('auth.reset_password_final'))

        flash('Código inválido o expirado. Verifica tu correo e intenta de nuevo.', 'danger')

    return render_template('auth/verificar.html')

@auth_blueprint.route('/reset-final', methods=['GET', 'POST'])
def reset_password_final():
    if 'recuperacion_email' not in session:
        flash('Sesión de recuperación inválida o caducada.', 'warning')
        return redirect(url_for('auth.recuperar_password'))

    if request.method == 'POST':
        nueva_password = request.form.get('password')
        confirmar_password = request.form.get('confirm_password')

        if len(nueva_password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'warning')
            return render_template('auth/nueva_password.html')

        if nueva_password != confirmar_password and confirmar_password:
            flash('Las contraseñas no coinciden.', 'warning')
            return render_template('auth/nueva_password.html')

        correo = session.pop('recuperacion_email', None)

        if correo and actualizar_password(correo, nueva_password):
            flash('¡Contraseña actualizada correctamente! Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Hubo un error al actualizar la base de datos.', 'danger')

    return render_template('auth/nueva_password.html')

@auth_blueprint.route('/login/google')
def google_login():
    return oauth.google.authorize_redirect(url_for('auth.google_callback', _external=True))

@auth_blueprint.route('/login/google/callback')
def google_callback():
    try:
        token = oauth.google.authorize_access_token()
        user_info = token.get('userinfo') or oauth.google.parse_id_token(token, nonce=token.get('nonce'))

        email = user_info.get('email')
        nombre = user_info.get('name', 'Usuario de Google')

        if not email:
            flash('Google no proporcionó un correo electrónico. No se pudo iniciar sesión.', 'danger')
            return redirect(url_for('auth.login'))

        usuario = obtener_usuario_por_correo(email)


        if not usuario:
            if registrar_usuario_oauth(nombre, email):
                enviar_correo_bienvenida(email, nombre)
                usuario = obtener_usuario_por_correo(email)


                if email == "jholianmanuel10@gmail.com":
                    try:
                        from database.db import obtener_conexion
                        conexion = obtener_conexion()
                        cursor = conexion.cursor()
                        cursor.execute("UPDATE usuarios SET rol = 'superadmin' WHERE correo = %s", (email,))
                        conexion.commit()
                        cursor.close()
                        conexion.close()

                        usuario = obtener_usuario_por_correo(email)
                    except Exception as db_err:
                        print(f"Error al auto-asignar superadmin en OAuth: {db_err}")
            else:
                flash('Error interno al crear tu cuenta con Google.', 'danger')
                return redirect(url_for('auth.login'))


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


        if usuario['rol'] in ['admin', 'superadmin']:
            flash(f"Bienvenido de nuevo, {usuario['nombre']}. Tienes acceso administrativo.", 'success')
            return redirect(url_for('admin.panel_admin'))

        flash(f'Bienvenido, {usuario["nombre"]}. Iniciaste sesión con Google.', 'success')
        return redirect(url_for('products.index'))

    except Exception as e:
        print(f"Error en Google Auth: {e}")
        flash('Ocurrió un error al conectarse con Google. Intenta más tarde.', 'danger')
        return redirect(url_for('auth.login'))
@auth_blueprint.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente. ¡Vuelve pronto!', 'info')
    return redirect(url_for('products.index'))