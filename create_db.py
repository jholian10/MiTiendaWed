import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

SQL_PATH = os.path.join(os.path.dirname(__file__), 'database', 'MiTiendaWeb_db_clean.sql')

def run_sql_file(path):
    with open(path, 'r', encoding='utf8') as f:
        sql = f.read()

    conn = None
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
            # Note: we intentionally do NOT pass the database parameter so we can create it
        )
        cursor = conn.cursor()
        # execute supports multi-statement execution
        for result in cursor.execute(sql, multi=True):
            pass
        conn.commit()
        print('✅ Base de datos y tablas creadas/actualizadas correctamente')
    except Exception as e:
        print(f'❌ Error al crear la base de datos: {e}')
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    if not os.path.exists(SQL_PATH):
        print(f'Archivo SQL no encontrado: {SQL_PATH}')
    else:
        run_sql_file(SQL_PATH)
