from flask import Blueprint, session, redirect, url_for, flash
import stripe
from models.cart_model import obtener_detalles_carrito

# Definición del Blueprint exclusivo para pagos
payment_blueprint = Blueprint('payment', __name__, url_prefix='/pago')

# Tu clave secreta de desarrollo de Stripe (sk_test_...)
stripe.api_key = "sk_test_TU_CLAVE_SECRETA_AQUI"

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

    # Estructurar carrito al formato nativo de Stripe
    line_items = []
    for item in items_carrito:
        line_items.append({
            'price_data': {
                'currency': 'usd',  # Cambia a 'cop', 'mxn', etc. según tu moneda
                'product_data': {
                    'name': item['nombre'],
                },
                # Stripe procesa en centavos enteros (Ej: $10.50 -> 1050)
                'unit_amount': int(float(item['precio_venta']) * 100),
            },
            'quantity': int(item['cantidad']),
        })

    try:
        # Crear la pasarela de Checkout externa
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            customer_email=session['usuario'].get('correo'),
            success_url='http://127.0.0.1:5000/pago/exitoso',
            cancel_url='http://127.0.0.1:5000/pago/fallido',
        )
        # Redirección directa hacia la pasarela de Stripe
        return redirect(checkout_session.url, code=303)
        
    except Exception as e:
        flash(f'Error de comunicación con la pasarela: {str(e)}', 'danger')
        return redirect(url_for('cart.ver_carrito'))


@payment_blueprint.route('/exitoso')
def pago_exitoso():
    """Ruta de aterrizaje cuando el cobro en Sandbox fue aprobado."""
    # NOTA: Aquí puedes ejecutar lógica extra como vaciar el carrito en la BD
    flash('¡Pago de prueba recibido con éxito en Stripe!', 'success')
    return redirect(url_for('cart.ver_carrito'))


@payment_blueprint.route('/fallido')
def pago_fallido():
    """Ruta de aterrizaje si el usuario cancela o la tarjeta es rechazada."""
    flash('El proceso de pago simulado ha sido cancelado.', 'warning')
    return redirect(url_for('cart.ver_carrito'))