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