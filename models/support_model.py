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

def obtener_clientes_soporte():
    """Obtiene lista de clientes que tienen mensajes de soporte pendientes"""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
        SELECT DISTINCT u.id, u.nombre, 
               (SELECT mensaje FROM soporte WHERE usuario_id = u.id ORDER BY id DESC LIMIT 1) as ultimo_mensaje
        FROM soporte s
        JOIN usuarios u ON s.usuario_id = u.id
        ORDER BY u.nombre
    """
    try:
        cursor.execute(query)
        clientes = cursor.fetchall()
        return clientes or []
    except Exception as e:
        print(f"Error obtener_clientes_soporte: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()

def obtener_historial_chat(usuario_id):
    """Obtiene todos los mensajes entre un cliente y el admin"""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
        SELECT id, usuario_id, mensaje, remitente, fecha as hora
        FROM soporte 
        WHERE usuario_id = %s
        ORDER BY fecha ASC
    """
    try:
        cursor.execute(query, (usuario_id,))
        mensajes = cursor.fetchall()
        return mensajes or []
    except Exception as e:
        print(f"Error obtener_historial_chat: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()

def guardar_respuesta_admin(usuario_id, mensaje):
    """Guarda un mensaje del admin en respuesta a un cliente"""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = """
            INSERT INTO soporte (usuario_id, mensaje, remitente) 
            VALUES (%s, %s, 'admin')
        """
        cursor.execute(query, (usuario_id, mensaje))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error guardar_respuesta_admin: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()