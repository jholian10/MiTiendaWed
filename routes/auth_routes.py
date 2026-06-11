import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from authlib.integrations.flask_client import OAuth
from models.auth_model import obtener_usuario_por_correo, registrar_usuario, registrar_usuario_oauth

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

# --- FUNCIÓN REPARADA: REGISTRO ---
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        password = request.form.get('password')
        rol = request.form.get('rol', 'cliente')
        
        exito = registrar_usuario(nombre, correo, password, rol)
        if exito:
            flash('Usuario registrado exitosamente. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('El correo electrónico ya se encuentra registrado o hubo un error.', 'danger')
            
    return render_template('auth/register.html')

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