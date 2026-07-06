import os
import smtplib
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.db import obtener_conexion
from models.product_model import listar_productos, obtener_producto_por_id
from models.support_model import obtener_todos_los_mensajes
from models.notificaciones_service import enviar_alerta_stock_email
from models.admin_product_model import insertar_producto, actualizar_producto, eliminar_producto as eliminar_producto_db

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')


def es_admin():
    """Verifica si el usuario en sesión es administrador o superadministrador."""
    user = session.get('usuario')
    return user is not None and user.get('rol') in ['admin', 'superadmin']

def es_superadmin():
    """Verifica si el usuario en sesión es específicamente un superadministrador."""
    user = session.get('usuario')
    return user is not None and user.get('rol') == 'superadmin'




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




@admin_blueprint.route('/usuarios/agregar', methods=['POST'])
def agregar_usuario():
    if not es_admin():
        return redirect(url_for('auth.login'))

    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    password = request.form.get('password')
    rol = request.form.get('rol')

    if rol == 'superadmin' and not es_superadmin():
        flash('No tienes permisos para crear un Super Administrador.', 'danger')
        return redirect(url_for('admin.gestion_usuarios'))

    password_enc = generate_password_hash(password)

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = "INSERT INTO usuarios (nombre, correo, password_hash, rol) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nombre, correo, password_enc, rol))
        conexion.commit()
        flash('Usuario agregado exitosamente.', 'success')
    except Exception as e:
        print("\n" + "="*50)
        print(f"ERROR EN BASE DE DATOS AL AGREGAR USUARIO: {e}")
        print("="*50 + "\n")
        flash(f'Error en la base de datos: {e}', 'danger')
    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for('admin.gestion_usuarios'))




@admin_blueprint.route('/usuarios/eliminar/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    if not es_admin():
        return redirect(url_for('auth.login'))

    if id == 1:
        flash('¡Operación bloqueada! El Super Administrador principal no puede ser eliminado.', 'danger')
        return redirect(url_for('admin.gestion_usuarios'))

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (id,))
        usuario_a_borrar = cursor.fetchone()

        if usuario_a_borrar and usuario_a_borrar['rol'] == 'superadmin':
            flash('¡Operación bloqueada! No está permitido eliminar cuentas de Super Administrador.', 'danger')
            return redirect(url_for('admin.gestion_usuarios'))

        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        conexion.commit()
        flash('Usuario eliminado del sistema.', 'success')
    except Exception as e:
        flash(f'Error al eliminar usuario: {e}', 'danger')
    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for('admin.gestion_usuarios'))




@admin_blueprint.route('/usuarios/cambiar_rol', methods=['POST'])
def cambiar_rol_usuario():
    if not es_admin():
        return redirect(url_for('auth.login'))

    usuario_id = int(request.form.get('usuario_id'))
    nuevo_rol = request.form.get('rol')

    if usuario_id == 1 or nuevo_rol == 'superadmin':
        if not es_superadmin():
            flash('No tienes permisos para modificar este rol ni ascender usuarios a Super Admin.', 'danger')
            return redirect(url_for('admin.gestion_usuarios'))

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




