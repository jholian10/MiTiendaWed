from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv
import os

load_dotenv()

from routes.admin_routes import admin_blueprint
from routes.product_routes import product_blueprint 
from routes.auth_routes import auth_blueprint, init_oauth 
from routes.cart_routes import cart_blueprint 
from routes.favorite_routes import favorite_blueprint 
from routes.payment_routes import payment_blueprint
from routes.profile_routes import profile_blueprint
from routes.order_routes import order_custom_bp 
from routes.admin_routes import admin_blueprint
from routes.support_routes import support_blueprint 

app = Flask(__name__)
print("Ruta de templates configurada:", app.template_folder)
print("Directorio actual:", os.getcwd())
app.secret_key = os.getenv('SECRET_KEY', 'clave_secreta_para_sesiones')

# Configuración de Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

init_oauth(app)

app.register_blueprint(admin_blueprint)
app.register_blueprint(product_blueprint) 
app.register_blueprint(auth_blueprint) 
app.register_blueprint(cart_blueprint) 
app.register_blueprint(favorite_blueprint) 
app.register_blueprint(payment_blueprint) 
app.register_blueprint(profile_blueprint)
app.register_blueprint(order_custom_bp)
# AGREGADO: Registra el blueprint de soporte
app.register_blueprint(support_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)