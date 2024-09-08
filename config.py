from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
import os
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zoo.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'laurane-c@hotmail.fr'
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_DEFAULT_SENDER'] = 'laurane-c@hotmail.fr'
mail = Mail(app)

db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///zoo.db'
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'laurane-c@hotmail.fr'
    MAIL_PASSWORD = 'your-email-password'
    MAIL_DEFAULT_SENDER = 'laurane-c@hotmail.fr'

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    with app.app_context():
        db.create_all()

    from commands import register_commands
    register_commands(app)

    return app

def role_required(role):
    from functools import wraps
    from flask import session, abort
    from models import User

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                abort(403)
            user = User.query.get(session['user_id'])
            if user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def save_avis_to_json():
    from models import Avis
    avis_list = Avis.query.all()
    avis_data = [
        {
            'nom': avis.nom,
            'pseudo': avis.pseudo,
            'titre': avis.titre,
            'message': avis.message,
            'approuve': avis.approuve
        }
        for avis in avis_list
    ]
    with open('avis.json', 'w') as f:
        json.dump(avis_data, f, indent=4)

def load_avis_from_json(file_path='avis.json'):
    with open(file_path, 'r') as file:
        avis = json.load(file)
    return avis

def load_services_from_json(file_path='services.json'):
    with open(file_path, 'r') as file:
        services = json.load(file)
        for service in services:
            new_service = Service(
                title=service['title'],
                description=service['description'],
                images_url=service.get('images_url', [])
            )
            db.session.add(new_service)
        db.session.commit()
        print("Services chargés depuis le fichier JSON.")


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS