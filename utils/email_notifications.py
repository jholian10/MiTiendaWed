from flask import current_app
from flask_mail import Message
from database.db import obtener_conexion

def obtener_correos_admins():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT correo FROM usuarios WHERE rol IN ('admin', 'superadmin') AND activo = 1")
    emails = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conexion.close()
    return emails

def enviar_alerta_stock(nombre_producto, stock_actual, stock_minimo):
    if stock_actual > stock_minimo:
        return

    destinatarios = obtener_correos_admins()
    print(f"DEBUG: Intentando enviar correo a {destinatarios} para el producto {nombre_producto}")

    if not destinatarios:
        print("DEBUG: No se encontraron administradores para enviar el correo.")
        return

    asunto = "🚨 Alerta de Inventario: " + ("AGOTADO" if stock_actual == 0 else "Stock Bajo")
    mensaje = f"El producto '{nombre_producto}' tiene {stock_actual} unidades (Mínimo: {stock_minimo})"

    try:
        msg = Message(asunto, recipients=destinatarios, body=mensaje)
        current_app.extensions['mail'].send(msg)
        print("DEBUG: ¡Correo enviado con éxito!")
    except Exception as e:
        print(f"DEBUG: ¡ERROR CRÍTICO AL ENVIAR CORREO! Error: {e}")