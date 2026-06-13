import os
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
from models.profile_model import actualizar_perfil_usuario

profile_blueprint = Blueprint('profile', __name__, url_prefix='/perfil')

UPLOAD_FOLDER = 'static/uploads/perfiles'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def obtener_usuario_sesion():
    return session.get('usuario')

def archivo_permitido(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@profile_blueprint.route('/')
def ver_perfil():
    usuario_datos = obtener_usuario_sesion()
    if not usuario_datos:
        flash('Debes iniciar sesión para acceder al perfil.', 'warning')
        return redirect(url_for('auth.login'))
    return render_template('perfil.html', usuario=usuario_datos, usuario_sesion=usuario_datos)

@profile_blueprint.route('/editar', methods=['GET', 'POST'])
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
        file = request.files.get('foto_perfil')
        
        foto_url = usuario_datos.get('foto_perfil_url')
        
        if file and file.filename != '':
            if archivo_permitido(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                filename = secure_filename(f"user_{usuario_datos['id']}.{ext}")
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                foto_url = f"/{UPLOAD_FOLDER}/{filename}"
            else:
                flash('Extensión de imagen no válida (usa PNG, JPG, JPEG o GIF).', 'danger')
                return render_template('editar_perfil.html', usuario=usuario_datos, usuario_sesion=usuario_datos)
        
        try:
            datos_nuevos = actualizar_perfil_usuario(
                usuario_datos['id'], nombre, correo, telefono, direccion, ciudad, foto_url
            )
            
            if isinstance(datos_nuevos, dict):
                session['usuario'] = {
                    'id': datos_nuevos.get('id', usuario_datos['id']),
                    'nombre': datos_nuevos.get('nombre', nombre),
                    'correo': datos_nuevos.get('correo', correo),
                    'rol': datos_nuevos.get('rol', usuario_datos['rol']),
                    'telefono': datos_nuevos.get('telefono', telefono),
                    'direccion': datos_nuevos.get('direccion', direccion),
                    'ciudad': datos_nuevos.get('ciudad', ciudad),
                    'foto_perfil_url': datos_nuevos.get('foto_perfil_url', foto_url)
                }
            else:
                session['usuario'] = {
                    'id': datos_nuevos[0],
                    'nombre': datos_nuevos[1],
                    'correo': datos_nuevos[2],
                    'rol': datos_nuevos[3],
                    'telefono': datos_nuevos[4],
                    'direccion': datos_nuevos[5],
                    'ciudad': datos_nuevos[6],
                    'foto_perfil_url': datos_nuevos[7]
                }
                
            session.modified = True
            flash('Perfil y foto actualizados con éxito.', 'success')
            return redirect(url_for('profile.ver_perfil'))
            
        except Exception as e:
            flash(f'Error al actualizar el perfil: {str(e)}', 'danger')

    return render_template('editar_perfil.html', usuario=usuario_datos, usuario_sesion=usuario_datos)