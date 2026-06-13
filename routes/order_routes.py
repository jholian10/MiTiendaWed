import os
import hashlib
import time
from flask import Blueprint, render_template, redirect, url_for, flash, session, request, render_template_string
from database.db import obtener_conexion
from models.order_model import obtener_pedidos_usuario

# Mantener el nombre del blueprint tal como lo requieres
order_custom_bp = Blueprint('orders', __name__, url_prefix='/pedidos')

# =========================================================================
# ⚙️ CREDENCIALES DE WOMPI (Cargadas desde tu .env corregido)
# =========================================================================
WOMPI_PUBLIC_KEY = os.getenv('WOMPI_PUBLIC_KEY', 'pub_test_GHpuOWhHiYzNcAX5EZX9Fy4lTKxfBTWT').strip()
WOMPI_INTEGRITY_SECRET = os.getenv('WOMPI_INTEGRITY_SECRET', 'test_integrity_P0flJ5cCmnqd6LtVHARxwxVSFy6rI6Ft').strip()


# --------------------------------------------------------
# VISTA: HISTORIAL DE PEDIDOS CON MAPEO DE ESTADOS BONITOS
# --------------------------------------------------------
@order_custom_bp.route('/')
def ver_pedidos():
    usuario_sesion = session.get('usuario')
    if not usuario_sesion:
        flash('Por favor, inicia sesión para ver tus pedidos.', 'error')
        return redirect(url_for('auth.login'))
    
    # Obtenemos la lista de pedidos desde tu modelo base
    mis_pedidos = obtener_pedidos_usuario(usuario_sesion['id'])
    
    # Diccionario de mapeo para que Jinja renderice textos amigables y clases CSS dinámicas
    mapeo_estados = {
        'PENDIENTE': {'texto': 'Pendiente de Pago', 'clase': 'badge-pendiente'},
        'PAGADO': {'texto': 'Pago Aprobado', 'clase': 'badge-pagado'},
        'EMPACANDO': {'texto': 'Empacando tu producto', 'clase': 'badge-empacando'},
        'EN_TRANSITO': {'texto': 'En camino / Tránsito', 'clase': 'badge-transito'},
        'ENTREGADO': {'texto': '¡Entregado con éxito!', 'clase': 'badge-entregado'}
    }
    
    return render_template('pedidos.html', pedidos=mis_pedidos, usuario_sesion=usuario_sesion, mapa_estados=mapeo_estados)


# --------------------------------------------------------
# ACCIÓN: CREAR PEDIDO E INICIAR PASARELA WOMPI
# --------------------------------------------------------
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
        conexion.autocommit = False # Iniciamos transacción segura para integridad SQL
        
        # 1. Obtener los productos que están actualmente en el carrito
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

        # 2. Calcular el total acumulado de la compra
        total_pedido = sum(float(item['precio_venta']) * item['cantidad'] for item in carro_items)
        
        # 3. Forzar el monto a centavos como entero absoluto para Wompi (Ej: 115000 -> 11500000)
        monto_en_centavos = int(round(total_pedido * 100))
        
        # 4. Crear una referencia única e irrepetible para Wompi usando marcas de tiempo en ms
        referencia_pago = f"ORD_{usuario_sesion['id']}_{int(time.time() * 1000)}"
        
        # 5. Insertar la cabecera en tu tabla de pedidos (Estado inicial: 'PENDIENTE')
        # NOTA: Agregamos la columna 'referencia' para poder enlazarlo con Wompi al recibir el Webhook
        sql_pedido = """
            INSERT INTO pedidos (usuario_id, referencia, total, estado, direccion_envio, ciudad_envio, telefono_contacto, fecha_creacion)
            VALUES (%s, %s, %s, 'PENDIENTE', %s, %s, %s, NOW())
        """
        cursor.execute(sql_pedido, (usuario_sesion['id'], referencia_pago, total_pedido, direccion, ciudad, telefono))
        pedido_id = cursor.lastrowid 
        
        # 6. Insertar cada producto del carrito al detalle del pedido
        sql_detalle = """
            INSERT INTO pedido_detalles (pedido_id, producto_id, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """
        for item in carro_items:
            cursor.execute(sql_detalle, (pedido_id, item['producto_id'], item['cantidad'], item['precio_venta']))
        
        # ⚠️ ACLARACIÓN: NO eliminamos el carrito aquí. El carrito se limpia únicamente 
        # en tu ruta de Webhook o página de retorno una vez Wompi confirme que la plata entró.
        
        conexion.commit() # Confirmamos la inserción en la BD local
        
        # 7. GENERACIÓN DEL CHECKSUM DE INTEGRIDAD EXIGIDO POR WOMPI
        # Cadena requerida: referencia + centavos + moneda + secreto_integridad
        cadena_firma = f"{referencia_pago}{monto_en_centavos}COP{WOMPI_INTEGRITY_SECRET}"
        firma_checksum = hashlib.sha256(cadena_firma.encode('utf-8')).hexdigest()

        # 📌 LOG DE VERIFICACIÓN EN CONSOLA (Para debugear en tu terminal ADSO)
        print("\n" + "="*60)
        print("🚀 [NEXUS GESTOR] PEDIDO ENLAZADO A PASARELA")
        print(f"• Pedido ID Local: {pedido_id}")
        print(f"• Referencia Generada: {referencia_pago}")
        print(f"• Total COP: ${total_pedido}")
        print(f"• Firma SHA256: {firma_checksum}")
        print("="*60 + "\n")

        correo_usuario = usuario_sesion.get('correo') or usuario_sesion.get('email', '')

        # 8. Retornar formulario dinámico que redirige al usuario directo a Wompi
        html_form = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Conectando con la pasarela de pago...</title>
            <style>
                body {{ font-family: 'Segoe UI', sans-serif; background-color: #f8f9fa; text-align: center; padding-top: 120px; color: #2c3e50; }}
                .loader-box {{ background: white; padding: 40px; border-radius: 16px; display: inline-block; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }}
                .spinner {{ border: 4px solid #f3f3f3; border-top: 4px solid #ff6f61; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 20px auto; }}
                @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
                h2 {{ color: #2c3e50; font-weight: 600; }}
            </style>
        </head>
        <body onload="document.getElementById('wompi_form').submit()">
            <div class="loader-box">
                <h2>Conectando de forma segura con Wompi...</h2>
                <div class="spinner"></div>
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
        
    except Exception as e:
        conexion.rollback() # Ante cualquier error cancelamos la transacción y evitamos inconsistencias
        print(f"❌ Error crítico en pasarela/pedido: {e}")
        flash('No se pudo procesar la transacción en este momento.', 'error')
        return redirect(url_for('cart.ver_carrito'))
        
    finally:
        cursor.close()
        conexion.close()