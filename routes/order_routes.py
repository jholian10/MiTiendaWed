import os
import hashlib
import time
from flask import Blueprint, render_template, redirect, url_for, flash, session, request, render_template_string
from database.db import obtener_conexion
from models.order_model import obtener_pedidos_usuario

# Corregido: Importamos el servicio de correos real desde tu carpeta models
from models.notificaciones_service import enviar_alerta_stock_email

order_custom_bp = Blueprint('orders', __name__, url_prefix='/pedidos')

# Credenciales de Wompi
WOMPI_PUBLIC_KEY = os.getenv('WOMPI_PUBLIC_KEY', 'pub_test_GHpuOWhHiYzNcAX5EZX9Fy4lTKxfBTWT').strip()
WOMPI_INTEGRITY_SECRET = os.getenv('WOMPI_INTEGRITY_SECRET', 'test_integrity_P0flJ5cCmnqd6LtVHARxwxVSFy6rI6Ft').strip()

@order_custom_bp.route('/')
def ver_pedidos():
    usuario_sesion = session.get('usuario')
    if not usuario_sesion:
        flash('Por favor, inicia sesión para ver tus pedidos.', 'error')
        return redirect(url_for('auth.login'))
    
    mis_pedidos = obtener_pedidos_usuario(usuario_sesion['id'])
    
    mapeo_estados = {
        'PENDIENTE': {'texto': 'Pendiente de Pago', 'clase': 'badge-pendiente'},
        'PAGADO': {'texto': 'Pago Aprobado', 'clase': 'badge-pagado'},
        'EMPACANDO': {'texto': 'Empacando tu producto', 'clase': 'badge-empacando'},
        'EN_TRANSITO': {'texto': 'En camino / Tránsito', 'clase': 'badge-transito'},
        'ENTREGADO': {'texto': '¡Entregado con éxito!', 'clase': 'badge-entregado'}
    }
    
    return render_template('pedidos.html', pedidos=mis_pedidos, usuario_sesion=usuario_sesion, mapa_estados=mapeo_estados)

@order_custom_bp.route('/crear', methods=['POST'])
def crear_pedido():
    usuario_sesion = session.get('usuario')
    if not usuario_sesion:
        flash('Inicia sesión para finalizar tu compra.', 'error')
        return redirect(url_for('auth.login'))
        
    direccion = request.form.get('direccion')
    ciudad = request.form.get('ciudad')
    telefono = request.form.get('telefono')
    
    if not direccion or not ciudad or not telefono:
        flash('Todos los campos de envío son obligatorios.', 'error')
        return redirect(url_for('cart.ver_carrito'))

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    try:
        conexion.autocommit = False # Transacción manual para seguridad
        
        # 1. Obtener carrito
        query_carrito = """
            SELECT c.producto_id, c.cantidad, p.precio_venta 
            FROM carrito c
            JOIN productos p ON c.producto_id = p.id
            WHERE c.usuario_id = %s
        """
        cursor.execute(query_carrito, (usuario_sesion['id'],))
        carro_items = cursor.fetchall()
        
        if not carro_items:
            flash('Tu carrito está vacío.', 'error')
            return redirect(url_for('product.index'))

        total_pedido = sum(float(item['precio_venta']) * item['cantidad'] for item in carro_items)
        monto_en_centavos = int(round(total_pedido * 100))
        referencia_pago = f"ORD_{usuario_sesion['id']}_{int(time.time() * 1000)}"
        
        # 2. Insertar cabecera del pedido
        sql_pedido = """
            INSERT INTO pedidos (usuario_id, referencia, total, estado, direccion_envio, ciudad_envio, telefono_contacto, fecha_creacion)
            VALUES (%s, %s, %s, 'PENDIENTE', %s, %s, %s, NOW())
        """
        cursor.execute(sql_pedido, (usuario_sesion['id'], referencia_pago, total_pedido, direccion, ciudad, telefono))
        pedido_id = cursor.lastrowid 
        
        # 3. Procesar artículos: Restar stock, notificar si es necesario e insertar detalle
        sql_detalle = """
            INSERT INTO pedido_detalles (pedido_id, producto_id, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """
        for item in carro_items:
            # A) Descontar stock del producto
            cursor.execute("UPDATE productos SET stock = stock - %s WHERE id = %s", (item['cantidad'], item['producto_id']))
            
            # B) Obtener datos para verificar el stock actual reflejado
            cursor.execute("SELECT nombre, stock, stock_minimo FROM productos WHERE id = %s", (item['producto_id'],))
            prod_actual = cursor.fetchone()
            
            # C) Corregido: Disparar la alerta por correo electrónico si bajó del stock mínimo tras la compra
            if prod_actual and prod_actual['stock'] <= prod_actual['stock_minimo']:
                enviar_alerta_stock_email(prod_actual['nombre'], prod_actual['stock'])

            # D) Insertar detalle de venta
            cursor.execute(sql_detalle, (pedido_id, item['producto_id'], item['cantidad'], item['precio_venta']))
        
        conexion.commit() # Confirmar todos los cambios si todo salió bien
        
        # 4. Firma Wompi para pago
        cadena_firma = f"{referencia_pago}{monto_en_centavos}COP{WOMPI_INTEGRITY_SECRET}"
        firma_checksum = hashlib.sha256(cadena_firma.encode('utf-8')).hexdigest()

        # Formulario de redirección automática
        html_form = f"""
        <body onload="document.getElementById('wompi_form').submit()">
            <form id="wompi_form" action="https://checkout.wompi.co/p/" method="GET">
                <input type="hidden" name="public-key" value="{WOMPI_PUBLIC_KEY}" />
                <input type="hidden" name="currency" value="COP" />
                <input type="hidden" name="amount-in-cents" value="{monto_en_centavos}" />
                <input type="hidden" name="reference" value="{referencia_pago}" />
                <input type="hidden" name="signature:integrity" value="{firma_checksum}" />
                <input type="hidden" name="customer-data:email" value="{usuario_sesion.get('correo', '')}" />
            </form>
        </body>
        """
        return render_template_string(html_form)
        
    except Exception as e:
        conexion.rollback() # Revertir cambios en la BD si algo falla
        print(f"❌ Error crítico en orden: {e}")
        flash('No se pudo procesar la transacción.', 'error')
        return redirect(url_for('cart.ver_carrito'))
    finally:
        cursor.close()
        conexion.close()

@order_custom_bp.route('/webhooks/wompi', methods=['POST'])
def webhook_wompi():
    data = request.json
    if data and data.get('event') == 'transaction.updated':
        transaction = data['data']['transaction']
        referencia = transaction['reference']
        
        if transaction['status'] == 'APPROVED':
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)
            try:
                # 1. Actualizar estado del pedido
                cursor.execute("UPDATE pedidos SET estado = 'EMPACANDO' WHERE referencia = %s", (referencia,))
                
                # 2. Obtener el usuario
                cursor.execute("SELECT usuario_id FROM pedidos WHERE referencia = %s", (referencia,))
                pedido = cursor.fetchone()
                
                if pedido:
                    u_id = pedido['usuario_id']
                    # 3. Vaciar carrito tras pago exitoso
                    cursor.execute("DELETE FROM carrito_detalles WHERE carrito_id IN (SELECT id FROM carritos WHERE usuario_id = %s)", (u_id,))
                    cursor.execute("DELETE FROM carritos WHERE usuario_id = %s", (u_id,))
                
                conexion.commit()
            except Exception as e:
                print(f"Error al procesar webhook: {e}")
                conexion.rollback()
            finally:
                cursor.close()
                conexion.close()
    return '', 200