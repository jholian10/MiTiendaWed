import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.db import obtener_conexion
from models.product_model import listar_productos, obtener_producto_por_id

# IMPORTANTE: Renombramos 'eliminar_producto' como 'eliminar_producto_db' 
from models.admin_product_model import insertar_producto, actualizar_producto, eliminar_producto as eliminar_producto_db

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

def es_admin():
    user = session.get('usuario')
    return user is not None and user.get('rol') == 'admin'

# =========================================================
# VISTA PRINCIPAL: DASHBOARD DEL ADMINISTRADOR
# =========================================================
@admin_blueprint.route('/')
def panel_admin():
    if not es_admin():
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.login'))
    
    productos = listar_productos()
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notificaciones ORDER BY fecha_creacion DESC LIMIT 5")
    notificaciones = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return render_template('admin/dashboard.html', productos=productos, notificaciones=notificaciones)

# =========================================================
# VISTA: GESTIÓN DE TODOS LOS USUARIOS RESTRISTRADOS
# =========================================================
@admin_blueprint.route('/usuarios')
def gestion_usuarios():
    if not es_admin():
        return redirect(url_for('auth.login'))
        
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, correo, rol FROM usuarios ORDER BY id DESC")
    lista_usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return render_template('admin/usuarios.html', usuarios=lista_usuarios)

# =========================================================
# ACCIÓN: REGISTRAR UN NUEVO PRODUCTO
# =========================================================
@admin_blueprint.route('/producto/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if not es_admin(): 
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio_compra = request.form.get('precio_compra')
        precio_venta = request.form.get('precio_venta')
        stock = int(request.form.get('stock', 0))
        stock_minimo = request.form.get('stock_minimo')
        imagen_url = request.form.get('imagen_url')
        descripcion = request.form.get('descripcion')
        
        # 1. Guardamos el producto en el inventario
        insertar_producto(nombre, precio_compra, precio_venta, stock, stock_minimo, imagen_url, descripcion)
        
        # 2. CREAMOS LA NOTIFICACIÓN DIRECTAMENTE DESDE PYTHON
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        if stock == 0:
            mensaje_alerta = f'¡Alerta de Inventario! El administrador registró el nuevo producto "{nombre}" SIN EXISTENCIAS (0 unidades).'
        else:
            mensaje_alerta = f'¡Nuevo Producto! El administrador registró "{nombre}" con {stock} unidades en el inventario.'
            
        cursor.execute("INSERT INTO notificaciones (mensaje, fecha_creacion) VALUES (%s, NOW())", (mensaje_alerta,))
        conexion.commit() # Guardamos los cambios de forma segura
        cursor.close()
        conexion.close()
        
        flash('Producto agregado con éxito al inventario.', 'success')
        return redirect(url_for('admin.panel_admin'))
        
    return render_template('admin/agregar.html')

# =========================================================
# ACCIÓN: EDITAR UN PRODUCTO EXISTENTE
# =========================================================
@admin_blueprint.route('/producto/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    if not es_admin(): 
        return redirect(url_for('auth.login'))
    
    producto = obtener_producto_por_id(id_producto)
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio_compra = request.form.get('precio_compra')
        precio_venta = request.form.get('precio_venta')
        stock = int(request.form.get('stock', 0))
        stock_minimo = int(request.form.get('stock_minimo', 0))
        imagen_url = request.form.get('imagen_url')
        descripcion = request.form.get('descripcion')
        
        # 1. Actualizamos los datos del producto
        actualizar_producto(id_producto, nombre, precio_compra, precio_venta, stock, stock_minimo, imagen_url, descripcion)
        
        # 2. CREAMOS LA NOTIFICACIÓN DESDE PYTHON DEPENDIENDO DEL STOCK
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        if stock == 0:
            mensaje_alerta = f'¡Alerta de Inventario! El producto "{nombre}" fue modificado y se ha quedado AGOTADO (0 unidades).'
        elif stock <= stock_minimo:
            mensaje_alerta = f'¡Atención! El producto "{nombre}" fue modificado y quedó por debajo del stock mínimo. Quedan {stock} unidades.'
        else:
            mensaje_alerta = f'¡Producto Actualizado! El administrador modificó los datos de "{nombre}".'
            
        cursor.execute("INSERT INTO notificaciones (mensaje, fecha_creacion) VALUES (%s, NOW())", (mensaje_alerta,))
        conexion.commit() # Aseguramos que se guarde en la BD
        cursor.close()
        conexion.close()
        
        flash('Producto actualizado con éxito.', 'success')
        return redirect(url_for('admin.panel_admin'))
        
    return render_template('admin/editar.html', producto=producto)

# =========================================================
# ACCIÓN: ELIMINAR UN PRODUCTO DEL INVENTARIO
# =========================================================
@admin_blueprint.route('/producto/eliminar/<int:id_producto>', methods=['POST'])
def eliminar_producto(id_producto):
    if not es_admin(): 
        return redirect(url_for('auth.login'))
    
    producto = obtener_producto_por_id(id_producto)
    nombre_producto = producto['nombre'] if producto else "Desconocido"
    
    eliminar_producto_db(id_producto)
    
    # OPCIONAL: También te crea notificación cuando eliminas algo
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO notificaciones (mensaje, fecha_creacion) VALUES (%s, NOW())", 
                   (f'¡Producto Eliminado! El administrador removió "{nombre_producto}" del sistema.',))
    conexion.commit()
    cursor.close()
    conexion.close()
    
    flash('Producto eliminado correctamente.', 'success')
    return redirect(url_for('admin.panel_admin'))

# =========================================================
# VISTA: VER TODAS LAS NOTIFICACIONES
# =========================================================
@admin_blueprint.route('/notificaciones')
def ver_notificaciones():
    if not es_admin():
        return redirect(url_for('auth.login'))
    
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notificaciones ORDER BY fecha_creacion DESC")
    todas = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return render_template('admin/notificaciones.html', notificaciones=todas)