from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models.product_model import (
    listar_productos,
    buscar_productos_por_nombre,
    obtener_producto_por_id, verificar_compra_usuario
)
from models.review_model import guardar_reseña, obtener_reseñas_por_producto

product_blueprint = Blueprint('products', __name__)

def obtener_usuario_sesion():
    return session.get('usuario')

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

@product_blueprint.route('/producto/<int:producto_id>')
def ver_producto(producto_id):
    producto = obtener_producto_por_id(producto_id)
    if not producto:
        flash('El producto solicitado no está disponible o no existe.', 'warning')
        return redirect(url_for('products.index'))
    
    usuario_sesion = obtener_usuario_sesion()
    reseñas = obtener_reseñas_por_producto(producto_id)
    
    # 1. Inicializamos la variable en False por defecto
    ha_comprado = False
    
    # 2. Si hay un usuario logueado, verificamos si ya compró este artículo
    if usuario_sesion:
        # Pasamos el ID del usuario y el ID del producto a una función verificadora
        ha_comprado = verificar_compra_usuario(usuario_sesion['id'], producto_id)
    
    return render_template(
        'ver_producto.html',
        producto=producto,
        usuario_sesion=usuario_sesion,
        reseñas=reseñas,
        ha_comprado=ha_comprado  # 3. Enviamos el resultado al HTML
    )

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
