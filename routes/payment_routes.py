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

    # Obtenemos datos del formulario
    direccion = request.form.get('direccion', 'No especificada')
    ciudad = request.form.get('ciudad', 'No especificada')
    telefono = request.form.get('telefono', 'No especificado')

    # Cálculos
    total_cop = sum(float(item['precio_venta']) * int(item['cantidad']) for item in items_carrito)
    monto_en_centavos = int(round(total_cop * 100))
    referencia_pago = f"ORD_{usuario_id}_{int(time.time() * 1000)}"
    
    # 1. Guardar en Base de Datos
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

    # 2. Preparar datos para Wompi
    cadena_firma = f"{referencia_pago}{monto_en_centavos}COP{WOMPI_INTEGRITY_SECRET}"
    firma_checksum = hashlib.sha256(cadena_firma.encode('utf-8')).hexdigest()

    # IMPORTANTE: Aquí está la variable que usa el formulario
    correo_usuario = session['usuario'].get('correo') or session['usuario'].get('email', '')

    # --- SI TIENES UNA FUNCIÓN DE EMAIL, LLÁMALA AQUÍ ---
    # Ejemplo: enviar_email(correo_usuario, "Confirmación de Orden", "...")
    # Asegúrate de usar 'correo_usuario' y no 'correo'
    
    html_form = f"""
    <!DOCTYPE html>
    <html lang="es">
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
            # 1. Intentar actualizar
            cursor.execute("UPDATE pedidos SET estado = 'EMPACANDO' WHERE referencia = %s", (referencia,))
            conexion.commit() # Guardamos el cambio
            
            # Verificamos si realmente se actualizó alguna fila
            if cursor.rowcount > 0:
                print(f"DEBUG: ÉXITO - Pedido {referencia} actualizado a EMPACANDO")
                
                # 2. Obtener usuario para limpiar carrito
                cursor.execute("SELECT usuario_id FROM pedidos WHERE referencia = %s", (referencia,))
                pedido = cursor.fetchone()
                
                if pedido:
                    u_id = pedido['usuario_id']
                    # Borrar carrito
                    cursor.execute("DELETE FROM carrito_detalles WHERE carrito_id IN (SELECT id FROM carritos WHERE usuario_id = %s)", (u_id,))
                    cursor.execute("DELETE FROM carritos WHERE usuario_id = %s", (u_id,))
                    conexion.commit()
                    print(f"DEBUG: Carrito del usuario {u_id} vaciado correctamente")
            else:
                # DIAGNÓSTICO: Si llega aquí, es porque la referencia no existe
                print(f"DEBUG: ¡ALERTA! No se encontró pedido con referencia '{referencia}'")
                
                # DEBUG EXTRA: Imprimimos qué hay en la base de datos para comparar
                cursor.execute("SELECT referencia FROM pedidos ORDER BY fecha_creacion DESC LIMIT 5")
                ultimos_pedidos = cursor.fetchall()
                print(f"DEBUG: Las últimas 5 referencias en la BD son: {ultimos_pedidos}")
                print(f"DEBUG: ¿Quizás la referencia tiene espacios o es distinta? Verifica el log de arriba.")
                
        except Exception as e:
            print(f"❌ ERROR CRÍTICO EN WEBHOOK: {e}")
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

@payment_blueprint.route('/test-db-connection')
def test_db():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        # Intentamos insertar un dato falso
        cursor.execute("INSERT INTO pedidos (usuario_id, referencia, total, estado) VALUES (%s, %s, %s, %s)", 
                       (1, 'PRUEBA_123', 0, 'PENDIENTE'))
        conexion.commit()
        cursor.close()
        conexion.close()
        return "¡Conexión y escritura exitosa! Revisa tu tabla pedidos."
    except Exception as e:
        return f"Error crítico de conexión: {str(e)}"