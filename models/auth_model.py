from database.db import obtener_conexion
from werkzeug.security import generate_password_hash

def obtener_usuario_por_correo(correo):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    query = """
        SELECT id, nombre, correo, password_hash, rol, activo, telefono, direccion, ciudad, foto_perfil_url 
        FROM usuarios 
        WHERE correo = %s AND activo = 1
    """
    cursor.execute(query, (correo,))
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()
    return usuario

def registrar_usuario(nombre, correo, password_plana, rol='cliente'):
    password_encriptada = generate_password_hash(password_plana, method='scrypt')
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = "INSERT INTO usuarios (nombre, correo, password_hash, rol, activo) VALUES (%s, %s, %s, %s, 1)"
    try:
        cursor.execute(query, (nombre, correo, password_encriptada, rol))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al registrar: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()

def registrar_usuario_oauth(nombre, correo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = "INSERT INTO usuarios (nombre, correo, password_hash, rol, activo) VALUES (%s, %s, 'google_auth', 'cliente', 1)"
    try:
        cursor.execute(query, (nombre, correo))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al registrar OAuth: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()

def actualizar_perfil_usuario(id_usuario, nombre, correo, telefono, direccion, ciudad, foto_perfil_url=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    if foto_perfil_url:
        query = """
            UPDATE usuarios 
            SET nombre = %s, correo = %s, telefono = %s, direccion = %s, ciudad = %s, foto_perfil_url = %s 
            WHERE id = %s
        """
        params = (nombre, correo, telefono, direccion, ciudad, foto_perfil_url, id_usuario)
    else:
        query = """
            UPDATE usuarios 
            SET nombre = %s, correo = %s, telefono = %s, direccion = %s, ciudad = %s 
            WHERE id = %s
        """
        params = (nombre, correo, telefono, direccion, ciudad, id_usuario)
        
    cursor.execute(query, params)
    conexion.commit()
    
    # Obtener el usuario actualizado
    cursor.execute("SELECT id, nombre, correo, rol, telefono, direccion, ciudad, foto_perfil_url FROM usuarios WHERE id = %s", (id_usuario,))
    usuario_actualizado = cursor.fetchone()
    
    cursor.close()
    conexion.close()
    return usuario_actualizado