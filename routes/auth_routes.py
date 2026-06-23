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
    """Inicializa la configuración de Google OAuth."""
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

# ==========================================
# PLANTILLAS DE CORREO Y FUNCIONES DE ENVÍO
# ==========================================

def enviar_correo_bienvenida(correo_destino, nombre_usuario):
    """
    Envía un correo de bienvenida con diseño HTML premium.
    Utiliza el contexto de la aplicación actual para evitar errores fuera de contexto.
    """
    try:
        msg = Message(
            subject="¡Bienvenido a Dunaka! Descubre lo mejor para ti",
            sender=os.getenv('MAIL_USERNAME'),
            recipients=[correo_destino]
        )
        
        # Diseño HTML Moderno y Responsivo
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
                        En Dunaka, nos esforzamos por ofrecerte los mejores productos con una experiencia de compra inigualable.
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
        # IMPORTANTE: Usamos current_app para evitar problemas de contexto
        current_app.extensions['mail'].send(msg)
        print(f"DEBUG: Correo de bienvenida enviado a {correo_destino}")
    except Exception as e:
        print(f"ERROR: No se pudo enviar el correo de bienvenida: {e}")

def enviar_correo_recuperacion(correo_destino, codigo):
    """
    Envía el código de seguridad de 6 dígitos con diseño HTML premium.
    """
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

# ==========================================
# RUTAS DE AUTENTICACIÓN
# ==========================================

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Maneja el inicio de sesión tradicional."""
    if request.method == 'POST':
        correo = request.form.get('correo')
        password_plana = request.form.get('password')
        
        # Validar entradas vacías
        if not correo or not password_plana:
            flash('Por favor, ingresa tu correo y contraseña.', 'warning')
            return render_template('auth/login.html')

        usuario = obtener_usuario_por_correo(correo)
        
        if usuario:
            hash_en_bd = usuario.get('password_hash')
            
            # Protección contra contraseñas generadas por OAuth o formatos inválidos
            if not hash_en_bd or ":" not in hash_en_bd:
                flash('Error: Formato de contraseña inválido o cuenta de Google. Usa "Olvidé mi contraseña" o inicia con Google.', 'danger')
                return render_template('auth/login.html')

            try:
                # Validar la contraseña de forma segura
                if check_password_hash(hash_en_bd, password_plana):
                    
                    # Guardamos los datos completos en la sesión
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
                    
                    # Redirección según rol (Admin/Superadmin vs Cliente)
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
    """Maneja el registro de nuevos usuarios."""
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        password = request.form.get('password', '')
        
        # Validaciones de seguridad básicas
        if len(nombre) < 3:
            flash('El nombre debe tener al menos 3 caracteres.', 'warning')
            return render_template('auth/register.html')
            
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres por seguridad.', 'warning')
            return render_template('auth/register.html')
        
        # Asignación de Rol
        rol = 'superadmin' if correo == "jholianmanuel10@gmail.com" else 'cliente'
        
        # Intentar registrar al usuario en BD
        if registrar_usuario(nombre, correo, password, rol):
            
            # --- ENVÍO DE CORREO DE BIENVENIDA ---
            # Ahora la función está bien ubicada, solo se ejecuta si el registro fue exitoso
            enviar_correo_bienvenida(correo, nombre)
            
            flash('¡Registro exitoso! Por favor, inicia sesión.', 'success')
            return redirect(url_for('auth.login'))
        
        flash('Error al registrar. Es probable que el correo ya esté en