@admin_blueprint.route('/producto/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if not es_admin(): return redirect(url_for('auth.login'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio_compra = request.form.get('precio_compra')
        precio_venta = request.form.get('precio_venta')
        stock = int(request.form.get('stock', 0))
        stock_minimo = int(request.form.get('stock_minimo', 5))
        descripcion = request.form.get('descripcion')

        imagen_url = request.form.get('imagen_url')
        imagen_file = request.files.get('imagen')

        imagen_final = ""
        if imagen_file and imagen_file.filename != '':
            os.makedirs('static/uploads', exist_ok=True)
            filename = secure_filename(imagen_file.filename)
            imagen_file.save(os.path.join('static/uploads', filename))
            imagen_final = f'/static/uploads/{filename}'
        elif imagen_url and imagen_url.strip() != "":
            imagen_final = imagen_url.strip()

        insertar_producto(nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_final)


        if stock <= stock_minimo:
            enviar_alerta_stock_email(nombre, stock)

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
        descripcion = request.form.get('descripcion')

        imagen_url = request.form.get('imagen_url')
        imagen_file = request.files.get('imagen_archivo')

        imagen_final = imagen_url if imagen_url else producto.get('imagen_url', '')

        if imagen_file and imagen_file.filename != '':
            os.makedirs('static/uploads', exist_ok=True)
            filename = secure_filename(imagen_file.filename)
            imagen_file.save(os.path.join('static/uploads', filename))
            imagen_final = f'/static/uploads/{filename}'

        actualizar_producto(id_producto, nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_final)


        if stock <= stock_minimo:
            enviar_alerta_stock_email(nombre, stock)

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        if stock == 0:
            mensaje_alerta = f'¡Alerta de Inventario! El producto "{nombre}" fue modificado y se ha quedado AGOTADO (0 unidades).'
        elif stock <= stock_minimo:
            mensaje_alerta = f'¡Atención! El producto "{nombre}" fue modificado y quedó por debajo del stock mínimo. Quedan {stock} unidades.'
        else:
            mensaje_alerta = f'¡Producto Actualizado! El administrador modificó los datos de "{nombre}".'

        cursor.execute("INSERT INTO notificaciones (mensaje, fecha_creacion) VALUES (%s, NOW())", (mensaje_alerta,))
        conexion.commit()
        cursor.close()
        conexion.close()

        flash('Producto actualizado con éxito.', 'success')
        return redirect(url_for('admin.panel_admin'))

    return render_template('admin/editar.html', producto=producto)




@admin_blueprint.route('/producto/eliminar/<int:id_producto>', methods=['POST'])
def eliminar_producto(id_producto):
    if not es_admin():
        return redirect(url_for('auth.login'))

    producto = obtener_producto_por_id(id_producto)
    nombre_producto = producto['nombre'] if producto else "Desconocido"

    eliminar_producto_db(id_producto)

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO notificaciones (mensaje, fecha_creacion) VALUES (%s, NOW())",
                   (f'¡Producto Eliminado! El administrador removió "{nombre_producto}" del sistema.',))
    conexion.commit()
    cursor.close()
    conexion.close()

    flash('Producto eliminado correctamente.', 'success')
    return redirect(url_for('admin.panel_admin'))




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


@admin_blueprint.route('/reportes')
def ver_reportes():
    if not es_admin():
        return redirect(url_for('auth.login'))
    
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    # 1. Total de productos activos
    cursor.execute("SELECT COUNT(*) as total FROM productos WHERE estado = 1")
    total_productos = cursor.fetchone()['total']
    
    # 2. Productos bajo stock
    cursor.execute("SELECT id, nombre, stock FROM productos WHERE stock < 5 AND estado = 1 ORDER BY stock ASC")
    stock_bajo = cursor.fetchall() or []
    
    # 3. 🛍️ TOP 10 Productos Más Vendidos (CORREGIDO: Apunta a pedidos aprobados)
    cursor.execute("""
        SELECT p.id, p.nombre, SUM(pd.cantidad) as cantidad_vendida, p.precio_venta
        FROM productos p
        INNER JOIN pedido_detalles pd ON p.id = pd.producto_id
        INNER JOIN pedidos pe ON pd.pedido_id = pe.id
        WHERE pe.estado != 'pendiente'
        GROUP BY p.id
        ORDER BY cantidad_vendida DESC
        LIMIT 10
    """)
    top_productos = cursor.fetchall() or []
    
    # 4. 💰 Ingresos Totales (CORREGIDO: Suma las ventas reales de pedidos pagados)
    cursor.execute("""
        SELECT SUM(p.precio_venta * pd.cantidad) as ingresos_totales
        FROM pedido_detalles pd
        INNER JOIN productos p ON pd.producto_id = p.id
        INNER JOIN pedidos pe ON pd.pedido_id = pe.id
        WHERE pe.estado != 'pendiente'
    """)
    result = cursor.fetchone()
    ingresos_totales = result['ingresos_totales'] if result['ingresos_totales'] else 0
    
    # 5. Soporte pendiente
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

@admin_blueprint.route('/pedidos')
def gestion_pedidos():
    if not es_admin():
        return redirect(url_for('auth.login'))

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    # Traemos los pedidos con la referencia y el nombre del cliente
    query = """
        SELECT p.id, p.referencia, p.total, p.estado, p.fecha_creacion, u.nombre as cliente 
        FROM pedidos p
        INNER JOIN usuarios u ON p.usuario_id = u.id
        ORDER BY p.fecha_creacion DESC
    """
    cursor.execute(query)
    lista_pedidos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return render_template('admin/pedidos.html', pedidos=lista_pedidos)


