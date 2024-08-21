from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date

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
    # vet_records = db.relationship('VetRecord', backref='animal', lazy=True)
    vet_records = db.relationship('VetRecord', back_populates='animal', lazy=True)


# Modèle Fiche Vétérinaire
class VetRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    food = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    health_status = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text, nullable=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    animal = db.relationship('Animal', back_populates='vet_records')


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

# Route pour afficher les détails d'un habitat spécifique
# @app.route('/habitat/<int:habitat_id>')
# def habitat_detail(habitat_id):
#     habitat = Habitat.query.get_or_404(habitat_id)
#     animals = Animal.query.filter_by(habitat_id=habitat_id).all()

@app.route('/habitat/<int:habitat_id>')
def habitat1(habitat_id):
    habitat = Habitat.query.get_or_404(habitat_id)
    animals = Animal.query.filter_by(habitat_id=habitat_id).all()

    # Récupère les enregistrements vétérinaires pour tous les animaux de l'habitat
    vet_records_by_animal = {}
    for animal in animals:
        vet_records_by_animal[animal.id] = VetRecord.query.filter_by(animal_id=animal.id).all()

    return render_template('habitat1.html', habitat=habitat, animals=animals, vet_records_by_animal=vet_records_by_animal)


# @app.route('/habitat1')
# def habitat1(habitat_id):
#     habitat = Habitat.query.get_or_404(habitat_id)
#     animals = Animal.query.filter_by(habitat_id=habitat_id).all()

#     # Si un animal spécifique est sélectionné
#     animal_id = request.args.get('animal_id')
#     selected_animal = None
#     vet_records = None
#     if animal_id:
#         selected_animal = Animal.query.get(animal_id)
#         vet_records = VetRecord.query.filter_by(animal_id=animal_id).all()

#     return render_template('habitat1.html', habitat=habitat, animals=animals, selected_animal=selected_animal, vet_records=vet_records)

# Route pour afficher les détails d'un animal spécifique et ses fiches vétérinaires
# @app.route('/animal/<int:animal_id>')
# def animal_detail(animal_id):
#     animal = Animal.query.get_or_404(animal_id)
#     vet_records = VetRecord.query.filter_by(animal_id=animal_id).all()
#     return render_template('habitat1.html', animal=animal, vet_records=vet_records)
# on change ? j'ai remplacé animal_detail par habitat1.html

import commands

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée la base de données si elle n'existe pas
    app.run(debug=True)


# a voir si on ne revient pas à ça :
# def habitat1():
#     habitat = Habitat.query.get_or_404(1)
#     animals = Animal.query.filter_by(habitat_id=1).all()
#     vet_records_by_animal = {animal.id: VetRecord.query.filter_by(animal_id=animal.id).all() for animal in animals}
#     return render_template('habitat1.html', habitat=habitat, animals=animals, vet_records_by_animal=vet_records_by_animal)


    
    # Exemple de données pour un habitat spécifique
    
    # animal_example = Animal(name="Kibo", species="Zèbre", image="zebre1.jpg", description="Kibo est un zèbre calme et protecteur. Il est très attaché à son groupe et veille toujours à rester près de ses compagnons. Bien que plus réservé que Zara, Kibo est un observateur attentif et joue un rôle clé dans la cohésion du troupeau.")
    
    # vet_records_example = [
    #     VetRecord(date=date(2024, 1, 1), food="Herbes", weight=300, health_status="Bonne santé", details="Aucun problème détecté", animal_id=1),
    #     VetRecord(date=date(2024, 1, 10), food="Herbes", weight=305, health_status="Excellente santé", details="Contrôle de routine", animal_id=2),
    # ]


# if __name__ == '__main__':
#     db.create_all()  # Crée la base de données si elle n'existe pas
#     app.run(debug=True)

# from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# # Configuration de la base de données SQLite
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zoo.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialisation de l'extension SQLAlchemy
# db = SQLAlchemy(app)

# # Modèle Utilisateur
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)
#     role = db.Column(db.String(20), nullable=False)  # 'admin', 'employee', 'veterinarian'

# # Modèle Habitat
# class Habitat(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text)
#     image = db.Column(db.String(200))
#     animals = db.relationship('Animal', backref='habitat', lazy=True)

# # Modèle Animal
# class Animal(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     species = db.Column(db.String(100), nullable=False)
#     image = db.Column(db.String(200))
#     habitat_id = db.Column(db.Integer, db.ForeignKey('habitat.id'), nullable=False)
#     vet_records = db.relationship('VetRecord', backref='animal', lazy=True)

