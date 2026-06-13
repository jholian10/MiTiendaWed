# models/perfil_modelo.py
from database.db import obtener_conexion

def actualizar_perfil_usuario(id_usuario, nombre, correo, telefono, direccion, ciudad, foto_perfil_url=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    try:
        if foto_perfil_url:
            query = """UPDATE usuarios SET nombre = %s, correo = %s, telefono = %s, 
                    direccion = %s, ciudad = %s, foto_perfil_url = %s WHERE id = %s"""
            params = (nombre, correo, telefono, direccion, ciudad, foto_perfil_url, id_usuario)
        else:
            query = """UPDATE usuarios SET nombre = %s, correo = %s, telefono = %s, 
                    direccion = %s, ciudad = %s WHERE id = %s"""
            params = (nombre, correo, telefono, direccion, ciudad, id_usuario)
        
        cursor.execute(query, params)
        conexion.commit()
        
        # Consultar los datos actualizados para devolverlos
        cursor.execute("SELECT id, nombre, correo, rol, telefono, direccion, ciudad, foto_perfil_url FROM usuarios WHERE id = %s", (id_usuario,))
        usuario = cursor.fetchone()
        return usuario
        
    except Exception as e:
        print(f"Error al actualizar perfil: {e}")
        return None
    finally:
        cursor.close()
        conexion.close()