import pymysql
pymysql.install_as_MySQLdb()


from flask import Flask
from config import Config

from .extensions import db, login_manager, admin_panel
from .auth import auth_bp
from .admin import configuracion_admin

from datetime import date



def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)

    admin_panel.init_app(app)

    app.register_blueprint(auth_bp)

    

    configuracion_admin()


    return app