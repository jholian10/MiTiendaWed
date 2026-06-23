from database.db import obtener_conexion


def listar_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id, p.nombre, p.descripcion, p.precio_compra, p.precio_venta, p.stock, p.stock_minimo, p.imagen_url, p.estado,
               COALESCE(AVG(r.calificacion), 0) AS promedio_estrellas,
               COUNT(r.id) AS total_resenas
        FROM productos p
        LEFT JOIN reseñas r ON p.id = r.producto_id
        WHERE p.estado = 1
        GROUP BY p.id
    """)
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return productos

def obtener_producto_por_id(id_producto):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*,
               COALESCE(AVG(r.calificacion), 0) AS promedio_estrellas,
               COUNT(r.id) AS total_resenas
        FROM productos p
        LEFT JOIN reseñas r ON p.id = r.producto_id
        WHERE p.id = %s
        GROUP BY p.id
    """, (id_producto,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()
    return producto

def buscar_productos_por_nombre(termino):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*,
               COALESCE(AVG(r.calificacion), 0) AS promedio_estrellas,
               COUNT(r.id) AS total_resenas
        FROM productos p
        LEFT JOIN reseñas r ON p.id = r.producto_id
        WHERE p.nombre LIKE %s AND p.estado = 1
        GROUP BY p.id
    """, (f"%{termino}%",))
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return productos