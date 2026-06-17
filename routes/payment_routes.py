import os
import hashlib
import time
from flask import Blueprint, session, redirect, url_for, flash, render_template_string, request
from database.db import obtener_conexion
from models.cart_model import obtener_detalles_carrito

payment_blueprint = Blueprint('payment', __name__, url_prefix='/pago')

WOMPI_PUBLIC_KEY = os.getenv('WOMPI_PUBLIC_KEY', 'pub_test_GHpuOWhHiYzNcAX5EZX9Fy4lTKxfBTWT').strip()
WOMPI_INTEGRITY_SECRET = os.getenv('WOMPI_INTEGRITY_SECRET', 'test_integrity_P0flJ5cCmnqd6LtVHARxwxVSFy6rI6Ft...').strip()

@payment_blueprint.route('/checkout', methods=['GET', 'POST'])
def procesar_pago():
    if 'usuario' not in session:
        flash('Debes iniciar sesión.', 'warning')
        return redirect(url_for('auth.login'))

    usuario_id = session['usuario']['id']
    items_carrito = obtener_detalles_carrito(usuario_id)
    
    if not items_carrito:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('cart.ver_carrito'))

    direccion = request.form.get('direccion', 'No especificada')
    ciudad = request.form.get('ciudad', 'No especificada')
    telefono = request.form.get('telefono', 'No especificado')

    total_cop = sum(float(item['precio_venta']) * int(item['cantidad']) for item in items_carrito)
    monto_en_centavos = int(round(total_cop * 100))
    referencia_pago = f"ORD_{usuario_id}_{int(time.time() * 1000)}"
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    sql = """INSERT INTO pedidos (usuario_id, referencia, total, estado, direccion_envio, ciudad_envio, telefono_contacto, fecha_creacion) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())"""
    cursor.execute(sql, (usuario_id, referencia_pago, total_cop, 'PENDIENTE', direccion, ciudad, telefono))
    
    conexion.commit()
    cursor.close()
    conexion.close()
    
    cadena_firma = f"{referencia_pago}{monto_en_centavos}COP{WOMPI_INTEGRITY_SECRET}"
    firma_checksum = hashlib.sha256(cadena_firma.encode('utf-8')).hexdigest()

    correo_usuario = session['usuario'].get('correo') or session['usuario'].get('email', '')

    html_form = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Procesando pago...</title>
    </head>
    <body onload="document.getElementById('wompi_form').submit()">
        <form id="wompi_form" action="https://checkout.wompi.co/p/" method="GET">
            <input type="hidden" name="public-key" value="{WOMPI_PUBLIC_KEY}" />
            <input type="hidden" name="currency" value="COP" />
            <input type="hidden" name="amount-in-cents" value="{monto_en_centavos}" />
            <input type="hidden" name="reference" value="{referencia_pago}" />
            <input type="hidden" name="signature:integrity" value="{firma_checksum}" />
            <input type="hidden" name="customer-data:email" value="{correo_usuario}" />
        </form>
    </body>
    </html>
    """
    return render_template_string(html_form)

@payment_blueprint.route('/webhooks/wompi', methods=['POST'])
def webhook_wompi():
    data = request.json
    if data and data.get('event') == 'transaction.updated':
        transaction = data['data']['transaction']
        referencia = transaction['reference']
        estado = transaction['status']

        if estado == 'APPROVED':
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)
            try:
                # 1. Actualizar estado
                cursor.execute("UPDATE pedidos SET estado = 'EMPACANDO' WHERE referencia = %s", (referencia,))
                
                # 2. Obtener usuario para limpiar carrito
                cursor.execute("SELECT usuario_id FROM pedidos WHERE referencia = %s", (referencia,))
                pedido = cursor.fetchone()
                
                if pedido:
                    u_id = pedido['usuario_id']
                    # Limpiar carrito
                    cursor.execute("DELETE FROM carrito_detalles WHERE carrito_id IN (SELECT id FROM carritos WHERE usuario_id = %s)", (u_id,))
                    cursor.execute("DELETE FROM carritos WHERE usuario_id = %s", (u_id,))
                
                conexion.commit()
            except Exception as e:
                print(f"Error en webhook: {e}")
                conexion.rollback()
            finally:
                cursor.close()
                conexion.close()
    
    return '', 200

@payment_blueprint.route('/test-borrar-carrito/<int:u_id>')
def test_borrado(u_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM carrito_detalles WHERE carrito_id IN (SELECT id FROM carritos WHERE usuario_id = %s)", (u_id,))
    cursor.execute("DELETE FROM carritos WHERE usuario_id = %s", (u_id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return "¡Carrito borrado con éxito!"