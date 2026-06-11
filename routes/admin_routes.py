import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from models.product_model import listar_productos, obtener_producto_por_id
from models.admin_product_model import insertar_producto, actualizar_producto, eliminar_producto

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

UPLOAD_FOLDER = 'static/uploads/productos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def es_admin():
    return session.get('usuario') and session['usuario'].get('rol') == 'admin'

@admin_blueprint.route('/')
def panel_admin():
    if not es_admin():
        flash('Acceso denegado. Se requieren permisos de administrador.', 'danger')
        return redirect(url_for('products.index'))
    productos = listar_productos()
    return render_template('admin/panel.html', productos=productos, usuario_sesion=session.get('usuario'))

@admin_blueprint.route('/producto/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if not es_admin():
        return redirect(url_for('products.index'))
        
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio_compra = float(request.form.get('precio_compra', 0))
        precio_venta = float(request.form.get('precio_venta', 0))
        stock = int(request.form.get('stock', 0))
        stock_minimo = int(request.form.get('stock_minimo', 0))
        file = request.files.get('imagen')
        
        imagen_url = '/static/images/default-product.png'
        if file and file.filename != '':
            ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
            if ext in ALLOWED_EXTENSIONS:
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                imagen_url = f"/{UPLOAD_FOLDER}/{filename}"
                
        insertar_producto(nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_url)
        flash('Producto agregado exitosamente.', 'success')
        return redirect(url_for('admin.panel_admin'))
        
    return render_template('admin/nuevo_producto.html', usuario_sesion=session.get('usuario'))

@admin_blueprint.route('/producto/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto_route(id_producto):
    if not es_admin():
        return redirect(url_for('products.index'))
        
    producto = obtener_producto_por_id(id_producto)
    if not producto:
        flash('Producto no encontrado.', 'warning')
        return redirect(url_for('admin.panel_admin'))
        
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio_compra = float(request.form.get('precio_compra', 0))
        precio_venta = float(request.form.get('precio_venta', 0))
        stock = int(request.form.get('stock', 0))
        stock_minimo = int(request.form.get('stock_minimo', 0))
        file = request.files.get('imagen')
        
        imagen_url = producto['imagen_url']
        if file and file.filename != '':
            ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
            if ext in ALLOWED_EXTENSIONS:
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                imagen_url = f"/{UPLOAD_FOLDER}/{filename}"
                
        actualizar_producto(id_producto, nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_url)
        flash('Producto actualizado correctamente.', 'success')
        return redirect(url_for('admin.panel_admin'))
        
    return render_template('admin/editar_producto.html', producto=producto, usuario_sesion=session.get('usuario'))

@admin_blueprint.route('/producto/eliminar/<int:id_producto>', methods=['POST'])
def eliminar_producto_route(id_producto):
    if not es_admin():
        return redirect(url_for('products.index'))
    eliminar_producto(id_producto)
    flash('Producto eliminado (baja lógica) correctamente.', 'success')
    return redirect(url_for('admin.panel_admin'))