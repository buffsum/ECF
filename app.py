from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import json

app = Flask(__name__)

# Configuration de la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zoo.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de l'extension SQLAlchemy
db = SQLAlchemy(app)

# Modèles (ajustés pour éviter la duplication)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'employee', 'veterinarian'

class Habitat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    animals = db.relationship('Animal', backref='habitat', lazy=True)
    # Pour le compteur de consultations
    consultation_count = db.Column(db.Integer, default=0)

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200))
    habitat_id = db.Column(db.Integer, db.ForeignKey('habitat.id'), nullable=False)
    vet_records = db.relationship('VetRecord', back_populates='animal', lazy=True)
    consultation_count = db.Column(db.Integer, default=0)  # Nouvelle colonne pour le compteur de consultations

class VetRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    food = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    health_status = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text, nullable=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    animal = db.relationship('Animal', back_populates='vet_records')
    consultation_count = db.Column(db.Integer, default=0)  # Nouveau champ pour le compteur de consultations

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

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/habitats')
def habitats():
    habitats = Habitat.query.all()
    return render_template('habitats.html', habitats=habitats)

# @app.route('/habitat/<int:habitat_id>')
# def habitat(habitat_id):
#     habitat = Habitat.query.get_or_404(habitat_id)
#     animals = Animal.query.filter_by(habitat_id=habitat_id).all()

#     # Récupère les enregistrements vétérinaires pour tous les animaux de l'habitat
#     vet_records_by_animal = {}
#     for animal in animals:
#         vet_records_by_animal[animal.id] = VetRecord.query.filter_by(animal_id=animal.id).all()

#     # Générez le nom du template basé sur l'habitat_id
#     template_name = f'habitat{habitat_id}.html'

#     # Rendre le template correspondant avec les données nécessaires
#     return render_template(template_name, habitat=habitat, animals=animals, vet_records_by_animal=vet_records_by_animal)
# @app.route('/habitat/<int:habitat_id>')
# def habitat(habitat_id):
#     habitat = Habitat.query.get_or_404(habitat_id)
#     animals = Animal.query.filter_by(habitat_id=habitat_id).all()

#     # Récupère le dernier enregistrement vétérinaire pour chaque animal de l'habitat
#     last_vet_records_by_animal = {}
#     for animal in animals:
#         # Trier les enregistrements vétérinaires par date en ordre décroissant et prendre le premier
#         last_vet_record = VetRecord.query.filter_by(animal_id=animal.id).order_by(VetRecord.date.desc()).first()
#         last_vet_records_by_animal[animal.id] = last_vet_record

#     # Générez le nom du template basé sur l'habitat_id
#     template_name = f'habitat{habitat_id}.html'

#     # Rendre le template correspondant avec les données nécessaires
#     return render_template(template_name, habitat=habitat, animals=animals, vet_records_by_animal=last_vet_records_by_animal)

@app.route('/habitat/<int:habitat_id>')
def habitat(habitat_id):
    habitat = Habitat.query.get_or_404(habitat_id)
    
    # Incrémenter le compteur de consultations
    habitat.consultation_count += 1
    db.session.commit()
    
    animals = Animal.query.filter_by(habitat_id=habitat_id).all()

    # Récupère le dernier enregistrement vétérinaire pour chaque animal de l'habitat
    last_vet_records_by_animal = {}
    for animal in animals:
        # Trier les enregistrements vétérinaires par date en ordre décroissant et prendre le premier
        last_vet_record = VetRecord.query.filter_by(animal_id=animal.id).order_by(VetRecord.date.desc()).first()
        last_vet_records_by_animal[animal.id] = last_vet_record

    # Générez le nom du template basé sur l'habitat_id
    template_name = f'habitat{habitat_id}.html'

    # Rendre le template correspondant avec les données nécessaires
    return render_template(template_name, habitat=habitat, animals=animals, vet_records_by_animal=last_vet_records_by_animal)

# @app.route('/admin', methods=['GET', 'POST'])
# def admin():
#     if request.method == 'POST':
#         try:
#             date_str = request.form['date']
#             food = request.form['food']
#             weight = float(request.form['weight'])
#             health_status = request.form['health_status']
#             details = request.form['details']
#             animal_id = int(request.form['animal_id'])

#             record_date = date.fromisoformat(date_str)

#             new_record = VetRecord(
#                 date=record_date, food=food, weight=weight,
#                 health_status=health_status, details=details,
#                 animal_id=animal_id
#             )

#             db.session.add(new_record)
#             db.session.commit()

#             # Incrémenter le compteur de consultations pour la fiche vétérinaire
#             new_record.consultation_count += 1
#             db.session.commit()

#             # Lire le fichier JSON, ajouter le nouvel enregistrement, puis réécrire le fichier
#             try:
#                 with open('vet_records.json', 'r') as f:
#                     vet_records = json.load(f)
#             except (FileNotFoundError, json.JSONDecodeError):
#                 vet_records = []

