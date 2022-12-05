import os
from flask import Flask, render_template
# ---------------- for ihm -----------------------------
from accessDB import AccessDB


__prg_version__ = "0.1.0"
__prg_name__ = "serveurBanque"


toBoolean = {'true': True, 'false': False}

SERVEUR_PORT = 5000
SERVEUR_DEBUG = True
SERVEUR_HOST = '0.0.0.0'

app = Flask(__name__)
app.config["VERSION"] = __prg_version__
app.config["APP_PORT"] = SERVEUR_PORT
app.config["APP_HOST"] = SERVEUR_HOST
app.config["APP_DEBUG"] = SERVEUR_DEBUG
app.config['APP_NAME'] = 'Serveur banque'
app.config['APP_DESC'] = 'IHM management parameters'

# db SQLAlchemy
SERVEUR_DIR = os.environ.get('SERVEUR_DIR', os.path.dirname(os.path.abspath(__file__)))



# register AccessDB
app.register_blueprint(AccessDB(url_prefix="/"))


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template('index.html')


def create_app():
    with app.app_context():
        for bp in app.blueprints:
            if 'init_db' in dir(app.blueprints[bp]):
                app.blueprints[bp].init_db()
    app.secret_key = "wow c'est secret de fou furieux"
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host=SERVEUR_HOST, port=SERVEUR_PORT, debug=SERVEUR_DEBUG)
