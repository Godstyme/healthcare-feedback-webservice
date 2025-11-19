from flask import Flask
from config import Config
from extensions.db import db
from extensions.jwt import jwt
from extensions.bcrypt import bcrypt
from flask_migrate import Migrate
from routes.user_routes import user_bp
from routes.patient_routes import patient_bp
from routes.admin_routes import admin_bp



from routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp) 
    app.register_blueprint(patient_bp)
    app.register_blueprint(admin_bp)

    return app


app = create_app()

if __name__ == "__main__":
    print("🚀 Starting Flask development server...")
    app.run(debug=True, host="127.0.0.1", port=5000)
