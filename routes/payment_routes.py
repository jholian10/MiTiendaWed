import os
import hashlib
import time
from flask import Blueprint, session, redirect, url_for, flash, request, render_template
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

    # Corrección matemática explícita: Convertimos el precio a float antes de operar
    total_cop = sum(float(item['precio_venta']) * int(item['cantidad']) for item in items_carrito)
    monto_en_centavos = int(round(total_cop * 100))
    referencia_pago = f"ORD_{usuario_id}_{int(time.time() * 1000)}"

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """INSERT INTO pedidos (usuario_id, referencia, total, estado, direccion_envio, ciudad_envio, telefono_contacto, fecha_creacion)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())"""

        cursor.execute(sql, (usuario_id, referencia_pago, total_cop, 'PENDIENTE', direccion, ciudad, telefono))
        conexion.commit()
        print(f"DEBUG: Pedido {referencia_pago} guardado correctamente.")

    except Exception as e:
        print(f"❌ ERROR CRÍTICO AL GUARDAR PEDIDO: {e}")
        flash('Hubo un error al procesar tu pedido.', 'danger')
        return redirect(url_for('cart.ver_carrito'))
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

    cadena_firma = f"{referencia_pago}{monto_en_centavos}COP{WOMPI_INTEGRITY_SECRET}"
    firma_checksum = hashlib.sha256(cadena_firma.encode('utf-8')).hexdigest()

    correo_usuario = session['usuario'].get('correo') or session['usuario'].get('email', '')
    url_retorno = "https://constrain-fading-overall.ngrok-free.dev/pago/resultado"

    # Redirección directa al Checkout de Wompi mediante URL limpia (Evita bloqueos 403 de CloudFront)
    url_wompi_directo = (
        f"https://checkout.wompi.co/p/?"
        f"public-key={WOMPI_PUBLIC_KEY}&"
        f"currency=COP&"
        f"amount-in-cents={monto_en_centavos}&"
        f"reference={referencia_pago}&"
        f"signature:integrity={firma_checksum}&"
        f"redirect-url={url_retorno}&"
        f"customer-data:email={correo_usuario}"
    )
    
    return redirect(url_wompi_directo)


@payment_blueprint.route('/webhooks/wompi', methods=['POST'])
def webhook_wompi():
    data = request.json
    print(f"DEBUG: Webhook recibido: {data}")

    if not data or data.get('event') != 'transaction.updated':
        return '', 200

    transaction = data['data']['transaction']
    referencia = transaction['reference']
    estado = transaction['status']

    print(f"DEBUG: Procesando transacción {referencia} con estado {estado}")

    if estado == 'APPROVED':
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute("UPDATE pedidos SET estado = 'EMPACANDO' WHERE referencia = %s", (referencia,))
            conexion.commit()

            if cursor.rowcount > 0:
                print(f"DEBUG: ÉXITO - Pedido {referencia} actualizado a EMPACANDO")

                cursor.execute("SELECT id, usuario_id FROM pedidos WHERE referencia = %s", (referencia,))
                pedido = cursor.fetchone()

                if pedido:
                    u_id = pedido['usuario_id']
                    pedido_id = pedido['id']

                    query_pasar_detalles = """
                        INSERT INTO pedido_detalles (pedido_id, producto_id, cantidad, precio_unitario)
                        SELECT %s, cd.producto_id, cd.cantidad, p.precio_venta
                        FROM carrito_detalles cd
                        INNER JOIN carritos c ON cd.carrito_id = c.id
                        INNER JOIN productos p ON cd.producto_id = p.id
                        WHERE c.usuario_id = %s
                    """
                    cursor.execute(query_pasar_detalles, (pedido_id, u_id))
                    print(f"DEBUG: Productos del carrito migrados a pedido_detalles para el pedido ID {pedido_id}")

                    cursor.execute("DELETE FROM carrito_detalles WHERE carrito_id IN (SELECT id FROM carritos WHERE usuario_id = %s)", (u_id,))
                    cursor.execute("DELETE FROM carritos WHERE usuario_id = %s", (u_id,))
                    
                    conexion.commit()
                    print(f"DEBUG: Carrito del usuario {u_id} vaciado correctamente")
            else:
                print(f"DEBUG: ¡ALERTA! No se encontró pedido con referencia '{referencia}'")

        except Exception as e:
            print(f"❌ ERROR CRÍTICO EN WEBHOOK: {e}")
            conexion.rollback()
        finally:
            cursor.close()
            conexion.close()

    return '', 200


@payment_blueprint.route('/resultado', methods=['GET'])
def resultado_pago():
    # Captura el ID de transacción enviado por Wompi por parámetro GET
    id_transaccion = request.args.get('id') or "En verificación"
    status_wompi = request.args.get('env') or "indefinido"
    
    print(f"DEBUG: Retorno de pasarela ejecutado. Transacción ID: {id_transaccion}, Estado: {status_wompi}")
    
    # Redirección directa a la vista física de pedidos de tu sistema para no romper el flujo
    flash(f"Pago procesado con éxito. ID de Operación: {id_transaccion}", "success")
    return redirect(url_for('orders.ver_pedidos'))