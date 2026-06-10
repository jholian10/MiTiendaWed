from database.db import obtener_conexion

def conmutar_favorito(usuario_id, producto_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Comprobar si el producto ya es favorito de este usuario
    query_check = "SELECT 1 FROM favoritos WHERE usuario_id = %s AND producto_id = %s"
    cursor.execute(query_check, (usuario_id, producto_id))
    existe = cursor.fetchone()
    
    if existe:
        query_delete = "DELETE FROM favoritos WHERE usuario_id = %s AND producto_id = %s"
        cursor.execute(query_delete, (usuario_id, producto_id))
        agregado = False
    else:
        query_insert = "INSERT INTO favoritos (usuario_id, producto_id) VALUES (%s, %s)"
        cursor.execute(query_insert, (usuario_id, producto_id))
        agregado = True
        
    conexion.commit()
    cursor.close()
    conexion.close()
    return agregado

def obtener_ids_favoritos(usuario_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    query = "SELECT producto_id FROM favoritos WHERE usuario_id = %s"
    cursor.execute(query, (usuario_id,))
    resultados = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    return [r[0] for r in resultados]

def obtener_productos_favoritos(usuario_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    query = """
        SELECT p.* FROM productos p
        INNER JOIN favoritos f ON p.id = f.producto_id
        WHERE f.usuario_id = %s
    """
    cursor.execute(query, (usuario_id,))
    productos = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    return productos