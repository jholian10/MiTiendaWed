import os
import hashlib
import time
import requests
from flask import Blueprint, session, redirect, url_for, flash, render_template_string, request
from models.cart_model import obtener_detalles_carrito

payment_blueprint = Blueprint('payment', __name__, url_prefix='/pago')

WOMPI_PUBLIC_KEY = os.getenv('WOMPI_PUBLIC_KEY', 'pub_test_GHpuOWhHiYzNcAX5EZX9Fy4lTKxfBTWT').strip()
WOMPI_INTEGRITY_SECRET = os.getenv('WOMPI_INTEGRITY_SECRET', 'test_integrity_P0flJ5cCmnqd6LtVHARxwxVSFy6rI6Ft').strip()

@payment_blueprint.route('/checkout', methods=['POST'])
def procesar_pago():
    if 'usuario' not in session:
        flash('Debes iniciar sesión para proceder al pago.', 'warning')
        return redirect(url_for('auth.login'))

    usuario_id = session['usuario']['id']
    items_carrito = obtener_detalles_carrito(usuario_id)
    
    if not items_carrito:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('cart.ver_carrito'))

    total_cop = 0
    for item in items_carrito:
        total_cop += float(item['precio_venta']) * int(item['cantidad'])
    
    monto_en_centavos = int(total_cop * 100)
    referencia_pago = f"MITIENDA_{usuario_id}_{int(time.time())}"
    moneda = "COP"
    cadena_firma = f"{referencia_pago}{monto_en_centavos}{moneda}{WOMPI_INTEGRITY_SECRET}"
    firma_checksum = hashlib.sha256(cadena_firma.encode('utf-8')).hexdigest()

    webhook_url = os.getenv('WOMPI_WEBHOOK_URL', '')
    if 'ngrok-free.app' in webhook_url:
        base_url = webhook_url.split('/api/')[0]
        redirect_url = f"{base_url}/pago/resultado"
    else:
        redirect_url = 'http://localhost:3000/pago/resultado'

    html_form = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Redireccionando a Pasarela de Pago</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 100px; background-color: #f4f6f9; }}
            .loader {{ border: 6px solid #f3f3f3; border-top: 6px solid #3498db; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 20px auto; }}
            @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
        </style>
    </head>
    <body onload="document.getElementById('wompi_form').submit()">
        <div class="loader"></div>
        <h2>Conectando de forma segura con Wompi...</h2>
        <p>Por favor, no cierres ni recargues esta ventana.</p>
        
        <form id="wompi_form" name="wompi_form" action="https://checkout.wompi.co/p/" method="GET">
            <input type="hidden" name="public-key" value="{WOMPI_PUBLIC_KEY}" />
            <input type="hidden" name="currency" value="{moneda}" />
            <input type="hidden" name="amount-in-cents" value="{monto_en_centavos}" />
            <input type="hidden" name="reference" value="{referencia_pago}" />
            <input type="hidden" name="signature:integrity" value="{firma_checksum}" />
            <input type="hidden" name="redirect-url" value="{redirect_url}" />
            <input type="hidden" name="customer-data:email" value="{session['usuario'].get('correo')}" />
        </form>
    </body>
    </html>
    """
    return render_template_string(html_form)

@payment_blueprint.route('/resultado', methods=['GET'])
def pago_resultado():
    transaccion_id = request.args.get('id')
    
    if not transaccion_id:
        flash('No se recibió un identificador válido de transacción.', 'warning')
        return redirect(url_for('cart.ver_carrito'))

    try:
        url_api = f"https://sandbox.wompi.co/v1/transactions/{transaccion_id}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "es-ES,es;q=0.9"
        }
        
        respuesta = requests.get(url_api, headers=headers).json()
        estado = respuesta['data']['status'] 

        if estado == "APPROVED":
            flash('¡Excelente! El pago simulado fue APROBADO con éxito.', 'success')
        elif estado == "DECLINED":
            flash('El pago simulado fue RECHAZADO por la pasarela.', 'danger')
        elif estado == "PENDING":
            flash('El pago se encuentra PENDIENTE.', 'info')
        else:
            flash(f'La transacción finalizó con el estado: {estado}', 'warning')

    except Exception:
        flash('El pago se procesó, pero ocurrió un problema al validar su estado.', 'info')

    return redirect(url_for('cart.ver_carrito'))