from flask import Blueprint, render_template, request, redirect, url_for
from models.product_model import (
    listar_productos, insertar_producto, obtener_producto_por_id, 
    actualizar_producto, eliminar_producto_por_id
)

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@admin_blueprint.route('/dashboard')
def dashboard():
    productos = listar_productos()
    return render_template('admin/dashboard.html', productos=productos)

@admin_blueprint.route('/producto/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        insertar_producto(
            request.form['nombre'],
            request.form['descripcion'] or None,
            request.form['precio_compra'],
            request.form['precio_venta'],
            request.form['stock'],
            request.form['stock_minimo'],
            request.form['imagen_url'] or None
        )
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/agregar.html')

@admin_blueprint.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    producto = obtener_producto_por_id(id)
    if request.method == 'POST':
        actualizar_producto(
            id,
            request.form['nombre'],
            request.form['descripcion'] or None,
            request.form['precio_compra'],
            request.form['precio_venta'],
            request.form['stock'],
            request.form['stock_minimo'],
            request.form['imagen_url'] or None
        )
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/editar.html', producto=producto)

@admin_blueprint.route('/producto/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    eliminar_producto_por_id(id)
    return redirect(url_for('admin.dashboard'))