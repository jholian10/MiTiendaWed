from database.db import obtener_conexion

def listar_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_url, estado 
        FROM productos WHERE estado = 1
    """)
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return productos

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

def obtener_producto_por_id(id_producto):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id = %s", (id_producto,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()
    return producto

def actualizar_producto(id_producto, nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_url):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
        UPDATE productos 
        SET nombre=%s, descripcion=%s, precio_compra=%s, precio_venta=%s, stock=%s, stock_minimo=%s, imagen_url=%s 
        WHERE id=%s
    """
    cursor.execute(query, (nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_url, id_producto))
    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar_producto_por_id(id_producto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("UPDATE productos SET estado = 0 WHERE id = %s", (id_producto,))
    conexion.commit()
    cursor.close()
    conexion.close()

def buscar_productos_por_nombre(termino):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
        SELECT id, nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_url, estado 
        FROM productos 
        WHERE (nombre LIKE %s OR descripcion LIKE %s) AND estado = 1
    """
    comodin = f"%{termino}%"
    cursor.execute(query, (comodin, comodin))
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return productos

# ===================================================
# CONSULTAS NUEVAS: GESTIÓN DE RESEÑAS
# ===================================================
def guardar_reseña(producto_id, usuario_id, calificacion, comentario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = """
            INSERT INTO reseñas (producto_id, usuario_id, calificacion, comentario) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (producto_id, usuario_id, calificacion, comentario))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al guardar la reseña en DB: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()

def obtener_reseñas_por_producto(producto_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        query = """
            SELECT r.id, r.producto_id, r.usuario_id, r.calificacion, r.comentario, r.fecha_creacion,
                   u.nombre AS usuario_nombre 
            FROM reseñas r
            JOIN usuarios u ON r.usuario_id = u.id
            WHERE r.producto_id = %s
            ORDER BY r.fecha_creacion DESC
        """
        cursor.execute(query, (producto_id,))
        reseñas = cursor.fetchall()
        return reseñas
    except Exception as e:
        print(f"Error al extraer las reseñas: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()