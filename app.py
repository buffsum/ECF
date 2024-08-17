from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration de la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zoo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de l'extension SQLAlchemy
db = SQLAlchemy(app)

# Modèle Utilisateur
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'employee', 'veterinarian'

# Modèle Habitat
class Habitat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    animals = db.relationship('Animal', backref='habitat', lazy=True)

# Modèle Animal
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200))
    habitat_id = db.Column(db.Integer, db.ForeignKey('habitat.id'), nullable=False)
    vet_records = db.relationship('VetRecord', backref='animal', lazy=True)

# Modèle Fiche Vétérinaire
class VetRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    food = db.Column(db.String(100))
    weight = db.Column(db.Float)
    health_status = db.Column(db.Text)
    details = db.Column(db.Text)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)

# Modèle Avis
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    approved = db.Column(db.Boolean, default=False)  # Non approuvé par défaut

# Routes pour les différentes pages
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/services')
def services():
    return render_template('services.html')

# Route pour afficher tous les habitats
@app.route('/habitats')
def habitats():
    habitats = Habitat.query.all()
    return render_template('habitats.html', habitats=habitats)

# Route pour afficher les détails d'un habitat spécifique et ses animaux
@app.route('/habitat/<int:habitat_id>')
def habitat_detail(habitat_id):
    habitat = Habitat.query.get_or_404(habitat_id)
    return render_template('habitat_detail.html', habitat=habitat)

# Route pour afficher les détails d'un animal spécifique et ses fiches vétérinaires
@app.route('/animal/<int:animal_id>')
def animal_detail(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    return render_template('animal_detail.html', animal=animal)

if __name__ == '__main__':
    db.create_all()  # Crée la base de données si elle n'existe pas
    app.run(debug=True)