#             vet_records.append({
#                 'date': date_str,
#                 'food': food,
#                 'weight': weight,
#                 'health_status': health_status,
#                 'details': details,
#                 'animal_id': animal_id
#             })

#             with open('vet_records.json', 'w') as f:
#                 json.dump(vet_records, f, indent=4)

#             flash('Fiche vétérinaire ajoutée avec succès!', 'success')

#         # Incrémenter le compteur de consultations
#             if 'animal_id' in request.form:
#                 animal_id = int(request.form['animal_id'])
#                 animal = Animal.query.get_or_404(animal_id)
#                 animal.consultation_count += 1
#                 db.session.commit()
#                 flash('Consultation comptabilisée avec succès!', 'success')

#         except Exception as e:
#             db.session.rollback()
#             flash(f"Erreur lors de l'ajout de la fiche: {str(e)}", 'danger')

#     animals = Animal.query.all()
#     habitats = Habitat.query.all()  # Assurez-vous d'avoir la classe Habitat définie

#     # Filtres
#     date_filter = request.args.get('date')
#     animal_filter = request.args.get('animal_id')

#     query = VetRecord.query

#     if date_filter:
#         query = query.filter_by(date=date.fromisoformat(date_filter))
#     if animal_filter:
#         query = query.filter_by(animal_id=int(animal_filter))

#     vet_records = query.all()

#     return render_template('admin.html', animals=animals, vet_records=vet_records, habitats=habitats)

