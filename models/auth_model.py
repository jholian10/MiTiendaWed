# models/auth_model.py
from database.db import obtener_conexion
from werkzeug.security import generate_password_hash

def obtener_usuario_por_correo(correo):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s AND activo = 1", (correo,))
        usuario = cursor.fetchone()
        return usuario
    finally:
        cursor.close()
        conexion.close()

def registrar_usuario(nombre, correo, password_plana, rol='cliente'):
    pwd = generate_password_hash(password_plana, method='scrypt')
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo, password_hash, rol, activo) VALUES (%s, %s, %s, %s, 1)", 
            (nombre, correo, pwd, rol)
        )
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()

def registrar_usuario_oauth(nombre, correo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo, password_hash, rol, activo) VALUES (%s, %s, 'google_auth', 'cliente', 1)", 
            (nombre, correo)
        )
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al registrar oauth: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()

def guardar_codigo_recuperacion(correo, codigo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "UPDATE usuarios SET codigo_recuperacion = %s, codigo_expira = NOW() + INTERVAL 10 MINUTE WHERE correo = %s", 
            (codigo, correo)
        )
        conexion.commit()
    finally:
        cursor.close()
        conexion.close()

def verificar_codigo_y_correo(correo, codigo):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id FROM usuarios WHERE correo = %s AND codigo_recuperacion = %s AND codigo_expira > NOW()", 
            (correo, codigo)
        )
        usuario = cursor.fetchone()
        return usuario
    finally:
        cursor.close()
        conexion.close()

def actualizar_password(correo, nueva_pwd):
    pwd = generate_password_hash(nueva_pwd, method='scrypt')
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "UPDATE usuarios SET password_hash = %s, codigo_recuperacion = NULL, codigo_expira = NULL WHERE correo = %s", 
            (pwd, correo)
        )
        conexion.commit()
    finally:
        cursor.close()
        conexion.close()
        
def obtener_datos_envio_usuario(usuario_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT telefono, direccion, ciudad FROM usuarios WHERE id = %s", (usuario_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()
    return usuario