import os
import hashlib
from werkzeug.utils import secure_filename # <--- AGREGA ESTA LÍNEA AQUÍ
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.db import obtener_conexion
from models.product_model import listar_productos, obtener_producto_por_id
from models.support_model import obtener_todos_los_mensajes

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
# VISTA: GESTIÓN DE TODOS LOS USUARIOS REGISTRADOS
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
# ACCIÓN: AGREGAR NUEVO USUARIO DESDE ADMIN
# =========================================================
@admin_blueprint.route('/usuarios/agregar', methods=['POST'])
def agregar_usuario():
    if not es_admin(): 
        return redirect(url_for('auth.login'))
    
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    password = request.form.get('password')
    rol = request.form.get('rol')
    
    # Encriptar la contraseña usando SHA-256
    password_enc = hashlib.sha256(password.encode('utf-8')).hexdigest()

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        # Consulta SQL limpia usando la columna password_hash
        query = "INSERT INTO usuarios (nombre, correo, password_hash, rol) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nombre, correo, password_enc, rol))
        conexion.commit()
        flash('Usuario agregado exitosamente.', 'success')
    except Exception as e:
        # Esto imprimirá el error exacto en tu consola/terminal de VS Code para saber qué falla
        print("\n" + "="*50)
        print(f"ERROR EN BASE DE DATOS AL AGREGAR USUARIO: {e}")
        print("="*50 + "\n")
        flash(f'Error en la base de datos: {e}', 'danger')
    finally:
        cursor.close()
        conexion.close()
        
    return redirect(url_for('admin.gestion_usuarios'))

# =========================================================
# ACCIÓN: ELIMINAR USUARIO DESDE ADMIN
# =========================================================
@admin_blueprint.route('/usuarios/eliminar/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    if not es_admin(): 
        return redirect(url_for('auth.login'))
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        conexion.commit()
        flash('Usuario eliminado del sistema.', 'success')
    except Exception as e:
        flash(f'Error al eliminar usuario: {e}', 'danger')
    finally:
        cursor.close()
        conexion.close()
        
    return redirect(url_for('admin.gestion_usuarios'))

# =========================================================
# ACCIÓN: CAMBIAR ROL DE USUARIO DESDE ADMIN
# =========================================================
@admin_blueprint.route('/usuarios/cambiar_rol', methods=['POST'])
def cambiar_rol_usuario():
    if not es_admin(): 
        return redirect(url_for('auth.login'))
    
    usuario_id = request.form.get('usuario_id')
    nuevo_rol = request.form.get('rol')
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("UPDATE usuarios SET rol = %s WHERE id = %s", (nuevo_rol, usuario_id))
        conexion.commit()
        flash('Rol actualizado correctamente.', 'success')
    except Exception as e:
        flash(f'Error al actualizar rol: {e}', 'danger')
    finally:
        cursor.close()
        conexion.close()
        
    return redirect(url_for('admin.gestion_usuarios'))

# =========================================================
# ACCIÓN: REGISTRAR UN NUEVO PRODUCTO
# =========================================================
@admin_blueprint.route('/producto/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if not es_admin(): return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        # Obtener datos
        nombre = request.form.get('nombre')
        precio_compra = request.form.get('precio_compra')
        precio_venta = request.form.get('precio_venta')
        stock = int(request.form.get('stock', 0))
        stock_minimo = int(request.form.get('stock_minimo', 5))
        descripcion = request.form.get('descripcion')
        
        # Guardar Imagen
        imagen_file = request.files.get('imagen')
        imagen_path = ""
        if imagen_file:
            filename = secure_filename(imagen_file.filename)
            imagen_file.save(os.path.join('static/uploads', filename))
            imagen_path = f'uploads/{filename}'
        
        # Insertar
        insertar_producto(nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_path)
        
        # Notificar
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO notificaciones (mensaje, fecha_creacion) VALUES (%s, NOW())", 
                       (f'Producto registrado: {nombre}',))
        conexion.commit()
        cursor.close()
        conexion.close()
        
        flash('Registrado con éxito', 'success')
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

# =========================================================
# VISTA: PANEL DE REPORTES
# =========================================================
@admin_blueprint.route('/reportes')
def ver_reportes():
    if not es_admin():
        return redirect(url_for('auth.login'))
    
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    # Total de productos
    cursor.execute("SELECT COUNT(*) as total FROM productos WHERE estado = 1")
    total_productos = cursor.fetchone()['total']
    
    # Stock bajo (menor a 5)
    cursor.execute("SELECT id, nombre, stock FROM productos WHERE stock < 5 AND estado = 1 ORDER BY stock ASC")
    stock_bajo = cursor.fetchall() or []
    
    # Productos más vendidos (si existe tabla de órdenes)
    cursor.execute("""
        SELECT p.id, p.nombre, COUNT(*) as cantidad_vendida, p.precio_venta
        FROM productos p
        LEFT JOIN carrito_detalles cd ON p.id = cd.producto_id
        GROUP BY p.id
        ORDER BY cantidad_vendida DESC
        LIMIT 10
    """)
    top_productos = cursor.fetchall() or []
    
    # Ingresos totales
    cursor.execute("""
        SELECT SUM(p.precio_venta * cd.cantidad) as ingresos_totales
        FROM productos p
        LEFT JOIN carrito_detalles cd ON p.id = cd.producto_id
    """)
    result = cursor.fetchone()
    ingresos_totales = result['ingresos_totales'] if result['ingresos_totales'] else 0
    
    # Mensajes de soporte pendientes
    cursor.execute("SELECT COUNT(*) as total FROM soporte WHERE estado = 'pendiente'")
    soporte_pendiente = cursor.fetchone()['total']
    
    cursor.close()
    conexion.close()
    
    reportes_data = {
        'total_productos': total_productos,
        'stock_bajo': stock_bajo,
        'top_productos': top_productos,
        'ingresos_totales': ingresos_totales,
        'soporte_pendiente': soporte_pendiente
    }
    
    return render_template('admin/reportes.html', reportes=reportes_data)