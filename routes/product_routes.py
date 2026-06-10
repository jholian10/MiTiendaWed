import os
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
# Se añade la importación de buscar_productos_por_nombre para gestionar los filtros
from models.product_model import listar_productos, buscar_productos_por_nombre 
from models.user_model import actualizar_perfil_usuario 

# CRÍTICO: Dejar sin url_prefix para que controle la página de inicio principal
product_blueprint = Blueprint('products', __name__)

UPLOAD_FOLDER = 'static/uploads/perfiles'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def obtener_usuario_sesion():
    return session.get('usuario')

# ==========================================
# PUNTO DE ENTRADA PRINCIPAL (PÁGINA DE INICIO CON BÚSQUEDA)
# ==========================================
@product_blueprint.route('/')
def index():
    # Captura el término ingresado en la barra de búsqueda (ej. /?q=bolso)
    termino_busqueda = request.args.get('q', '').strip()
    
    if termino_busqueda:
        # Filtra los productos que coincidan con la búsqueda
        bolsos = buscar_productos_por_nombre(termino_busqueda)
    else:
        # Carga el catálogo completo si no hay filtro activo
        bolsos = listar_productos()
        
    return render_template(
        'index.html', 
        productos=bolsos, 
        usuario_sesion=obtener_usuario_sesion(),
        busqueda=termino_busqueda  # Mantiene el texto dentro del input del buscador
    )

# ==========================================
# VISTA DE PERFIL (SOLO LECTURA)
# ==========================================
@product_blueprint.route('/perfil')
def perfil():
    usuario_datos = obtener_usuario_sesion()
    if not usuario_datos:
        flash('Debes iniciar sesión para acceder al perfil.', 'warning')
        return redirect(url_for('auth.login'))
    return render_template('perfil.html', usuario=usuario_datos, usuario_sesion=usuario_datos)

# ==========================================
# FORMULARIO DE EDICIÓN
# ==========================================
@product_blueprint.route('/perfil/editar', methods=['GET', 'POST'])
def editar_perfil():
    usuario_datos = obtener_usuario_sesion()
    if not usuario_datos:
        flash('Debes iniciar sesión para editar tu perfil.', 'warning')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        ciudad = request.form.get('ciudad')
        file = request.files.get('foto_perfil') # Captura el archivo del formulario
        
        # Mantiene la foto actual por si el usuario no sube una nueva
        foto_url = usuario_datos.get('foto_perfil_url')
        
        # Si el usuario seleccionó un archivo, lo procesamos y guardamos
        if file and file.filename != '':
            ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
            if ext in ALLOWED_EXTENSIONS:
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                # Guarda la foto con un nombre único basado en el ID del usuario
                filename = secure_filename(f"user_{usuario_datos['id']}.{ext}")
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                foto_url = f"/{UPLOAD_FOLDER}/{filename}" # Nueva ruta de la foto
        
        try:
            # CORRECCIÓN AQUÍ: Se pasa 'ciudad' correctamente a tu modelo de base de datos
            datos_nuevos = actualizar_perfil_usuario(
                usuario_datos['id'], nombre, correo, telefono, direccion, ciudad, foto_url
            )
            
            # Actualiza los datos de la sesión de Flask inmediatamente
            session['usuario'] = {
                'id': datos_nuevos[0] if isinstance(datos_nuevos, (tuple, list)) else datos_nuevos.get('id'),
                'nombre': datos_nuevos[1] if isinstance(datos_nuevos, (tuple, list)) else datos_nuevos.get('nombre'),
                'correo': datos_nuevos[2] if isinstance(datos_nuevos, (tuple, list)) else datos_nuevos.get('correo'),
                'rol': datos_nuevos[3] if isinstance(datos_nuevos, (tuple, list)) else datos_nuevos.get('rol'),
                'telefono': datos_nuevos[4] if isinstance(datos_nuevos, (tuple, list)) else datos_nuevos.get('telefono'),
                'direccion': datos_nuevos[5] if isinstance(datos_nuevos, (tuple, list)) else datos_nuevos.get('direccion'),
                'ciudad': datos_nuevos[6] if isinstance(datos_nuevos, (tuple, list)) else datos_nuevos.get('ciudad'),
                'foto_perfil_url': datos_nuevos[7] if isinstance(datos_nuevos, (tuple, list)) else datos_nuevos.get('foto_perfil_url')
            }
            
            flash('Perfil y foto actualizados con éxito.', 'success')
            return redirect(url_for('products.perfil'))
        except Exception as e:
            flash(f'Error al actualizar el perfil: {str(e)}', 'danger')

    return render_template('editar_perfil.html', usuario=usuario_datos, usuario_sesion=usuario_datos)