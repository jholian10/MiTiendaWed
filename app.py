from flask import Flask
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

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'clave_secreta_para_sesiones')

init_oauth(app)

app.register_blueprint(admin_blueprint)
app.register_blueprint(product_blueprint) 
app.register_blueprint(auth_blueprint) 
app.register_blueprint(cart_blueprint) 
app.register_blueprint(favorite_blueprint) 
app.register_blueprint(payment_blueprint) 
app.register_blueprint(profile_blueprint)
app.register_blueprint(order_custom_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)