from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import threading
from flask_cors import CORS  
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object('api.config.Config')
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    Migrate(app=app)

    CORS(app)

    with app.app_context():
        from api.routes import auth, rag, index
        app.register_blueprint(auth.bp)
        app.register_blueprint(rag.bp)
        app.register_blueprint(index.bp)
        db.create_all()

    return app

app = create_app()

