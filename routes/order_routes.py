import os
import hashlib
import time
from flask import Blueprint, render_template, redirect, url_for, flash, session, request, render_template_string
from database.db import obtener_conexion
from models.order_model import obtener_pedidos_usuario
from models.notificaciones_service import enviar_alerta_stock_email

order_custom_bp = Blueprint('orders', __name__, url_prefix='/pedidos')

WOMPI_PUBLIC_KEY = os.getenv('WOMPI_PUBLIC_KEY', 'pub_test_GHpuOWhHiYzNcAX5EZX9Fy4lTKxfBTWT').strip()
WOMPI_INTEGRITY_SECRET = os.getenv('WOMPI_INTEGRITY_SECRET', 'test_integrity_P0flJ5cCmnqd6LtVHARxwxVSFy6rI6Ft').strip()

@order_custom_bp.route('/')
def ver_pedidos():
    usuario_sesion = session.get('usuario')
    if not usuario_sesion:
        flash('Por favor, inicia sesión para ver tus pedidos.', 'error')
        return redirect(url_for('auth.login'))

    mis_pedidos = obtener_pedidos_usuario(usuario_sesion['id'])

    # Corregimos las llaves para que coincidan exactamente con la base de datos y el admin
    mapeo_estados = {
        'pendiente': {'texto': 'Pendiente de Pago', 'clase': 'badge-pendiente'},
        'pagado': {'texto': 'Pago Aprobado', 'clase': 'badge-pagado'},
        'empacando': {'texto': 'Empacando tu bolso artesanal 🎒', 'clase': 'badge-empacando'},
        'en transito': {'texto': 'En camino / Tránsito 🚚', 'clase': 'badge-transito'},
        'entregado': {'texto': '¡Entregado con éxito! 🎉', 'clase': 'badge-entregado'},
        'cancelado': {'texto': 'Pedido Cancelado ❌', 'clase': 'badge-cancelado'}
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
        conexion.autocommit = False

        # 1. Extraer los productos usando las tablas correctas del carrito
        query_carrito = """
            SELECT cd.producto_id, cd.cantidad, p.precio_venta, p.nombre, p.stock, p.stock_minimo
            FROM carrito_detalles cd
            INNER JOIN carritos c ON cd.carrito_id = c.id
            INNER JOIN productos p ON cd.producto_id = p.id
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

        # 2. Crear el encabezado del pedido
        sql_pedido = """
            INSERT INTO pedidos (usuario_id, referencia, total, estado, direccion_envio, ciudad_envio, telefono_contacto, fecha_creacion)
            VALUES (%s, %s, %s, 'PENDIENTE', %s, %s, %s, NOW())
        """
        cursor.execute(sql_pedido, (usuario_sesion['id'], referencia_pago, total_pedido, direccion, ciudad, telefono))
        pedido_id = cursor.lastrowid

        # 3. Insertar detalles y gestionar inventario
        sql_detalle = """
            INSERT INTO pedido_detalles (pedido_id, producto_id, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """
        
        for item in carro_items:
            # Descontar stock del catálogo
            cursor.execute("UPDATE productos SET stock = stock - %s WHERE id = %s", (item['cantidad'], item['producto_id']))
            
            # Verificar si se necesita enviar alerta por inventario bajo
            nuevo_stock = item['stock'] - item['cantidad']
            if nuevo_stock <= item['stock_minimo']:
                enviar_alerta_stock_email(item['nombre'], nuevo_stock)

            # Insertar el producto en los detalles del pedido
            cursor.execute(sql_detalle, (pedido_id, item['producto_id'], item['cantidad'], item['precio_venta']))

        # Confirmar todos los cambios en la base de datos
        conexion.commit()

        # 4. Construir la firma de integridad y la vista de redirección para Wompi
        cadena_firma = f"{referencia_pago}{monto_en_centavos}COP{WOMPI_INTEGRITY_SECRET}"
        firma_checksum = hashlib.sha256(cadena_firma.encode('utf-8')).hexdigest()

        html_form = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Redirigiendo a pasarela segura...</title>
        </head>
        <body onload="document.getElementById('wompi_form').submit()" style="background-color: #f8f9fa; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
            <div style="text-align: center; font-family: sans-serif; color: #333;">
                <h2>Procesando tu orden...</h2>
                <p>Serás redirigido a Wompi en un instante.</p>
            </div>
            <form id="wompi_form" action="https://checkout.wompi.co/p/" method="GET" style="display: none;">
                <input type="hidden" name="public-key" value="{WOMPI_PUBLIC_KEY}" />
                <input type="hidden" name="currency" value="COP" />
                <input type="hidden" name="amount-in-cents" value="{monto_en_centavos}" />
                <input type="hidden" name="reference" value="{referencia_pago}" />
                <input type="hidden" name="signature:integrity" value="{firma_checksum}" />
                <input type="hidden" name="customer-data:email" value="{usuario_sesion.get('correo', '')}" />
            </form>
        </body>
        </html>
        """
        return render_template_string(html_form)

    except Exception as e:
        conexion.rollback()
        print(f"❌ Error crítico en orden: {e}")
        flash('No se pudo procesar la transacción de tu compra.', 'error')
        return redirect(url_for('cart.ver_carrito'))
    finally:
        cursor.close()
        conexion.close()