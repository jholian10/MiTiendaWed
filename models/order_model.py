from database.db import obtener_conexion

def obtener_pedidos_usuario(usuario_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    pedidos = []
    
    try:
        # Consulta para traer los pedidos del usuario
        query = """
            SELECT id, referencia, total, estado, fecha_creacion
            FROM pedidos
            WHERE usuario_id = %s
            ORDER BY fecha_creacion DESC
        """
        cursor.execute(query, (usuario_id,))
        pedidos = cursor.fetchall()
        
        # Por cada pedido, traemos los productos relacionados
        for pedido in pedidos:
            query_detalles = """
        SELECT pd.cantidad, pd.precio_unitario, p.nombre, p.imagen_url 
        FROM pedido_detalles pd
        JOIN productos p ON pd.producto_id = p.id
        WHERE pd.pedido_id = %s
        """
            cursor.execute(query_detalles, (pedido['id'],))
            pedido['detalles'] = cursor.fetchall()
            
    except Exception as e:
        print(f"Error al obtener pedidos: {e}")
    finally:
        cursor.close()
        conexion.close()
        
    return pedidos