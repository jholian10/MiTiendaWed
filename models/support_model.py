# models/support_model.py
from database.db import obtener_conexion

def guardar_mensaje_soporte(id_usuario, mensaje):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = "INSERT INTO soporte (usuario_id, mensaje) VALUES (%s, %s)"
        cursor.execute(query, (id_usuario, mensaje))
        conexion.commit()
        return True
    except Exception as e:
        print(f"ERROR AL GUARDAR EN BD: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()
        
def obtener_todos_los_mensajes():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    # Seleccionamos el mensaje junto con el nombre del usuario
    query = """
        SELECT s.*, u.nombre 
        FROM soporte s 
        JOIN usuarios u ON s.usuario_id = u.id 
        WHERE s.estado = 'pendiente'
    """
    cursor.execute(query)
    mensajes = cursor.fetchall()
    cursor.close()
    conexion.close()
    return mensajes