import os
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from werkzeug.utils import secure_filename

# Importaciones del modelo de productos y reseñas
from models.product_model import (
    listar_productos, 
    buscar_productos_por_nombre, 
    obtener_producto_por_id,
    guardar_reseña,
    obtener_reseñas_por_producto
) 
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
    termino_busqueda = request.args.get('q', '').strip()
    
    if termino_busqueda:
        bolsos = buscar_productos_por_nombre(termino_busqueda)
    else:
        bolsos = listar_productos()
        
    return render_template(
        'index.html', 
        productos=bolsos, 
        usuario_sesion=obtener_usuario_sesion(),
        busqueda=termino_busqueda
    )

# ==========================================
# VISTA: VER DETALLE DEL PRODUCTO (CON RESEÑAS CARGADAS)
# ==========================================
@product_blueprint.route('/producto/<int:producto_id>')
def ver_producto(producto_id):
    producto = obtener_producto_por_id(producto_id)
    
    if not producto:
        flash('El producto solicitado no está disponible o no existe.', 'warning')
        return redirect(url_for('products.index'))
    
    # Extraemos las reseñas asociadas a este producto específico
    reseñas = obtener_reseñas_por_producto(producto_id)
        
    return render_template(
        'ver_producto.html', 
        producto=producto, 
        usuario_sesion=obtener_usuario_sesion(),
        reseñas=reseñas
    )

# ==========================================
# RUTA NUEVA: PROCESAR EL FORMULARIO DE ENVÍO DE RESEÑA
# ==========================================
@product_blueprint.route('/producto/<int:producto_id>/reseña', methods=['POST'])
def enviar_reseña(producto_id):
    usuario_datos = obtener_usuario_sesion()
    
    if not usuario_datos:
        flash('Debes iniciar sesión para acceder al sistema de opiniones.', 'warning')
        return redirect(url_for('auth.login'))
        
    calificacion = request.form.get('calificacion')
    comentario = request.form.get('comentario', '').strip()
    
    if not calificacion:
        flash('Por favor selecciona una cantidad de estrellas válida.', 'warning')
        return redirect(url_for('products.ver_producto', producto_id=producto_id))
        
    # Guardamos el registro conectando producto, usuario, estrellas y comentario
    exito = guardar_reseña(
        producto_id=producto_id,
        usuario_id=usuario_datos['id'],
        calificacion=int(calificacion),
        comentario=comentario
    )
    
    if exito:
        flash('¡Tu reseña ha sido publicada con éxito!', 'success')
    else:
        flash('No se pudo guardar tu reseña en este momento. Inténtalo más tarde.', 'danger')
        
    return redirect(url_for('products.ver_producto', producto_id=producto_id))

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
# FORMULARIO DE EDICIÓN DE PERFIL
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
        file = request.files.get('foto_perfil')
        
        foto_url = usuario_datos.get('foto_perfil_url')
        
        if file and file.filename != '':
            ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
            if ext in ALLOWED_EXTENSIONS:
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                filename = secure_filename(f"user_{usuario_datos['id']}.{ext}")
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                foto_url = f"/{UPLOAD_FOLDER}/{filename}"
        
        try:
            datos_nuevos = actualizar_perfil_usuario(
                usuario_datos['id'], nombre, correo, telefono, direccion, city=ciudad, foto_url=foto_url
            )
            
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


# =========================================================================
# LÓGICA DE AGREGAR AL CARRITO INTERCEPTADA EN ESTE BLUEPRINT
# =========================================================================
@product_blueprint.route('/carrito/agregar/<int:producto_id>', methods=['POST'])
def agregar_carrito_directo(producto_id):
    usuario_datos = obtener_usuario_sesion()
    if not usuario_datos:
        flash('Debes iniciar sesión para gestionar tu carrito.', 'warning')
        return redirect(url_for('auth.login'))
        
    cantidad = int(request.form.get('cantidad', 1))
    
    # ---------------------------------------------------------------------
    # Tu código actual para meter el producto a la base de datos o sesión:
    # (Ejemplo: insertar_en_tabla_carrito(usuario_datos['id'], producto_id, cantidad))
    # ---------------------------------------------------------------------
    
    # SI PRESIONÓ "COMPRAR YA", REDIRIGE DIRECTO AL CARRITO
    if request.form.get('comprar_ahora') == 'true':
        return redirect(url_for('cart.ver_carrito'))
        
    # SI PRESIONÓ "AÑADIR AL CARRITO", REGRESA AL PRODUCTO CON MENSAJE DE ÉXITO
    flash(f'¡Se agregaron ({cantidad}) unidades con éxito!', 'success')
    return redirect(url_for('products.ver_producto', producto_id=producto_id))