@admin_blueprint.route('/pedidos/actualizar/<int:id_pedido>', methods=['POST'])
def actualizar_estado_pedido(id_pedido):
    if not es_admin():
        return redirect(url_for('auth.login'))

    nuevo_estado = request.form.get('estado')

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True) # Usamos dictionary=True para facilitar las lecturas
    try:
        # 1. Primero obtenemos los datos del cliente y su pedido para el correo (Cambiado u.email por u.correo)
        query_cliente = """
            SELECT u.correo, u.nombre, p.referencia 
            FROM pedidos p
            INNER JOIN usuarios u ON p.usuario_id = u.id
            WHERE p.id = %s
        """
        cursor.execute(query_cliente, (id_pedido,))
        datos_pedido = cursor.fetchone()

        # 2. Actualizamos el estado del pedido en la base de datos
        cursor.execute("UPDATE pedidos SET estado = %s WHERE id = %s", (nuevo_estado, id_pedido))
        
        # 3. Insertamos la notificación interna del sistema
        mensaje_notificacion = f'El pedido #{id_pedido} ha sido actualizado a: "{nuevo_estado}".'
        cursor.execute("INSERT INTO notificaciones (mensaje, fecha_creacion) VALUES (%s, NOW())", (mensaje_notificacion,))
        
        conexion.commit()

        # 4. Enviamos el correo electrónico si encontramos los datos del cliente (Cambiado ['email'] por ['correo'])
        if datos_pedido and datos_pedido['correo']:
            ref = datos_pedido['referencia'] if datos_pedido['referencia'] else id_pedido
            enviar_correo_estado(
                email_destino=datos_pedido['correo'],
                nombre_cliente=datos_pedido['nombre'],
                referencia_pedido=ref,
                nuevo_estado=nuevo_estado
            )

        flash(f'Pedido actualizado a "{nuevo_estado}" y cliente notificado.', 'success')
    except Exception as e:
        flash(f'Error al actualizar el pedido o enviar el correo: {e}', 'danger')
    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for('admin.gestion_pedidos'))
def enviar_correo_estado(email_destino, nombre_cliente, referencia_pedido, nuevo_estado):
    remitente = os.getenv('MAIL_USERNAME', 'jholianmanuel10@gmail.com')
    password = os.getenv('MAIL_PASSWORD', 'tbffjihlqxwtgxkh')
    server_smtp = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    
    puerto_smtp = 465 

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = email_destino
    # Aseguramos que el asunto también soporte caracteres especiales en español
    msg['Subject'] = f"🛍️ Actualización de tu pedido en Dunaka - #{referencia_pedido}"

    cuerpo_html = f"""
    <html>
    <body style="font-family: 'Poppins', Arial, sans-serif; background-color: #f7fafc; padding: 20px; color: #2d3748;">
        <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 16px; padding: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;">
            <h2 style="color: #6f42c1; text-align: center; font-size: 24px; font-weight: 700; margin-bottom: 20px;">¡Hola, {nombre_cliente}! 👋</h2>
            <p style="font-size: 16px; line-height: 1.6; text-align: center;">
                Queremos informarte que el estado de tu pedido con referencia <strong style="color: #2b6cb0;">#{referencia_pedido}</strong> ha cambiado.
            </p>
            
            <div style="background: #edf2f7; border-radius: 12px; padding: 20px; text-align: center; margin: 25px 0;">
                <p style="margin: 0; font-size: 14px; text-uppercase; color: #718096; font-weight: 600; letter-spacing: 0.5px;">Nuevo Estado:</p>
                <p style="margin: 5px 0 0 0; font-size: 22px; color: #1a202c; font-weight: 700; text-transform: capitalize;">✨ {nuevo_estado} ✨</p>
            </div>

            <p style="font-size: 15px; line-height: 1.6; text-align: center; color: #4a5568;">
                Estamos trabajando para que disfrutes de tu producto lo antes posible. Si tienes dudas, puedes ingresar a tu panel de usuario o escribirnos a soporte.
            </p>
            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 30px 0;">
            <p style="font-size: 12px; text-align: center; color: #a0aec0; margin: 0;">
                Este es un correo automático de Dunaka. Por favor no respondas directamente a este mensaje.
            </p>
        </div>
    </body>
    </html>
    """
    
    # Forzamos a que el texto interno MIME use codificación utf-8 de forma estricta
    msg.attach(MIMEText(cuerpo_html, 'html', 'utf-8'))

    try:
        server = smtplib.SMTP_SSL(server_smtp, puerto_smtp)
        server.login(remitente, password)
        # SOLUCIÓN CRÍTICA: Usamos as_bytes() en lugar de as_string() para evitar fallos de codificación ASCII
        server.sendmail(remitente, email_destino, msg.as_bytes())
        server.quit()
        print(f"📩 Correo enviado con éxito a {email_destino}")
    except Exception as e:
        print(f"❌ Error crítico al enviar correo: {e}")
        raise e