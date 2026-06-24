
from database.db import obtener_conexion

def guardar_mensaje_soporte(id_usuario, nombre, correo, mensaje):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:

        query = "INSERT INTO soporte (usuario_id, nombre, correo, mensaje, remitente) VALUES (%s, %s, %s, %s, 'cliente')"
        cursor.execute(query, (id_usuario, nombre, correo, mensaje))
        conexion.commit()
        return True

    except Exception as e:
        print(f"Error guardar_mensaje_soporte: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()

def obtener_todos_los_mensajes():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

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
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    query = """
        SELECT id, usuario_id, mensaje, remitente, fecha_creacion as hora
        FROM soporte
        WHERE usuario_id = %s
        ORDER BY fecha_creacion ASC
    """
    try:
        cursor.execute(query, (usuario_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error en obtener_historial_chat: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()

def obtener_todos_los_mensajes():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    query = """
        SELECT s.*, u.nombre
        FROM soporte s
        JOIN usuarios u ON s.usuario_id = u.Id
        WHERE s.estado = 'pendiente'
    """
    cursor.execute(query)
    mensajes = cursor.fetchall()
    cursor.close()
    conexion.close()
    return mensajes

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