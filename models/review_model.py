from database.db import obtener_conexion

def guardar_reseña(producto_id, usuario_id, calificacion, comentario):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        query = """
            INSERT INTO reseñas (producto_id, usuario_id, calificacion, comentario, fecha_creacion)
            VALUES (%s, %s, %s, %s, NOW())
        """
        cursor.execute(query, (producto_id, usuario_id, calificacion, comentario))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception:
        return False

def obtener_reseñas_por_producto(producto_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
        SELECT r.*, u.nombre AS usuario_nombre
        FROM reseñas r
        INNER JOIN usuarios u ON r.usuario_id = u.id
        WHERE r.producto_id = %s
        ORDER BY r.fecha_creacion DESC
    """
    cursor.execute(query, (producto_id,))
    reseñas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return reseñas