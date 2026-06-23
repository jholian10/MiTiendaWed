import os
from flask import current_app
from flask_mail import Message
from database.db import obtener_conexion

def obtener_correos_administradores():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT correo FROM usuarios WHERE rol IN ('admin', 'superadmin') AND activo = 1")
        usuarios = cursor.fetchall()
        return [u['correo'] for u in usuarios]
    finally:
        cursor.close()
        conexion.close()

def enviar_alerta_stock_email(nombre_producto, stock_actual):
    destinatarios = obtener_correos_administradores()
    if not destinatarios:
        return False

    es_agotado = stock_actual <= 0
    asunto = f"🚨 ¡AGOTADO!: {nombre_producto}" if es_agotado else f"⚠️ Stock Bajo: {nombre_producto}"
    color_alerta = "#ef4444" if es_agotado else f"#f59e0b"
    texto_estado = "se ha quedado sin existencias por completo." if es_agotado else f"está próximo a agotarse. Quedan solo {stock_actual} unidades."

    try:
        msg = Message(
            subject=asunto,
            sender=os.getenv('MAIL_USERNAME'),
            recipients=destinatarios
        )

        msg.html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="background-color: #f4f7fa; padding: 40px 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 24px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.08); border: 1px solid #eef2f6;">
                
                <div style="padding: 30px; text-align: center; border-bottom: 1px solid #f1f5f9; background-color: #5d58ef;">
                    <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 800;">Dunaka Panel</h1>
                </div>

                <div style="padding: 40px; text-align: center;">
                    <div style="display: inline-block; padding: 12px 24px; background-color: {color_alerta}20; border-radius: 50px; margin-bottom: 25px;">
                        <span style="color: {color_alerta}; font-weight: 700; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">
                            Alerta de Inventario
                        </span>
                    </div>

                    <h2 style="color: #0f172a; margin: 0 0 20px 0; font-size: 22px; font-weight: 700;">{nombre_producto}</h2>
                    
                    <p style="color: #475569; line-height: 1.8; font-size: 16px; margin: 0 0 30px 0;">
                        El producto <strong>{nombre_producto}</strong> {texto_estado}
                    </p>
                    
                    <div style="background-color: #f8fafc; border-radius: 16px; padding: 20px; margin-bottom: 35px; border: 1px solid #e2e8f0; display: inline-block; width: 80%;">
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="text-align: left; color: #64748b; font-size: 15px; padding: 6px 0;">Estado:</td>
                                <td style="text-align: right; color: {color_alerta}; font-weight: 700; font-size: 15px; padding: 6px 0;">
                                    {"AGOTADO" if es_agotado else "STOCK BAJO"}
                                </td>
                            </tr>
                            <tr>
                                <td style="text-align: left; color: #64748b; font-size: 15px; padding: 6px 0;">Unidades restantes:</td>
                                <td style="text-align: right; color: #1e293b; font-weight: 700; font-size: 15px; padding: 6px 0;">{stock_actual}</td>
                            </tr>
                        </table>
                    </div>

                    <a href="http://127.0.0.1:5000/admin/inventario" style="display: inline-block; padding: 15px 40px; background-color: #5d58ef; color: #ffffff; text-decoration: none; border-radius: 50px; font-weight: 600; font-size: 15px; box-shadow: 0 4px 15px rgba(93, 88, 239, 0.3);">
                        Gestionar Inventario
                    </a>
                </div>

                <div style="background-color: #f8fafc; padding: 25px; text-align: center; border-top: 1px solid #e2e8f0;">
                    <p style="color: #94a3b8; font-size: 12px; margin: 0;">
                        Este es un correo automático generado por el sistema de inventario de Dunaka.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        current_app.extensions['mail'].send(msg)
        return True
    except Exception as e:
        print(f"ERROR: No se pudo enviar el correo de alerta de stock: {e}")
        return False