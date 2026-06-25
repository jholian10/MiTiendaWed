import os
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from models.profile_model import actualizar_perfil_usuario
from models.auth_model import obtener_usuario_por_correo, actualizar_password
from models.auth_model import cambiar_password

profile_blueprint = Blueprint('profile', __name__, url_prefix='/perfil')

UPLOAD_FOLDER = 'static/uploads/perfiles'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def obtener_usuario_sesion():
    return session.get('usuario')

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

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
        contrasena_actual = request.form.get('contrasena_actual')
        nueva_contrasena = request.form.get('nueva_contrasena')
        confirmar_contrasena = request.form.get('confirmar_contrasena')

        foto_url = usuario_datos.get('foto_perfil_url')

        if file and file.filename != '':
            if archivo_permitido(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                destino = os.path.join(PROJECT_ROOT, UPLOAD_FOLDER)
                os.makedirs(destino, exist_ok=True)
                filename = secure_filename(f"user_{usuario_datos['id']}.{ext}")
                file.save(os.path.join(destino, filename))
                foto_url = f"/{UPLOAD_FOLDER}/{filename}"
            else:
                flash('Extensión de imagen no válida (usa PNG, JPG, JPEG o GIF).', 'danger')
                return render_template('editar_perfil.html', usuario=usuario_datos, usuario_sesion=usuario_datos)

        cambiar_contrasena = False
        if contrasena_actual or nueva_contrasena or confirmar_contrasena:
            if not contrasena_actual or not nueva_contrasena or not confirmar_contrasena:
                flash('Para cambiar la contraseña completa los tres campos.', 'danger')
                return render_template('editar_perfil.html', usuario=usuario_datos, usuario_sesion=usuario_datos)

            if nueva_contrasena != confirmar_contrasena:
                flash('La nueva contraseña no coincide con la confirmación.', 'danger')
                return render_template('editar_perfil.html', usuario=usuario_datos, usuario_sesion=usuario_datos)

            usuario_db = obtener_usuario_por_correo(usuario_datos['correo'])
            if not usuario_db or not check_password_hash(usuario_db['password_hash'], contrasena_actual):
                flash('La contraseña actual es incorrecta.', 'danger')
                return render_template('editar_perfil.html', usuario=usuario_datos, usuario_sesion=usuario_datos)

            cambiar_contrasena = True

        try:
            datos_nuevos = actualizar_perfil_usuario(
                usuario_datos['id'], nombre, correo, telefono, direccion, ciudad, foto_url
            )

            if not datos_nuevos:
                flash('No se pudieron guardar los cambios. Intenta de nuevo.', 'danger')
                return render_template('editar_perfil.html', usuario=usuario_datos, usuario_sesion=usuario_datos)

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

            if cambiar_contrasena:
                try:
                    actualizar_password(session['usuario']['correo'], nueva_contrasena)
                    flash('Contraseña actualizada correctamente.', 'success')
                except Exception as e:
                    flash(f'Error al cambiar la contraseña: {str(e)}', 'danger')
                    return render_template('editar_perfil.html', usuario=usuario_datos, usuario_sesion=usuario_datos)

            session.modified = True
            flash('Perfil actualizado con éxito.', 'success')
            return redirect(url_for('profile.ver_perfil'))

        except Exception as e:
            print(f"Error al actualizar el perfil: {str(e)}")
            import traceback
            print(traceback.format_exc())
            flash(f'Error al guardar los cambios: {str(e)}', 'danger')

    return render_template('editar_perfil.html', usuario=usuario_datos, usuario_sesion=usuario_datos)


@profile_blueprint.route('/cambiar-password', methods=['POST'])
def actualizar_password():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    actual = request.form.get('password_actual')
    nueva = request.form.get('nueva_password')
    confirmacion = request.form.get('confirmar_password')

    if nueva != confirmacion:
        flash('Las contraseñas nuevas no coinciden.', 'error')
        return redirect(url_for('profile.ver_perfil'))

    if cambiar_password(session['usuario']['id'], actual, nueva):
        flash('Contraseña actualizada con éxito.', 'success')
    else:
        flash('Error: La contraseña actual es incorrecta.', 'error')

    return redirect(url_for('profile.ver_perfil'))