# # Modèle Fiche Vétérinaire
# class VetRecord(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.Date, nullable=False)
#     food = db.Column(db.String(100))
#     weight = db.Column(db.Float)
#     health_status = db.Column(db.Text)
#     details = db.Column(db.Text)
#     animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)

# # Modèle Avis
# class Review(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     visitor_name = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     approved = db.Column(db.Boolean, default=False)  # Non approuvé par défaut

# # Routes pour les différentes pages
# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

# @app.route('/register')
# def register():
#     return render_template('register.html')

# @app.route('/admin')
# def admin():
#     return render_template('admin.html')

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')

# @app.route('/services')
# def services():
#     return render_template('services.html')

# # Route pour afficher tous les habitats
# @app.route('/habitats')
# def habitats():
#     habitats = Habitat.query.all()
#     return render_template('habitats.html', habitats=habitats)

# # Route pour afficher les détails d'un habitat spécifique
# @app.route('/habitat/<int:habitat_id>')
# def habitat_detail(habitat_id):
#     # Dictionnaire de correspondance entre ID d'habitat et fichiers HTML
#     habitat_pages = {
#         1: 'habitat1.html',
#         2: 'habitat2.html',
#         3: 'habitat3.html',
#         4: 'habitat4.html'
#     }

#     # Obtenir le fichier HTML correspondant à l'ID d'habitat
#     habitat_page = habitat_pages.get(habitat_id, '404.html')  # Page par défaut si ID non trouvé

#     return render_template(habitat_page)


# @app.route('/habitat/<int:habitat_id>')
# def habitat1(habitat_id):
#     habitat = Habitat.query.get_or_404(habitat_id)
#     animals = Animal.query.filter_by(habitat_id=habitat_id).all()

#     # Récupère les enregistrements vétérinaires pour tous les animaux de l'habitat
#     vet_records_by_animal = {}
#     for animal in animals:
#         vet_records_by_animal[animal.id] = VetRecord.query.filter_by(animal_id=animal.id).all()

#     return render_template('habitat1.html', habitat=habitat, animals=animals, vet_records_by_animal=vet_records_by_animal)

# @app.route('/habitat/<int:habitat_id>')
# def habitat2(habitat_id):
#     habitat = Habitat.query.get_or_404(habitat_id)
#     animals = Animal.query.filter_by(habitat_id=habitat_id).all()

#     # Récupère les enregistrements vétérinaires pour tous les animaux de l'habitat
#     vet_records_by_animal = {}
#     for animal in animals:
#         vet_records_by_animal[animal.id] = VetRecord.query.filter_by(animal_id=animal.id).all()

#     return render_template('habitat2.html', habitat=habitat, animals=animals, vet_records_by_animal=vet_records_by_animal)

# def habitat3(habitat_id):
#     habitat = Habitat.query.get_or_404(habitat_id)
#     animals = Animal.query.filter_by(habitat_id=habitat_id).all()

#     # Récupère les enregistrements vétérinaires pour tous les animaux de l'habitat
#     vet_records_by_animal = {}
#     for animal in animals:
#         vet_records_by_animal[animal.id] = VetRecord.query.filter_by(animal_id=animal.id).all()

#     return render_template('habitat3.html', habitat=habitat, animals=animals, vet_records_by_animal=vet_records_by_animal)

# def habitat4(habitat_id):
#     habitat = Habitat.query.get_or_404(habitat_id)
#     animals = Animal.query.filter_by(habitat_id=habitat_id).all()

#     # Récupère les enregistrements vétérinaires pour tous les animaux de l'habitat
#     vet_records_by_animal = {}
#     for animal in animals:
#         vet_records_by_animal[animal.id] = VetRecord.query.filter_by(animal_id=animal.id).all()

#     return render_template('habitat4.html', habitat=habitat, animals=animals, vet_records_by_animal=vet_records_by_animal)

# # Route pour afficher les détails d'un animal spécifique et ses fiches vétérinaires
# @app.route('/animal/<int:animal_id>')
# def animal_detail(animal_id):
#     animal = Animal.query.get_or_404(animal_id)
#     return render_template('animal_detail.html', animal=animal)

# import commands

# if __name__ == '__main__':
#     db.create_all()  # Crée la base de données si elle n'existe pas
#     app.run(debug=True)