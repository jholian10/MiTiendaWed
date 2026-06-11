from database.db import obtener_conexion

def obtener_pedidos_usuario(usuario_id):
    """Trae todos los pedidos de un usuario con sus respectivos detalles estructurados como diccionarios"""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True) # Retorna los registros como diccionarios {'id': 1, 'total': ...}
    
    try:
        # 1. Traer los pedidos del usuario
        query_pedidos = """
            SELECT id, usuario_id, fecha_creacion, total, estado, direccion_envio, ciudad_envio, telefono_contacto 
            FROM pedidos 
            WHERE usuario_id = %s 
            ORDER BY fecha_creacion DESC
        """
        cursor.execute(query_pedidos, (usuario_id,))
        pedidos = cursor.fetchall() # Esto ya es una lista de diccionarios
        
        # 2. Por cada pedido, buscar sus productos asociados
        for pedido in pedidos:
            query_detalles = """
                SELECT pd.id, pd.pedido_id, pd.producto_id, pd.cantidad, pd.precio_unitario, 
                       p.nombre AS producto_nombre, p.imagen_url AS producto_imagen
                FROM pedido_detalles pd
                JOIN productos p ON pd.producto_id = p.id
                WHERE pd.pedido_id = %s
            """
            cursor.execute(query_detalles, (pedido['id'],))
            # Añadimos la lista de productos directamente dentro del diccionario del pedido
            pedido['detalles'] = cursor.fetchall()
            
        return pedidos
        
    except Exception as e:
        print(f"Error en obtener_pedidos_usuario: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()