from flask import Flask
from routes.admin_routes import admin_blueprint
from routes.product_routes import product_blueprint 
from routes.auth_routes import auth_blueprint
from routes.cart_routes import cart_blueprint 
from routes.favorite_routes import favorite_blueprint 

# IMPORTACIÓN DESDE EL NUEVO ARCHIVO DE PAGOS
from routes.payment_routes import payment_blueprint 

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones'

# Registro de Blueprints de la plataforma
app.register_blueprint(admin_blueprint)
app.register_blueprint(product_blueprint) 
app.register_blueprint(auth_blueprint)
app.register_blueprint(cart_blueprint) 
app.register_blueprint(favorite_blueprint) 

# REGISTRO DEL BLUEPRINT DE PAGOS SEPARADO
app.register_blueprint(payment_blueprint) 

if __name__ == '__main__':
    app.run(debug=True)