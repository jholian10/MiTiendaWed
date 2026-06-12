from werkzeug.security import generate_password_hash
from database.db import obtener_conexion

def crear_admin(nombre, correo, password):
    pwd_hash = generate_password_hash(password, method='pbkdf2:sha256')
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo, password_hash, rol, activo) VALUES (%s, %s, %s, 'admin', 1)",
            (nombre, correo, pwd_hash)
        )
        conexion.commit()
        print(f"✅ Administrador {correo} creado exitosamente.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conexion.close()

if __name__ == "__main__":
    # Cambia estos datos por los que necesites
    crear_admin("Admin Nuevo", "nuevoadmin@dunaka.com", "admin123")