from database.db import obtener_conexion

def guardar_direccion(usuario_id, departamento, ciudad, barrio, direccion_detallada, telefono_contacto="N/A"):
    """
    Guarda o actualiza la dirección del usuario en la base de datos.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        query = """
            INSERT INTO direcciones_usuario
            (usuario_id, departamento, ciudad, barrio, direccion_detallada, telefono_contacto)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        datos = (usuario_id, departamento, ciudad, barrio, direccion_detallada, telefono_contacto)

        cursor.execute(query, datos)
        conexion.commit()
        return True

    except Exception as e:
        print(f"Error al insertar en base de datos: {e}")
        conexion.rollback()
        return False

    finally:
        cursor.close()
        conexion.close()


def obtener_direccion_usuario(usuario_id):
    """
    Obtiene la dirección guardada del usuario desde la tabla direcciones_usuario.
    """
    conexion = obtener_conexion()
    
    try:
        # Intentamos usar diccionario si tu conector lo soporta por defecto
        cursor = conexion.cursor(dictionary=True)
    except TypeError:
        cursor = conexion.cursor()

    try:
        query = """
            SELECT departamento, ciudad, barrio, direccion_detallada, telefono_contacto 
            FROM direcciones_usuario 
            WHERE usuario_id = %s 
            ORDER BY id DESC LIMIT 1
        """
        cursor.execute(query, (usuario_id,))
        resultado = cursor.fetchone()
        
        # Si el resultado es una tupla (en vez de diccionario), la mapeamos manualmente
        if resultado and not isinstance(resultado, dict):
            columnas = [col[0] for col in cursor.description]
            return dict(zip(columnas, resultado))
            
        return resultado 
    except Exception as e:
        print(f"Error al obtener la dirección: {e}")
        return None
    finally:
        cursor.close()
        conexion.close()