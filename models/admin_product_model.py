from database.db import obtener_conexion

def insertar_producto(nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_url):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
        INSERT INTO productos (nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_url) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_url))
    conexion.commit()
    cursor.close()
    conexion.close()
    return True

def actualizar_producto(id_producto, nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_url):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
        UPDATE productos 
        SET nombre = %s, descripcion = %s, precio_compra = %s, precio_venta = %s, 
            stock = %s, stock_minimo = %s, imagen_url = %s
        WHERE id = %s
    """
    cursor.execute(query, (nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_url, id_producto))
    conexion.commit()
    cursor.close()
    conexion.close()
    return True

def eliminar_producto(id_producto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("UPDATE productos SET estado = 0 WHERE id = %s", (id_producto,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return True