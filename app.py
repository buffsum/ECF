from flask import Flask, render_template, request, redirect, url_for, flash
# from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import json
# import os

app = Flask(__name__)
# app.secret_key = 'votre_clé_secrète'  # Nécessaire pour que flash fonctionne

# Configuration de la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zoo.db'
app.config['SECRET_KEY'] = 'your_secret_key'
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

# @app.route('/admin')
# def admin():
#     return render_template('admin.html')

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
@app.route('/habitat/<int:habitat_id>')
def habitat(habitat_id):
    habitat = Habitat.query.get_or_404(habitat_id)
    animals = Animal.query.filter_by(habitat_id=habitat_id).all()

    # Récupère les enregistrements vétérinaires pour tous les animaux de l'habitat
    vet_records_by_animal = {}
    for animal in animals:
        vet_records_by_animal[animal.id] = VetRecord.query.filter_by(animal_id=animal.id).all()

    # Générez le nom du template basé sur l'habitat_id
    template_name = f'habitat{habitat_id}.html'

    # Rendre le template correspondant avec les données nécessaires
    return render_template(template_name, habitat=habitat, animals=animals, vet_records_by_animal=vet_records_by_animal)

# Pour le véto
# @app.route('/admin', methods=['GET', 'POST'])
# def admin():
#     if request.method == 'POST':
#         # Récupérer les données du formulaire
#         date = request.form['date']
#         food = request.form['food']
#         weight = request.form['weight']
#         health_status = request.form['health_status']
#         details = request.form['details']
#         animal_id = request.form['animal_id']
        
#         # Code pour ajouter la fiche vétérinaire dans la base de données
#         # (Ceci est un exemple, votre code peut varier)
        
#         flash('Fiche vétérinaire ajoutée avec succès!', 'success')
#         return redirect(url_for('admin'))
    
#     # Afficher la page admin si GET
#     return render_template('admin.html')

# @app.route('/admin', methods=['GET', 'POST'])
# def admin():
#     if request.method == 'POST':
#         # Récupérer les données du formulaire
#         date_str = request.form['date']
#         food = request.form['food']
#         weight = float(request.form['weight'])
#         health_status = request.form['health_status']
#         details = request.form['details']
#         animal_id = int(request.form['animal_id'])

#         # Convertir la chaîne de caractères en objet date
#         record_date = date.fromisoformat(date_str)

#         # Créer une nouvelle fiche vétérinaire
#         new_record = VetRecord(date=record_date, food=food, weight=weight, health_status=health_status, details=details, animal_id=animal_id)

#         try:
#             # Votre code pour créer et ajouter la fiche
#             db.session.commit()
#         except Exception as e:
#             db.session.rollback()
#             print(f"Erreur lors de l'enregistrement de la fiche: {e}")
#             flash(f"Erreur lors de l'enregistrement de la fiche: {e}", 'danger')

#         # Ajouter la fiche à la base de données
#         db.session.add(new_record)
#         db.session.commit()

#         # Message de confirmation
#         flash('Fiche vétérinaire ajoutée avec succès!', 'success')

#     # Récupérer la liste des animaux pour le menu déroulant
#     animals = Animal.query.all()

#     return render_template('admin.html', animals=animals)
# Routes
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        try:
            date_str = request.form['date']
            food = request.form['food']
            weight = float(request.form['weight'])
            health_status = request.form['health_status']
            details = request.form['details']
            animal_id = int(request.form['animal_id'])

            # Convertir la chaîne de caractères en objet date
            record_date = date.fromisoformat(date_str)

            # Créer une nouvelle fiche vétérinaire
            new_record = VetRecord(
                date=record_date, food=food, weight=weight,
                health_status=health_status, details=details,
                animal_id=animal_id
            )

            # Ajouter la fiche à la base de données
            db.session.add(new_record)
            db.session.commit()

            # Enregistrer dans un fichier JSON
            with open('vet_records.json', 'a') as f:
                json.dump({
                    'date': date_str,
                    'food': food,
                    'weight': weight,
                    'health_status': health_status,
                    'details': details,
                    'animal_id': animal_id
                }, f)
                f.write('\n')

            flash('Fiche vétérinaire ajoutée avec succès!', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'ajout de la fiche: {str(e)}", 'danger')

    # Récupérer la liste des animaux pour le menu déroulant
    animals = Animal.query.all()

    return render_template('admin.html', animals=animals)

import commands

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée la base de données si elle n'existe pas
    app.run(debug=True)

