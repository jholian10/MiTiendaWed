from database.db import obtener_conexion

def obtener_o_crear_carrito(usuario_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id FROM carritos WHERE usuario_id = %s", (usuario_id,))
    carrito = cursor.fetchone()
    
    if carrito:
        carrito_id = carrito['id']
    else:
        cursor.execute("INSERT INTO carritos (usuario_id) VALUES (%s)", (usuario_id,))
        conexion.commit()
        carrito_id = cursor.lastrowid
        
    cursor.close()
    conexion.close()
    return carrito_id

def agregar_producto_al_carrito(usuario_id, producto_id, cantidad=1):
    carrito_id = obtener_o_crear_carrito(usuario_id)
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    query_verificar = "SELECT id, cantidad FROM carrito_detalles WHERE carrito_id = %s AND producto_id = %s"
    cursor.execute(query_verificar, (carrito_id, producto_id))
    detalle = cursor.fetchone()
    
    if detalle:
        nueva_cantidad = detalle['cantidad'] + cantidad
        query_update = "UPDATE carrito_detalles SET cantidad = %s WHERE id = %s"
        cursor.execute(query_update, (nueva_cantidad, detalle['id']))
    else:
        query_insert = "INSERT INTO carrito_detalles (carrito_id, producto_id, cantidad) VALUES (%s, %s, %s)"
        cursor.execute(query_insert, (carrito_id, producto_id, cantidad))
        
    conexion.commit()
    cursor.close()
    conexion.close()
    return True

def obtener_detalles_carrito(usuario_id):
    carrito_id = obtener_o_crear_carrito(usuario_id)
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
        SELECT cd.id AS detalle_id, p.id AS producto_id, p.nombre, p.precio_venta, 
               p.imagen_url, cd.cantidad, (p.precio_venta * cd.cantidad) AS subtotal
        FROM carrito_detalles cd
        JOIN productos p ON cd.producto_id = p.id
        WHERE cd.carrito_id = %s
    """
    cursor.execute(query, (carrito_id,))
    items = cursor.fetchall()
    cursor.close()
    conexion.close()
    return items

def obtener_carrito_usuario(usuario_id):
    items = obtener_detalles_carrito(usuario_id)
    total = sum(float(item['subtotal']) for item in items)
    return {
        'items': items,
        'total': total
    }

def eliminar_del_carrito(detalle_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM carrito_detalles WHERE id = %s", (detalle_id,))
    conexion.commit()
    cursor.close()
    conexion.close()