import os
import hashlib
import time
from flask import Blueprint, session, redirect, url_for, flash, render_template_string, request
from database.db import obtener_conexion
from models.cart_model import obtener_detalles_carrito

payment_blueprint = Blueprint('payment', __name__, url_prefix='/pago')

# Configuración de Wompi
WOMPI_PUBLIC_KEY = os.getenv('WOMPI_PUBLIC_KEY', 'pub_test_GHpuOWhHiYzNcAX5EZX9Fy4lTKxfBTWT').strip()
WOMPI_INTEGRITY_SECRET = os.getenv('WOMPI_INTEGRITY_SECRET', 'test_integrity_P0flJ5cCmnqd6LtVHARxwxVSFy6rI6Ft').strip()

@payment_blueprint.route('/checkout', methods=['POST'])
def procesar_pago():
    if 'usuario' not in session:
        flash('Debes iniciar sesión.', 'warning')
        return redirect(url_for('auth.login'))

    usuario_id = session['usuario']['id']
    items_carrito = obtener_detalles_carrito(usuario_id)
    
    if not items_carrito:
        flash('Carrito vacío.', 'warning')
        return redirect(url_for('cart.ver_carrito'))

    # 1. Calculamos el total flotante de la BD
    total_cop = sum(float(item['precio_venta']) * int(item['cantidad']) for item in items_carrito)
    
    # 2. ¡EL ARREGLO DE LA FIRMA!: Forzamos a un ENTERO puro eliminando cualquier punto decimal (.0)
    monto_en_centavos = int(round(total_cop * 100))
    
    # 3. Referencia única en milisegundos
    referencia_pago = f"ORD_{usuario_id}_{int(time.time() * 1000)}"
    
    # Guardamos el registro en la BD
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO ordenes (usuario_id, referencia, total, estado) VALUES (%s, %s, %s, 'PENDIENTE')", 
                   (usuario_id, referencia_pago, total_cop))
    conexion.commit()
    cursor.close()
    conexion.close()
    
    # 4. Generamos la firma con el orden estricto de Wompi usando el entero limpio
    cadena_firma = f"{referencia_pago}{monto_en_centavos}COP{WOMPI_INTEGRITY_SECRET}"
    firma_checksum = hashlib.sha256(cadena_firma.encode('utf-8')).hexdigest()

    correo_usuario = session['usuario'].get('correo') or session['usuario'].get('email', '')

    # 5. Renderizado del formulario con redirección automática usando el método GET
    html_form = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Conectando con la pasarela de pago...</title>
        <style>
            body {{ font-family: 'Poppins', sans-serif; background-color: #f6f5f2; text-align: center; padding-top: 100px; color: #2b3531; }}
            .loader-box {{ background: white; padding: 40px; border-radius: 24px; display: inline-block; box-shadow: 0 15px 35px rgba(0,0,0,0.02); }}
            h2 {{ color: #ff6f61; }}
        </style>
    </head>
    <body onload="document.getElementById('wompi_form').submit()">
        <div class="loader-box">
            <h2>Conectando de forma segura con Wompi...</h2>
            <p>Por favor, no cierres ni recargues esta ventana.</p>
        </div>
        
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