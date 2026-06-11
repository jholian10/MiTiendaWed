from database.db import obtener_conexion
from werkzeug.security import generate_password_hash

def obtener_usuario_por_correo(correo):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE correo = %s AND activo = 1", (correo,))
    u = cursor.fetchone()
    cursor.close(); conexion.close()
    return u

def registrar_usuario(nombre, correo, password_plana, rol='cliente'):
    pwd = generate_password_hash(password_plana, method='scrypt')
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nombre, correo, password_hash, rol, activo) VALUES (%s, %s, %s, %s, 1)", 
                       (nombre, correo, pwd, rol))
        conexion.commit()
        return True
    except: return False
    finally: cursor.close(); conexion.close()

def registrar_usuario_oauth(nombre, correo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nombre, correo, password_hash, rol, activo) VALUES (%s, %s, 'google_auth', 'cliente', 1)", 
                       (nombre, correo))
        conexion.commit()
        return True
    except: return False
    finally: cursor.close(); conexion.close()

def guardar_codigo_recuperacion(correo, codigo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("UPDATE usuarios SET codigo_recuperacion = %s, codigo_expira = NOW() + INTERVAL 10 MINUTE WHERE correo = %s", 
                   (codigo, correo))
    conexion.commit()
    cursor.close(); conexion.close()

def verificar_codigo_y_correo(correo, codigo):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id FROM usuarios WHERE correo = %s AND codigo_recuperacion = %s AND codigo_expira > NOW()", 
                   (correo, codigo))
    u = cursor.fetchone()
    cursor.close(); conexion.close()
    return u

def actualizar_password(correo, nueva_pwd):
    pwd = generate_password_hash(nueva_pwd, method='scrypt')
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("UPDATE usuarios SET password_hash = %s, codigo_recuperacion = NULL WHERE correo = %s", 
                   (pwd, correo))
    conexion.commit()
    cursor.close(); conexion.close()
    
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