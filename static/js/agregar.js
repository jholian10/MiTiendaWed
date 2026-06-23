# Dentro de @admin_blueprint.route('/producto/nuevo', methods=['GET', 'POST'])
# Busca el bloque de la imagen y déjalo estructurado así:

imagen_final = ""
if imagen_file and imagen_file.filename != '':
    os.makedirs('static/uploads', exist_ok=True)
    filename = secure_filename(imagen_file.filename)
    imagen_file.save(os.path.join('static/uploads', filename))
    imagen_final = f'/static/uploads/{filename}'
elif imagen_url and imagen_url.strip() != "":
    imagen_final = imagen_url.strip()
else:
    # IMAGEN POR DEFECTO: Si el usuario no subió nada, usa esta silueta estándar
    imagen_final = '/static/uploads/default_bolso.png'