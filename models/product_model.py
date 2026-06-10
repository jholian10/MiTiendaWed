from database.db import obtener_conexion

def listar_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_url, estado 
        FROM productos WHERE estado = 1
    """)
    productos = cursor.fetchall()  # Recupera la lista completa
    cursor.close()
    conexion.close()
    return productos

def insertar_producto(nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_url):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
        INSERT INTO productos (nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_url) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_url))
    conexion.commit()
    cursor.close()
    conexion.close()

def obtener_producto_por_id(id_producto):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id = %s", (id_producto,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()
    return producto

def actualizar_producto(id_producto, nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_url):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
        UPDATE productos 
        SET nombre=%s, descripcion=%s, precio_compra=%s, precio_venta=%s, stock=%s, stock_minimo=%s, imagen_url=%s 
        WHERE id=%s
    """
    cursor.execute(query, (nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_url, id_producto))
    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar_producto_por_id(id_producto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    # Eliminación lógica (cambia estado a 0) para no perder el histórico de ventas
    cursor.execute("UPDATE productos SET estado = 0 WHERE id = %s", (id_producto,))
    conexion.commit()
    cursor.close()
    conexion.close()

# ===================================================
# NUEVA FUNCIÓN: BUSCADOR FILTRADO DE PRODUCTOS ACTIVOS
# ===================================================
def buscar_productos_por_nombre(termino):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    # Consulta que busca coincidencia parcial en nombre o descripción, respetando que el producto esté activo
    query = """
        SELECT id, nombre, descripcion, precio_compra, precio_venta, stock, stock_minimo, imagen_url, estado 
        FROM productos 
        WHERE (nombre LIKE %s OR descripcion LIKE %s) AND estado = 1
    """
    
    # Configura el comodín para la búsqueda parcial con LIKE
    comodin = f"%{termino}%"
    
    cursor.execute(query, (comodin, comodin))
    productos = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    return productos