from database.db import obtener_conexion

try:
    conn = obtener_conexion()
    cursor = conn.cursor()


    cursor.execute("""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME='usuarios' AND COLUMN_NAME='foto_perfil_url'
    """)
    existe = cursor.fetchone()

    if not existe:
        print('❌ Columna NO existe. Agregando...')
        cursor.execute('ALTER TABLE usuarios ADD COLUMN foto_perfil_url VARCHAR(255) DEFAULT NULL')
        conn.commit()
        print('✅ Columna foto_perfil_url agregada correctamente')
    else:
        print('✅ Columna foto_perfil_url ya existe')

    cursor.close()
    conn.close()
except Exception as e:
    print(f'❌ Error: {e}')