@app.route('/increment-consultation/<int:record_id>', methods=['POST'])
def increment_consultation(record_id):
    vet_record = VetRecord.query.get_or_404(record_id)  # Récupère l'enregistrement vétérinaire par ID
    vet_record.consultation_count += 1  # Incrémente le compteur de consultations
    db.session.commit()  # Enregistre les modifications dans la base de données
    return redirect(request.referrer)  # Redirige vers la page précédente

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        try:
            date_str = request.form['date']
            food = request.form['food']
            weight = float(request.form['weight'])
            health_status = request.form['health_status']
            details = request.form['details']
            animal_id = int(request.form['animal_id'])

            record_date = date.fromisoformat(date_str)

            # Créez et ajoutez le nouvel enregistrement dans la base de données
            new_record = VetRecord(
                date=record_date, food=food, weight=weight,
                health_status=health_status, details=details,
                animal_id=animal_id
            )

            db.session.add(new_record)
            db.session.commit()

            # Lire le fichier JSON, ajouter le nouvel enregistrement, puis réécrire le fichier
            try:
                with open('vet_records.json', 'r') as f:
                    vet_records = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                vet_records = []

            vet_records.append({
                'date': date_str,
                'food': food,
                'weight': weight,
                'health_status': health_status,
                'details': details,
                'animal_id': animal_id
            })

            with open('vet_records.json', 'w') as f:
                json.dump(vet_records, f, indent=4)

            flash('Fiche vétérinaire ajoutée avec succès!', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'ajout de la fiche: {str(e)}", 'danger')

    animals = Animal.query.all()
    habitats = Habitat.query.all()  # Ajoutez cette ligne pour récupérer les habitats

    # Filtres
    date_filter = request.args.get('date')
    animal_filter = request.args.get('animal_id')

    query = VetRecord.query

    if date_filter:
        query = query.filter_by(date=date.fromisoformat(date_filter))
    if animal_filter:
        query = query.filter_by(animal_id=int(animal_filter))

    vet_records = query.all()

    # Créez un dictionnaire pour stocker le nombre de consultations par animal
    consultation_counts = {animal.id: 0 for animal in animals}
    for record in vet_records:
        consultation_counts[record.animal_id] += 1

    return render_template('admin.html', animals=animals, vet_records=vet_records, habitats=habitats, consultation_counts=consultation_counts)

# @app.route('/admin', methods=['GET', 'POST'])
# def admin():
#     if request.method == 'POST':
#         try:
#             date_str = request.form['date']
#             food = request.form['food']
#             weight = float(request.form['weight'])
#             health_status = request.form['health_status']
#             details = request.form['details']
#             animal_id = int(request.form['animal_id'])

#             record_date = date.fromisoformat(date_str)

#             new_record = VetRecord(
#                 date=record_date, food=food, weight=weight,
#                 health_status=health_status, details=details,
#                 animal_id=animal_id
#             )

#             db.session.add(new_record)
#             db.session.commit()

#             # Lire le fichier JSON, ajouter le nouvel enregistrement, puis réécrire le fichier
#             try:
#                 with open('vet_records.json', 'r') as f:
#                     vet_records = json.load(f)
#             except (FileNotFoundError, json.JSONDecodeError):
#                 vet_records = []

#             vet_records.append({
#                 'date': date_str,
#                 'food': food,
#                 'weight': weight,
#                 'health_status': health_status,
#                 'details': details,
#                 'animal_id': animal_id
#             })

#             with open('vet_records.json', 'w') as f:
#                 json.dump(vet_records, f, indent=4)

#             flash('Fiche vétérinaire ajoutée avec succès!', 'success')

#         except Exception as e:
#             db.session.rollback()
#             flash(f"Erreur lors de l'ajout de la fiche: {str(e)}", 'danger')

#     animals = Animal.query.all()
#     habitats = Habitat.query.all()  # Ajoutez cette ligne pour récupérer les habitats

#     # Filtres
#     date_filter = request.args.get('date')
#     animal_filter = request.args.get('animal_id')

#     query = VetRecord.query

#     if date_filter:
#         query = query.filter_by(date=date.fromisoformat(date_filter))
#     if animal_filter:
#         query = query.filter_by(animal_id=int(animal_filter))

#     vet_records = query.all()

#     # Créez un dictionnaire pour stocker le nombre de consultations par animal
#     consultation_counts = {animal.id: 0 for animal in animals}
#     for record in vet_records:
#         consultation_counts[record.animal_id] += 1

#     return render_template('admin.html', animals=animals, vet_records=vet_records, habitats=habitats)


import commands

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée la base de données si elle n'existe pas
    app.run(debug=True)

# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# from datetime import date
# import json

# app = Flask(__name__)

# # Configuration de la base de données SQLite
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zoo.db'
# app.config['SECRET_KEY'] = 'your_secret_key'
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
#     # vet_records = db.relationship('VetRecord', backref='animal', lazy=True)
#     vet_records = db.relationship('VetRecord', back_populates='animal', lazy=True)


# # Modèle Fiche Vétérinaire
# class VetRecord(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.Date, nullable=False)
#     food = db.Column(db.String(100), nullable=False)
#     weight = db.Column(db.Float, nullable=False)
#     health_status = db.Column(db.String(200), nullable=False)
#     details = db.Column(db.Text, nullable=True)
#     animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
#     animal = db.relationship('Animal', back_populates='vet_records')

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
# def habitat(habitat_id):
#     habitat = Habitat.query.get_or_404(habitat_id)
#     animals = Animal.query.filter_by(habitat_id=habitat_id).all()

#     # Récupère les enregistrements vétérinaires pour tous les animaux de l'habitat
#     vet_records_by_animal = {}
#     for animal in animals:
#         vet_records_by_animal[animal.id] = VetRecord.query.filter_by(animal_id=animal.id).all()

#     # Générez le nom du template basé sur l'habitat_id
#     template_name = f'habitat{habitat_id}.html'

#     # Rendre le template correspondant avec les données nécessaires
#     return render_template(template_name, habitat=habitat, animals=animals, vet_records_by_animal=vet_records_by_animal)

# # Routes véto
# @app.route('/admin', methods=['GET', 'POST'])
# def admin():
#     if request.method == 'POST':
#         try:
#             date_str = request.form['date']
#             food = request.form['food']
#             weight = float(request.form['weight'])
#             health_status = request.form['health_status']
#             details = request.form['details']
#             animal_id = int(request.form['animal_id'])

#             record_date = date.fromisoformat(date_str)

#             new_record = VetRecord(
#                 date=record_date, food=food, weight=weight,
#                 health_status=health_status, details=details,
#                 animal_id=animal_id
#             )

#             db.session.add(new_record)
#             db.session.commit()

#             # Lire le fichier JSON, ajouter le nouvel enregistrement, puis réécrire le fichier
#             try:
#                 with open('vet_records.json', 'r') as f:
#                     vet_records = json.load(f)
#             except (FileNotFoundError, json.JSONDecodeError):
#                 vet_records = []

#             vet_records.append({
#                 'date': date_str,
#                 'food': food,
#                 'weight': weight,
#                 'health_status': health_status,
#                 'details': details,
#                 'animal_id': animal_id
#             })

#             with open('vet_records.json', 'w') as f:
#                 json.dump(vet_records, f, indent=4)

#             flash('Fiche vétérinaire ajoutée avec succès!', 'success')

#         except Exception as e:
#             db.session.rollback()
#             flash(f"Erreur lors de l'ajout de la fiche: {str(e)}", 'danger')

#     animals = Animal.query.all()
    
#     # Filtres
#     date_filter = request.args.get('date')
#     animal_filter = request.args.get('animal_id')

#     query = VetRecord.query

#     if date_filter:
#         query = query.filter_by(date=date.fromisoformat(date_filter))
#     if animal_filter:
#         query = query.filter_by(animal_id=int(animal_filter))

#     vet_records = query.all()

#     return render_template('admin.html', animals=animals, vet_records=vet_records)

# import commands

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()  # Crée la base de données si elle n'existe pas
#     app.run(debug=True)

