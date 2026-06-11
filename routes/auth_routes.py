from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from models.auth_model import obtener_usuario_por_correo, registrar_usuario

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario' in session:
        if session['usuario']['rol'] == 'admin':
            return redirect(url_for('admin.panel_admin'))
        return redirect(url_for('products.index'))

    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')
        usuario = obtener_usuario_por_correo(correo)
        
        if usuario:
            coincide = check_password_hash(usuario['password_hash'], password)
            if coincide:
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
                    return redirect(url_for('admin.panel_admin'))
                return redirect(url_for('products.index'))
        
        flash('Correo electrónico o contraseña incorrectos.', 'danger')
        
    return render_template('auth/login.html')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        password = request.form.get('password')
        rol = request.form.get('rol', 'cliente')
        
        if not nombre or not correo or not password:
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('auth/register.html')
            
        exito = registrar_usuario(nombre, correo, password, rol)
        if exito:
            flash('Usuario registrado exitosamente. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('El correo electrónico ya se encuentra registrado.', 'danger')
            
    return render_template('auth/register.html')

@auth_blueprint.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('products.index'))