import os
import logging
from flask import Flask, render_template
# ---------------- for ihm -----------------------------
from db import db
from auth import Auth, login_required
from info import Info
from discount import Discount
from order import Order
from history import History
from products import Products
from static import Static
from statistiques import Statistiques
from paramapplication import ParamApplication
from accessDB import AccessDB


__prg_version__ = "0.4.8"
__prg_name__ = "crm_densmore"


toBoolean = {'true': True, 'false': False}

CRM_DENSMORE_PORT = int(os.environ.get('CRM_DENSMORE_PORT', '5000'))
CRM_DENSMORE_DEBUG = toBoolean.get(os.environ.get('CRM_DENSMORE_DEBUG', 'false'), True)
CRM_DENSMORE_HOST = os.environ.get('CRM_DENSMORE_HOST', '0.0.0.0')

app = Flask(__name__)
app.config["VERSION"] = __prg_version__
app.config["APP_PORT"] = CRM_DENSMORE_PORT
app.config["APP_HOST"] = CRM_DENSMORE_HOST
app.config["APP_DEBUG"] = CRM_DENSMORE_DEBUG
app.config['APP_NAME'] = os.environ.get('CRM_DENSMORE_NAME', 'CRM_DENSMORE')
app.config['APP_DESC'] = os.environ.get('CRM_DENSMORE_DESC', 'IHM management parameters')

# db SQLAlchemy
CRM_DENSMORE_DIR = os.environ.get('CRM_DENSMORE_DIR', os.path.dirname(os.path.abspath(__file__)))
database_file = "sqlite:///{}".format(os.path.join(CRM_DENSMORE_DIR, "crm_densmore.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# register Auth
app.register_blueprint(Auth(url_prefix="/"))
# register Info
app.register_blueprint(Info(url_prefix="/"))
# register Order
app.register_blueprint(Order(url_prefix="/"))
# register Discount
app.register_blueprint(Discount(url_prefix="/"))
# register History
app.register_blueprint(History(url_prefix="/"))
# register Products
app.register_blueprint(Products(url_prefix="/"))
# register Statistiques
app.register_blueprint(Statistiques(url_prefix="/"))
# register AccessDB
app.register_blueprint(AccessDB(url_prefix="/"))
# register Static
CRM_DENSMORE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
app.register_blueprint(Static(name="js", url_prefix="/javascripts/", path=os.path.join(CRM_DENSMORE_PATH, "javascripts")))
app.register_blueprint(Static(name="siimple", url_prefix="/siimple/", path=os.path.join(CRM_DENSMORE_PATH, "siimple")))
app.register_blueprint(Static(name="css", url_prefix="/css/", path=os.path.join(CRM_DENSMORE_PATH, "css")))
app.register_blueprint(Static(name="orders", url_prefix="/orders/", path=os.path.join(CRM_DENSMORE_PATH, "orders")))
app.register_blueprint(Static(name="simplepicker", url_prefix="/dist/", path=os.path.join(CRM_DENSMORE_PATH, "dist")))

# register CRM_densmoreApplication
app.register_blueprint(ParamApplication(url_prefix="/"))


@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    return render_template('index.html')


def create_app():
    db.init_app(app)
    with app.app_context():
        db.create_all()
    with app.app_context():
        for bp in app.blueprints:
            if 'init_db' in dir(app.blueprints[bp]):
                app.blueprints[bp].init_db()
    app.logger.setLevel(logging.DEBUG)
    app.secret_key = "wow c'est secret de fou furieux"
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host=CRM_DENSMORE_HOST, port=CRM_DENSMORE_PORT, debug=CRM_DENSMORE_DEBUG)
