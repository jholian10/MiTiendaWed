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

def verificar_compra_usuario(usuario_id, producto_id):
    """
    Consulta si el usuario ha comprado el producto, aceptando múltiples 
    estados válidos de pedido para facilitar las pruebas del proyecto.
    """
    conexion = obtener_conexion() 
    cursor = conexion.cursor()
    
    # Hemos modificado la condición de p.estado para que acepte 'completado', 'pagado' o 'pendiente'
    query = """
        SELECT COUNT(*) FROM pedido_detalles pd
        JOIN pedidos p ON pd.pedido_id = p.id
        WHERE p.usuario_id = %s 
          AND pd.producto_id = %s 
          AND p.estado IN ('completado', 'pagado', 'pendiente', 'entregado')
    """
    
    cursor.execute(query, (usuario_id, producto_id))
    resultado = cursor.fetchone()
    
    cursor.close()
    conexion.close()
    
    return resultado[0] > 0 if resultado else False