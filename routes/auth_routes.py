from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from models.user_model import obtener_usuario_por_correo, registrar_usuario

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario' in session:
        if session['usuario']['rol'] == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('products.index'))

    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')
        
        print("\n=== INTENTO DE INICIO DE SESIÓN ===")
        print(f"-> Correo recibido del HTML: '{correo}'")
        print(f"-> Contraseña recibida (longitud): {len(password) if password else 0}")
        
        usuario = obtener_usuario_por_correo(correo)
        print(f"-> Usuario encontrado en BD: {True if usuario else False}")
        
        if usuario:
            print(f"   [-] Nombre en BD: {usuario.get('nombre')}")
            print(f"   [-] Rol en BD: {usuario.get('rol')}")
            
            coincide = check_password_hash(usuario['password_hash'], password)
            print(f"-> ¿La contraseña coincide con el Hash?: {coincide}")
            
            if coincide:
                # SE INCLUYEN LOS NUEVOS CAMPOS EN LA SESIÓN DE FLASK
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
                print("-> Sesión creada con éxito con datos de perfil. Redirigiendo...")
                print("===================================\n")
                
                if usuario['rol'] == 'admin':
                    return redirect(url_for('admin.dashboard'))
                return redirect(url_for('products.index'))
            else:
                print("-> ERROR: Contraseña inválida frente al Hash guardado.")
        else:
            print("-> ERROR: El correo electrónico no existe en la base de datos.")
        print("===================================\n")
        
        flash('Correo electrónico o contraseña incorrectos.', 'danger')
        
    return render_template('auth/login.html')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """Endpoint para que Python registre usuarios encriptando las contraseñas automáticamente."""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        password = request.form.get('password')
        rol = request.form.get('rol', 'cliente') # Por defecto se registra como cliente
        
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
    session.pop('usuario_sesion', None) # Limpieza total de llaves alternativas
    return redirect(url_for('products.index'))