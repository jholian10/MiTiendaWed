from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from database.db import obtener_conexion
from models.order_model import obtener_pedidos_usuario

# Esta línea debe quedar así en routes/order_routes.py
order_custom_bp = Blueprint('orders', __name__, url_prefix='/pedidos')

# --------------------------------------------------------
# VISTA: HISTORIAL DE PEDIDOS
# --------------------------------------------------------
@order_custom_bp.route('/')
def ver_pedidos():
    usuario_sesion = session.get('usuario')
    if not usuario_sesion:
        flash('Por favor, inicia sesión para ver tus pedidos.', 'error')
        return redirect(url_for('auth.login'))
    
    # Llamamos a la función del modelo que nos devuelve la lista con diccionarios nativos
    mis_pedidos = obtener_pedidos_usuario(usuario_sesion['id'])
    
    # Tu archivo 'pedidos.html' funcionará idéntico porque Jinja lee igual pedido.estado que pedido['estado']
    return render_template('pedidos.html', pedidos=mis_pedidos, usuario_sesion=usuario_sesion)


# --------------------------------------------------------
# ACCIÓN: CREAR PEDIDO DESDE EL CARRITO
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
        conexion.autocommit = False # Iniciamos transacción segura
        
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

        # 2. Calcular el total acumulado
        total_pedido = sum(float(item['precio_venta']) * item['cantidad'] for item in carro_items)
        
        # 3. Insertar la cabecera del pedido
        sql_pedido = """
            INSERT INTO pedidos (usuario_id, total, estado, direccion_envio, ciudad_envio, telefono_contacto, fecha_creacion)
            VALUES (%s, %s, 'pendiente', %s, %s, %s, NOW())
        """
        cursor.execute(sql_pedido, (usuario_sesion['id'], total_pedido, direccion, ciudad, telefono))
        pedido_id = cursor.lastrowid # Capturamos el ID asignado al pedido
        
        # 4. Insertar cada producto del carrito al detalle del pedido
        sql_detalle = """
            INSERT INTO pedido_detalles (pedido_id, producto_id, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """
        for item in carro_items:
            cursor.execute(sql_detalle, (pedido_id, item['producto_id'], item['cantidad'], item['precio_venta']))
        
        # 5. Limpiar el carrito del usuario ya que la compra fue procesada
        cursor.execute("DELETE FROM carrito WHERE usuario_id = %s", (usuario_sesion['id'],))
        
        conexion.commit() # Guardamos todo de golpe en la base de datos
        flash('¡Tu pedido ha sido registrado con éxito!', 'success')
        return redirect(url_for('orders.ver_pedidos'))
        
    except Exception as e:
        conexion.rollback() # Si algo falla en el proceso, deshacemos los cambios para evitar datos basura
        print(f"Error al crear pedido: {e}")
        flash('No se pudo completar la compra. Inténtalo de nuevo.', 'error')
        return redirect(url_for('cart.ver_carrito'))
        
    finally:
        cursor.close()
        conexion.close()