from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
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

# Modèles
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

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200))
    habitat_id = db.Column(db.Integer, db.ForeignKey('habitat.id'), nullable=False)
    vet_records = db.relationship('VetRecord', back_populates='animal', lazy=True)

class VetRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    food = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    health_status = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text, nullable=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    animal = db.relationship('Animal', back_populates='vet_records')
    consultation_count = db.Column(db.Integer, default=0)  # Nouveau champ pour le compteur de consultations

class Avis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    pseudo = db.Column(db.String(100), nullable=False)
    titre = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    approuve = db.Column(db.Boolean, default=False)

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                abort(403)  # Forbidden
            user = User.query.get(session['user_id'])
            if user.role != role:
                abort(403)  # Forbidden
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/submit_review', methods=['POST'])
def submit_review():
    nom = request.form['nom']
    pseudo = request.form['pseudo']
    titre = request.form['title']
    message = request.form['message']
    
    nouvel_avis = Avis(nom=nom, pseudo=pseudo, titre=titre, message=message)
    db.session.add(nouvel_avis)
    db.session.commit()
    
    flash('Votre avis a été soumis et est en attente de validation.')
    return redirect(url_for('index'))

@app.route('/approve_review/<int:avis_id>')
def approve_review(avis_id):
    avis = Avis.query.get_or_404(avis_id)
    avis.approuve = True
    db.session.commit()
    flash('Avis approuvé.')
    return redirect(url_for('admin'))

@app.route('/disapprove_review/<int:avis_id>')
def disapprove_review(avis_id):
    avis = Avis.query.get_or_404(avis_id)
    db.session.delete(avis)
    db.session.commit()
    flash('Avis supprimé.')
    return redirect(url_for('admin'))

# Routes pour les différentes pages

@app.route('/')
def home():
    # Récupérer les avis validés (approuvés)
    avis_valides = Avis.query.filter_by(approuve=True).all()
    return render_template('index.html', avis_valides=avis_valides)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("TEST")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_role'] = user.role
            flash('Connexion réussie!', 'success')
            if user.role == 'admin':
                return redirect(url_for('admin'))
            elif user.role == 'employee':
                return redirect(url_for('employee'))
            elif user.role == 'veterinarian':
                return redirect(url_for('veterinarian'))
            else:
                return redirect(url_for('home'))
        else:
            flash('Nom d\'utilisateuuuuur ou mot de passe incorrect', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_role', None)
    flash('Vous avez été déconnecté.', 'success')
    return redirect(url_for('home'))

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

@app.route('/habitat/<int:habitat_id>')
def habitat(habitat_id):
    habitat = Habitat.query.get_or_404(habitat_id)
    
    db.session.commit()
    
    animals = Animal.query.filter_by(habitat_id=habitat_id).all()

    # Récupère le dernier enregistrement vétérinaire pour chaque animal de l'habitat
    last_vet_records_by_animal = {}
    for animal in animals:
        last_vet_record = VetRecord.query.filter_by(animal_id=animal.id).order_by(VetRecord.date.desc()).first()
        last_vet_records_by_animal[animal.id] = last_vet_record
        print(f"Animal ID: {animal.id}, Consultation Count: {last_vet_record.consultation_count if last_vet_record else 'No records'}")

    template_name = f'habitat{habitat_id}.html'
    return render_template(template_name, habitat=habitat, animals=animals, vet_records_by_animal=last_vet_records_by_animal)

@app.route('/increment-consultation/<int:animal_id_here>', methods=['POST'])
def increment_consultation(animal_id_here):
    animal_in_question = Animal.query.get_or_404(animal_id_here)
    
    animals = Animal.query.filter_by(habitat_id=animal_in_question.habitat_id).all()

    last_vet_records_by_animal = {}
    for animal in animals:
        last_vet_record = VetRecord.query.filter_by(animal_id=animal.id).order_by(VetRecord.date.desc()).first()
        last_vet_records_by_animal[animal.id] = last_vet_record
    last_vet_record = last_vet_records_by_animal.get(animal_id_here)

    if last_vet_record:
        print(f"TEST animal id: {animal_id_here}, vet record id : {last_vet_record.id}")
        last_vet_record.consultation_count += 1
    else:
        print(f"TEST animal id: {animal_id_here}, no vet records found")

    db.session.commit()
    return redirect(request.referrer)

@app.route('/admin', methods=['GET', 'POST'])
@role_required('admin')
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

            new_record = VetRecord(
                date=record_date, food=food, weight=weight,
                health_status=health_status, details=details,
                animal_id=animal_id
            )

            db.session.add(new_record)
            db.session.commit()

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

    filter_date = request.args.get('date')
    filter_animal_id = request.args.get('animal_id')

    query = VetRecord.query

    if filter_date:
        query = query.filter(VetRecord.date == date.fromisoformat(filter_date))

    if filter_animal_id:
        query = query.filter(VetRecord.animal_id == filter_animal_id)

    animals = Animal.query.all()
    vet_records = query.all()
    habitats = Habitat.query.all()
    
    consultation_counts = {animal.id: 0 for animal in animals}
    for record in vet_records:
        consultation_counts[record.animal_id] += record.consultation_count

    avis_a_valider = Avis.query.filter_by(approuve=False).all()

    return render_template('admin.html', avis_a_valider=avis_a_valider, animals=animals, vet_records=vet_records, habitats=habitats, consultation_counts=consultation_counts)

@app.route('/employee')
@role_required('employee')
def employee():
    return render_template('employee.html')

@app.route('/veterinarian')
@role_required('veterinarian')
def veterinarian():
    return render_template('veterinarian.html')

import commands

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


# from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
# from functools import wraps
# from werkzeug.security import check_password_hash, generate_password_hash
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

# # Modèles (ajustés pour éviter la duplication)
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)
#     role = db.Column(db.String(20), nullable=False)  # 'admin', 'employee', 'veterinarian'

# class Habitat(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text)
#     image = db.Column(db.String(200))
#     animals = db.relationship('Animal', backref='habitat', lazy=True)

# class Animal(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     species = db.Column(db.String(100), nullable=False)
#     image = db.Column(db.String(200))
#     habitat_id = db.Column(db.Integer, db.ForeignKey('habitat.id'), nullable=False)
#     vet_records = db.relationship('VetRecord', back_populates='animal', lazy=True)

# class VetRecord(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     date = db.Column(db.Date, nullable=False)
#     food = db.Column(db.String(100), nullable=False)
#     weight = db.Column(db.Float, nullable=False)
#     health_status = db.Column(db.String(200), nullable=False)
#     details = db.Column(db.Text, nullable=True)
#     animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
#     animal = db.relationship('Animal', back_populates='vet_records')
#     consultation_count = db.Column(db.Integer, default=0)  # Nouveau champ pour le compteur de consultations

# class Avis(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nom = db.Column(db.String(100), nullable=False)
#     pseudo = db.Column(db.String(100), nullable=False)
#     titre = db.Column(db.String(100), nullable=False)
#     message = db.Column(db.Text, nullable=False)
#     approuve = db.Column(db.Boolean, default=False)

# def role_required(role):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             if 'user_id' not in session:
#                 abort(403)  # Forbidden
#             user = User.query.get(session['user_id'])
#             if user.role != role:
#                 abort(403)  # Forbidden
#             return f(*args, **kwargs)
#         return decorated_function
#     return decorator

# @app.route('/submit_review', methods=['POST'])
# def submit_review():
#     nom = request.form['nom']
#     pseudo = request.form['pseudo']
#     titre = request.form['title']
#     message = request.form['message']
    
#     nouvel_avis = Avis(nom=nom, pseudo=pseudo, titre=titre, message=message)
#     db.session.add(nouvel_avis)
#     db.session.commit()
    
#     flash('Votre avis a été soumis et est en attente de validation.')
#     return redirect(url_for('home'))

# @app.route('/approve_review/<int:avis_id>')
# def approve_review(avis_id):
#     avis = Avis.query.get_or_404(avis_id)
#     avis.approuve = True
#     db.session.commit()
#     flash('Avis approuvé.')
#     return redirect(url_for('admin'))

# @app.route('/disapprove_review/<int:avis_id>')
# def disapprove_review(avis_id):
#     avis = Avis.query.get_or_404(avis_id)
#     db.session.delete(avis)
#     db.session.commit()
#     flash('Avis supprimé.')
#     return redirect(url_for('admin'))

# # Routes pour les différentes pages

# @app.route('/')
# def index():
# # def home():
#     # Récupérer les avis validés (approuvés)
#     avis_valides = Avis.query.filter_by(approuve=True).all()
#     return render_template('index.html', avis_valides=avis_valides)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         print("TEST2")
#         if user and check_password_hash(user.password, password):
#             print("TESSSSST")
#             session['user_id'] = user.id
#             session['user_role'] = user.role
#             if user.role == 'admin':
#                 return redirect(url_for('admin'))
#             else:
#                 print("Admin not ok")
#                 return redirect(url_for('index'))
#         else:
#             return "Nom d'utilisateur ou mot de passe incorrect"
#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     session.pop('user_role', None)
#     flash('Vous avez été déconnecté.', 'success')
#     return redirect(url_for('login'))

# @app.route('/register')
# def register():
#     return render_template('register.html')

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')

# @app.route('/services')
# def services():
#     return render_template('services.html')

# @app.route('/habitats')
# def habitats():
#     habitats = Habitat.query.all()
#     return render_template('habitats.html', habitats=habitats)

# @app.route('/habitat/<int:habitat_id>')
# def habitat(habitat_id):
#     habitat = Habitat.query.get_or_404(habitat_id)
    
#     db.session.commit()
    
#     animals = Animal.query.filter_by(habitat_id=habitat_id).all()

#     # Récupère le dernier enregistrement vétérinaire pour chaque animal de l'habitat
#     last_vet_records_by_animal = {}
#     for animal in animals:
#         last_vet_record = VetRecord.query.filter_by(animal_id=animal.id).order_by(VetRecord.date.desc()).first()
#         last_vet_records_by_animal[animal.id] = last_vet_record
#         print(f"Animal ID: {animal.id}, Consultation Count: {last_vet_record.consultation_count if last_vet_record else 'No records'}")

#     template_name = f'habitat{habitat_id}.html'
#     return render_template(template_name, habitat=habitat, animals=animals, vet_records_by_animal=last_vet_records_by_animal)

# @app.route('/increment-consultation/<int:animal_id_here>', methods=['POST'])
# def increment_consultation(animal_id_here):
#     animal_in_question = Animal.query.get_or_404(animal_id_here)
    
#     animals = Animal.query.filter_by(habitat_id=animal_in_question.habitat_id).all()

#     last_vet_records_by_animal = {}
#     for animal in animals:
#         last_vet_record = VetRecord.query.filter_by(animal_id=animal.id).order_by(VetRecord.date.desc()).first()
#         last_vet_records_by_animal[animal.id] = last_vet_record
#     last_vet_record = last_vet_records_by_animal.get(animal_id_here)

#     if last_vet_record:
#         print(f"TEST animal id: {animal_id_here}, vet record id : {last_vet_record.id}")
#         last_vet_record.consultation_count += 1
#     else:
#         print(f"TEST animal id: {animal_id_here}, no vet records found")

#     db.session.commit()
#     return redirect(request.referrer)

# @app.route('/admin', methods=['GET', 'POST'])
# @role_required('admin')
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

#     filter_date = request.args.get('date')
#     filter_animal_id = request.args.get('animal_id')

#     query = VetRecord.query

#     if filter_date:
#         query = query.filter(VetRecord.date == date.fromisoformat(filter_date))

#     if filter_animal_id:
#         query = query.filter(VetRecord.animal_id == filter_animal_id)

#     animals = Animal.query.all()
#     vet_records = query.all()
#     habitats = Habitat.query.all()
    
#     consultation_counts = {animal.id: 0 for animal in animals}
#     for record in vet_records:
#         consultation_counts[record.animal_id] += record.consultation_count

#     avis_a_valider = Avis.query.filter_by(approuve=False).all()

#     return render_template('admin.html', avis_a_valider=avis_a_valider, animals=animals, vet_records=vet_records, habitats=habitats, consultation_counts=consultation_counts)

# @app.route('/employee')
# @role_required('employee')
# def employee_page():
#     return render_template('employee.html')

# @app.route('/veterinarian')
# @role_required('veterinarian')
# def veterinarian_page():
#     return render_template('veterinarian.html')

# import commands

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
    
# # from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
# # from functools import wraps
# # from werkzeug.security import check_password_hash, generate_password_hash
# # from flask_sqlalchemy import SQLAlchemy
# # from datetime import date
# # import json

# # app = Flask(__name__)

# # # Configuration de la base de données SQLite
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zoo.db'
# # app.config['SECRET_KEY'] = 'your_secret_key'
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # # Initialisation de l'extension SQLAlchemy
# # db = SQLAlchemy(app)

# # # Modèles (ajustés pour éviter la duplication)
# # class User(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     username = db.Column(db.String(120), unique=True, nullable=False)
# #     password = db.Column(db.String(120), nullable=False)
# #     role = db.Column(db.String(20), nullable=False)  # 'admin', 'employee', 'veterinarian'

# # class Habitat(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     name = db.Column(db.String(100), nullable=False)
# #     description = db.Column(db.Text)
# #     image = db.Column(db.String(200))
# #     animals = db.relationship('Animal', backref='habitat', lazy=True)
# #     # Pour le compteur de consultations
# #     # consultation_count = db.Column(db.Integer, default=0)

# # class Animal(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     name = db.Column(db.String(100), nullable=False)
# #     species = db.Column(db.String(100), nullable=False)
# #     image = db.Column(db.String(200))
# #     habitat_id = db.Column(db.Integer, db.ForeignKey('habitat.id'), nullable=False)
# #     vet_records = db.relationship('VetRecord', back_populates='animal', lazy=True)
# #     # consultation_count = db.Column(db.Integer, default=0)  # Nouvelle colonne pour le compteur de consultations

# # class VetRecord(db.Model):
# #     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
# #     date = db.Column(db.Date, nullable=False)
# #     food = db.Column(db.String(100), nullable=False)
# #     weight = db.Column(db.Float, nullable=False)
# #     health_status = db.Column(db.String(200), nullable=False)
# #     details = db.Column(db.Text, nullable=True)
# #     animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
# #     animal = db.relationship('Animal', back_populates='vet_records')
# #     consultation_count = db.Column(db.Integer, default=0)  # Nouveau champ pour le compteur de consultations

# # # class Review(db.Model):
# # #     id = db.Column(db.Integer, primary_key=True)
# # #     visitor_name = db.Column(db.String(100), nullable=False)
# # #     content = db.Column(db.Text, nullable=False)
# # #     approved = db.Column(db.Boolean, default=False)  # Non approuvé par défaut

# # class Avis(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     nom = db.Column(db.String(100), nullable=False)
# #     pseudo = db.Column(db.String(100), nullable=False)
# #     titre = db.Column(db.String(100), nullable=False)
# #     message = db.Column(db.Text, nullable=False)
# #     approuve = db.Column(db.Boolean, default=False)

# # def role_required(role):
# #     def decorator(f):
# #         @wraps(f)
# #         def decorated_function(*args, **kwargs):
# #             if 'user_id' not in session:
# #                 abort(403)  # Forbidden
# #             user = User.query.get(session['user_id'])
# #             if user.role != role:
# #                 abort(403)  # Forbidden
# #             return f(*args, **kwargs)
# #         return decorated_function
# #     return decorator

# # @app.route('/submit_review', methods=['POST'])
# # def submit_review():
# #     nom = request.form['nom']
# #     pseudo = request.form['pseudo']
# #     titre = request.form['title']
# #     message = request.form['message']
    
# #     nouvel_avis = Avis(nom=nom, pseudo=pseudo, titre=titre, message=message)
# #     db.session.add(nouvel_avis)
# #     db.session.commit()
    
# #     flash('Votre avis a été soumis et est en attente de validation.')
# #     return redirect(url_for('home'))

# # @app.route('/approve_review/<int:avis_id>')
# # def approve_review(avis_id):
# #     avis = Avis.query.get_or_404(avis_id)
# #     avis.approuve = True
# #     db.session.commit()
# #     flash('Avis approuvé.')
# #     return redirect(url_for('admin'))

# # @app.route('/disapprove_review/<int:avis_id>')
# # def disapprove_review(avis_id):
# #     avis = Avis.query.get_or_404(avis_id)
# #     db.session.delete(avis)
# #     db.session.commit()
# #     flash('Avis supprimé.')
# #     return redirect(url_for('admin'))

# # # Routes pour les différentes pages

# # @app.route('/')
# # def home():
# #     # Récupérer les avis validés (approuvés)
# #     avis_valides = Avis.query.filter_by(approuve=True).all()
# #     return render_template('index.html', avis_valides=avis_valides)

# # # @app.route('/login', methods=['GET', 'POST'])
# # # def login():
# # #     if request.method == 'POST':
# # #         username = request.form['username']
# # #         password = request.form['password']
# # #         user = User.query.filter_by(username=username).first()
# # #         if user and check_password_hash(user.password, password):
# # #             session['user_id'] = user.id
# # #             session['user_role'] = user.role
# # #             return redirect(url_for('index'))
# # #         else:
# # #             return "Nom d'utilisateur ou mot de passe incorrect"
# # #     return render_template('login.html')
# # @app.route('/login', methods=['GET', 'POST'])
# # def login():
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']
# #         user = User.query.filter_by(username=username).first()
# #         if user and check_password_hash(user.password, password):
# #             session['user_id'] = user.id
# #             session['user_role'] = user.role
# #             if user.role == 'admin':
# #                 return redirect(url_for('admin'))
# #             else:
# #                 return redirect(url_for('index'))
# #         else:
# #             return "Nom d'utilisateur ou mot de passe incorrect"
# #     return render_template('login.html')

# # @app.route('/logout')
# # def logout():
# #     session.pop('user_id', None)
# #     session.pop('user_role', None)
# #     return redirect(url_for('login'))

# # @app.route('/register')
# # def register():
# #     return render_template('register.html')

# # @app.route('/contact')
# # def contact():
# #     return render_template('contact.html')

# # @app.route('/services')
# # def services():
# #     return render_template('services.html')

# # @app.route('/habitats')
# # def habitats():
# #     habitats = Habitat.query.all()
# #     return render_template('habitats.html', habitats=habitats)

# # @app.route('/habitat/<int:habitat_id>')
# # def habitat(habitat_id):
# #     habitat = Habitat.query.get_or_404(habitat_id)
    
# #     # Incrémenter le compteur de consultations
# #     # habitat.consultation_count += 1
# #     db.session.commit()
    
# #     animals = Animal.query.filter_by(habitat_id=habitat_id).all()

# #     # Récupère le dernier enregistrement vétérinaire pour chaque animal de l'habitat
# #     last_vet_records_by_animal = {}
# #     for animal in animals:
# #         # Trier les enregistrements vétérinaires par date en ordre décroissant et prendre le premier
# #         last_vet_record = VetRecord.query.filter_by(animal_id=animal.id).order_by(VetRecord.date.desc()).first()
# #         last_vet_records_by_animal[animal.id] = last_vet_record
# #         print(f"Animal ID: {animal.id}, Consultation Count: {last_vet_record.consultation_count if last_vet_record else 'No records'}")  # Ajoute ceci pour déboguer

# #     # Générez le nom du template basé sur l'habitat_id
# #     template_name = f'habitat{habitat_id}.html'

# #     # Rendre le template correspondant avec les données nécessaires
# #     return render_template(template_name, habitat=habitat, animals=animals, vet_records_by_animal=last_vet_records_by_animal)

# # @app.route('/increment-consultation/<int:animal_id_here>', methods=['POST'])
# # def increment_consultation(animal_id_here):
# #     animal_in_question = Animal.query.get_or_404(animal_id_here)  # Récupère l'animal par ID
    
# #     animals = Animal.query.filter_by(habitat_id=animal_in_question.habitat_id).all()

# #     # Récupère le dernier enregistrement vétérinaire pour chaque animal de l'habitat
# #     last_vet_records_by_animal = {}
# #     for animal in animals:
# #         # Trier les enregistrements vétérinaires par date en ordre décroissant et prendre le premier
# #         last_vet_record = VetRecord.query.filter_by(animal_id=animal.id).order_by(VetRecord.date.desc()).first()
# #         last_vet_records_by_animal[animal.id] = last_vet_record
# #     last_vet_record = last_vet_records_by_animal.get(animal_id_here)

# #     if last_vet_record:
# #         print(f"TEST animal id: {animal_id_here}, vet record id : {last_vet_record.id}")
# #         last_vet_record.consultation_count += 1  # Incrémente le compteur de consultations
# #     else:
# #         print(f"TEST animal id: {animal_id_here}, no vet records found")

# #     db.session.commit()  # Enregistre les modifications dans la base de données
# #     return redirect(request.referrer)  # Redirige vers la page précédente

# # @app.route('/admin', methods=['GET', 'POST'])
# # @role_required('admin')
# # def admin():
# #     if request.method == 'POST':
# #         try:
# #             date_str = request.form['date']
# #             food = request.form['food']
# #             weight = float(request.form['weight'])
# #             health_status = request.form['health_status']
# #             details = request.form['details']
# #             animal_id = int(request.form['animal_id'])

# #             record_date = date.fromisoformat(date_str)

# #             # Créez et ajoutez le nouvel enregistrement dans la base de données
# #             new_record = VetRecord(
# #                 date=record_date, food=food, weight=weight,
# #                 health_status=health_status, details=details,
# #                 animal_id=animal_id
# #             )

# #             db.session.add(new_record)
# #             db.session.commit()

# #             # Lire le fichier JSON, ajouter le nouvel enregistrement, puis réécrire le fichier
# #             try:
# #                 with open('vet_records.json', 'r') as f:
# #                     vet_records = json.load(f)
# #             except (FileNotFoundError, json.JSONDecodeError):
# #                 vet_records = []

# #             vet_records.append({
# #                 'date': date_str,
# #                 'food': food,
# #                 'weight': weight,
# #                 'health_status': health_status,
# #                 'details': details,
# #                 'animal_id': animal_id
# #             })

# #             with open('vet_records.json', 'w') as f:
# #                 json.dump(vet_records, f, indent=4)

# #             flash('Fiche vétérinaire ajoutée avec succès!', 'success')

# #         except Exception as e:
# #             db.session.rollback()
# #             flash(f"Erreur lors de l'ajout de la fiche: {str(e)}", 'danger')

# #     # Récupérer les valeurs des filtres depuis le formulaire
# #     filter_date = request.args.get('date')
# #     filter_animal_id = request.args.get('animal_id')

# #     # Commencer par une requête qui ne filtre rien
# #     query = VetRecord.query

# #     # Appliquer un filtre par date si une date est spécifiée
# #     if filter_date:
# #         query = query.filter(VetRecord.date == date.fromisoformat(filter_date))

# #     # Appliquer un filtre par animal_id si un animal est spécifié
# #     if filter_animal_id:
# #         query = query.filter(VetRecord.animal_id == filter_animal_id)

# #     animals = Animal.query.all()
# #     vet_records = query.all()
# #     habitats = Habitat.query.all()  # Ajoutez cette ligne pour récupérer les habitats
    
# #     consultation_counts = {animal.id: 0 for animal in animals}
# #     for record in vet_records:
# #         consultation_counts[record.animal_id] += record.consultation_count  # Utilise la valeur actuelle de consultation_count

# #     avis_a_valider = Avis.query.filter_by(approuve=False).all()

# #     return render_template('admin.html', avis_a_valider=avis_a_valider, animals=animals, vet_records=vet_records, habitats=habitats, consultation_counts=consultation_counts)

# # @app.route('/employee')
# # @role_required('employee')
# # def employee_page():
# #     # Code pour la page employé
# #     return render_template('employee.html')

# # @app.route('/veterinarian')
# # @role_required('veterinarian')
# # def veterinarian_page():
# #     # Code pour la page vétérinaire
# #     return render_template('veterinarian.html')

# # import commands

# # if __name__ == '__main__':
# #     with app.app_context():
# #         db.create_all()  # Crée la base de données si elle n'existe pas
# #     app.run(debug=True)

# # # from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
# # # from functools import wraps
# # # from flask_sqlalchemy import SQLAlchemy
# # # from datetime import date
# # # import json

# # # app = Flask(__name__)

# # # # Configuration de la base de données SQLite
# # # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zoo.db'
# # # app.config['SECRET_KEY'] = 'your_secret_key'
# # # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # # # Initialisation de l'extension SQLAlchemy
# # # db = SQLAlchemy(app)

# # # # Modèles (ajustés pour éviter la duplication)
# # # class User(db.Model):
# # #     id = db.Column(db.Integer, primary_key=True)
# # #     username = db.Column(db.String(120), unique=True, nullable=False)
# # #     password = db.Column(db.String(120), nullable=False)
# # #     role = db.Column(db.String(20), nullable=False)  # 'admin', 'employee', 'veterinarian'

# # # class Habitat(db.Model):
# # #     id = db.Column(db.Integer, primary_key=True)
# # #     name = db.Column(db.String(100), nullable=False)
# # #     description = db.Column(db.Text)
# # #     image = db.Column(db.String(200))
# # #     animals = db.relationship('Animal', backref='habitat', lazy=True)
# # #     # Pour le compteur de consultations
# # #     # consultation_count = db.Column(db.Integer, default=0)

# # # class Animal(db.Model):
# # #     id = db.Column(db.Integer, primary_key=True)
# # #     name = db.Column(db.String(100), nullable=False)
# # #     species = db.Column(db.String(100), nullable=False)
# # #     image = db.Column(db.String(200))
# # #     habitat_id = db.Column(db.Integer, db.ForeignKey('habitat.id'), nullable=False)
# # #     vet_records = db.relationship('VetRecord', back_populates='animal', lazy=True)
# # #     # consultation_count = db.Column(db.Integer, default=0)  # Nouvelle colonne pour le compteur de consultations

# # # class VetRecord(db.Model):
# # #     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
# # #     date = db.Column(db.Date, nullable=False)
# # #     food = db.Column(db.String(100), nullable=False)
# # #     weight = db.Column(db.Float, nullable=False)
# # #     health_status = db.Column(db.String(200), nullable=False)
# # #     details = db.Column(db.Text, nullable=True)
# # #     animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
# # #     animal = db.relationship('Animal', back_populates='vet_records')
# # #     consultation_count = db.Column(db.Integer, default=0)  # Nouveau champ pour le compteur de consultations

# # # # class Review(db.Model):
# # # #     id = db.Column(db.Integer, primary_key=True)
# # # #     visitor_name = db.Column(db.String(100), nullable=False)
# # # #     content = db.Column(db.Text, nullable=False)
# # # #     approved = db.Column(db.Boolean, default=False)  # Non approuvé par défaut

# # # class Avis(db.Model):
# # #     id = db.Column(db.Integer, primary_key=True)
# # #     nom = db.Column(db.String(100), nullable=False)
# # #     pseudo = db.Column(db.String(100), nullable=False)
# # #     titre = db.Column(db.String(100), nullable=False)
# # #     message = db.Column(db.Text, nullable=False)
# # #     approuve = db.Column(db.Boolean, default=False)

# # # @app.route('/submit_review', methods=['POST'])
# # # def submit_review():
# # #     nom = request.form['nom']
# # #     pseudo = request.form['pseudo']
# # #     titre = request.form['title']
# # #     message = request.form['message']
    
# # #     nouvel_avis = Avis(nom=nom, pseudo=pseudo, titre=titre, message=message)
# # #     db.session.add(nouvel_avis)
# # #     db.session.commit()
    
# # #     flash('Votre avis a été soumis et est en attente de validation.')
# # #     return redirect(url_for('home'))

# # # # @app.route('/admin')
# # # # def admin():
# # # #     avis_a_valider = Avis.query.filter_by(approuve=False).all()
# # # #     return render_template('admin.html', avis_a_valider=avis_a_valider)

# # # @app.route('/approve_review/<int:avis_id>')
# # # def approve_review(avis_id):
# # #     avis = Avis.query.get_or_404(avis_id)
# # #     avis.approuve = True
# # #     db.session.commit()
# # #     flash('Avis approuvé.')
# # #     return redirect(url_for('admin'))

# # # @app.route('/disapprove_review/<int:avis_id>')
# # # def disapprove_review(avis_id):
# # #     avis = Avis.query.get_or_404(avis_id)
# # #     db.session.delete(avis)
# # #     db.session.commit()
# # #     flash('Avis supprimé.')
# # #     return redirect(url_for('admin'))

# # # # Routes pour les différentes pages

# # # @app.route('/')
# # # def home():
# # #     # Récupérer les avis validés (approuvés)
# # #     avis_valides = Avis.query.filter_by(approuve=True).all()
# # #     return render_template('index.html', avis_valides=avis_valides)


# # # @app.route('/login')
# # # def login():
# # #     return render_template('login.html')

# # # @app.route('/register')
# # # def register():
# # #     return render_template('register.html')

# # # @app.route('/contact')
# # # def contact():
# # #     return render_template('contact.html')

# # # @app.route('/services')
# # # def services():
# # #     return render_template('services.html')

# # # @app.route('/habitats')
# # # def habitats():
# # #     habitats = Habitat.query.all()
# # #     return render_template('habitats.html', habitats=habitats)

# # # @app.route('/habitat/<int:habitat_id>')
# # # def habitat(habitat_id):
# # #     habitat = Habitat.query.get_or_404(habitat_id)
    
# # #     # Incrémenter le compteur de consultations
# # #     # habitat.consultation_count += 1
# # #     db.session.commit()
    
# # #     animals = Animal.query.filter_by(habitat_id=habitat_id).all()

# # #     # Récupère le dernier enregistrement vétérinaire pour chaque animal de l'habitat
# # #     last_vet_records_by_animal = {}
# # #     for animal in animals:
# # #         # Trier les enregistrements vétérinaires par date en ordre décroissant et prendre le premier
# # #         last_vet_record = VetRecord.query.filter_by(animal_id=animal.id).order_by(VetRecord.date.desc()).first()
# # #         last_vet_records_by_animal[animal.id] = last_vet_record
# # #         print(f"Animal ID: {animal.id}, Consultation Count: {last_vet_record.consultation_count if last_vet_record else 'No records'}")  # Ajoute ceci pour déboguer

# # #     # Générez le nom du template basé sur l'habitat_id
# # #     template_name = f'habitat{habitat_id}.html'

# # #     # Rendre le template correspondant avec les données nécessaires
# # #     return render_template(template_name, habitat=habitat, animals=animals, vet_records_by_animal=last_vet_records_by_animal)

# # # @app.route('/increment-consultation/<int:animal_id_here>', methods=['POST'])
# # # def increment_consultation(animal_id_here):
# # #     # vet_record = VetRecord.query.get_or_404(record_id)  # Récupère l'enregistrement vétérinaire par ID
# # #     # animal_id = VetRecord.query.get_or_404(record_id).animal_id
# # #     animal_in_question = Animal.query.get_or_404(animal_id_here)  # Récupère l'enregistrement vétérinaire par ID
    
# # #     animals = Animal.query.filter_by(habitat_id=animal_in_question.habitat_id).all()

# # #     # Récupère le dernier enregistrement vétérinaire pour chaque animal de l'habitat
# # #     last_vet_records_by_animal = {}
# # #     for animal in animals:
# # #         # Trier les enregistrements vétérinaires par date en ordre décroissant et prendre le premier
# # #         last_vet_record = VetRecord.query.filter_by(animal_id=animal.id).order_by(VetRecord.date.desc()).first()
# # #         last_vet_records_by_animal[animal.id] = last_vet_record
# # #     #print(f"TEST : {record_id}, {vet_record.animal_id}")
# # #     last_vet_record = last_vet_records_by_animal.get(animal_id_here)

# # #     if last_vet_record:
# # #         print(f"TEST animal id: {animal_id_here}, vet record id : {last_vet_record.id}")
# # #     else:
# # #         print(f"TEST animal id: {animal_id_here}, no vet records found")

# # #     #print(f"TEST animal id: {animal_id_here}, vet record id : {animal_in_question.vet_records[last_vet_record.id]}")
# # #     #print(f"Before Increment - VetRecord ID: {vet_record.id}, Animal ID: {vet_record.animal_id}, Current Count: {vet_record.consultation_count}")
# # #     last_vet_record.consultation_count += 1  # Incrémente le compteur de consultations


# # #     db.session.commit()  # Enregistre les modifications dans la base de données
# # #     # print(f"After Increment - Animal ID: {vet_record.animal_id}, VetRecord ID: {vet_record.id}, New Count: {vet_record.consultation_count}")
# # #     #print(f"After Increment - VetRecord ID: {vet_record.id}, Animal ID: {vet_record.animal_id}, New Count: {vet_record.consultation_count}")
# # #     return redirect(request.referrer)  # Redirige vers la page précédente
# # #     # return '', 204  # Réponse vide avec statut HTTP 204 No Content

# # # @app.route('/admin', methods=['GET', 'POST'])
# # # def admin():
# # #     if request.method == 'POST':
# # #         try:
# # #             date_str = request.form['date']
# # #             food = request.form['food']
# # #             weight = float(request.form['weight'])
# # #             health_status = request.form['health_status']
# # #             details = request.form['details']
# # #             animal_id = int(request.form['animal_id'])

# # #             record_date = date.fromisoformat(date_str)

# # #             # Créez et ajoutez le nouvel enregistrement dans la base de données
# # #             new_record = VetRecord(
# # #                 date=record_date, food=food, weight=weight,
# # #                 health_status=health_status, details=details,
# # #                 animal_id=animal_id
# # #             )

# # #             db.session.add(new_record)
# # #             db.session.commit()

# # #             # Lire le fichier JSON, ajouter le nouvel enregistrement, puis réécrire le fichier
# # #             try:
# # #                 with open('vet_records.json', 'r') as f:
# # #                     vet_records = json.load(f)
# # #             except (FileNotFoundError, json.JSONDecodeError):
# # #                 vet_records = []

# # #             vet_records.append({
# # #                 'date': date_str,
# # #                 'food': food,
# # #                 'weight': weight,
# # #                 'health_status': health_status,
# # #                 'details': details,
# # #                 'animal_id': animal_id
# # #             })

# # #             with open('vet_records.json', 'w') as f:
# # #                 json.dump(vet_records, f, indent=4)

# # #             flash('Fiche vétérinaire ajoutée avec succès!', 'success')

# # #         except Exception as e:
# # #             db.session.rollback()
# # #             flash(f"Erreur lors de l'ajout de la fiche: {str(e)}", 'danger')

# # #     # Récupérer les valeurs des filtres depuis le formulaire
# # #     filter_date = request.args.get('date')
# # #     filter_animal_id = request.args.get('animal_id')

# # #     # Commencer par une requête qui ne filtre rien
# # #     query = VetRecord.query

# # #     # Appliquer un filtre par date si une date est spécifiée
# # #     if filter_date:
# # #         query = query.filter(VetRecord.date == date.fromisoformat(filter_date))

# # #     # Appliquer un filtre par animal_id si un animal est spécifié
# # #     if filter_animal_id:
# # #         query = query.filter(VetRecord.animal_id == filter_animal_id)

# # #     animals = Animal.query.all()
# # #     vet_records = query.all()
# # #     habitats = Habitat.query.all()  # Ajoutez cette ligne pour récupérer les habitats
    
# # #     consultation_counts = {animal.id: 0 for animal in animals}
# # #     for record in vet_records:
# # #         consultation_counts[record.animal_id] += record.consultation_count  # Utilise la valeur actuelle de consultation_count

# # #     avis_a_valider = Avis.query.filter_by(approuve=False).all()

# # #     return render_template('admin.html', avis_a_valider=avis_a_valider, animals=animals, vet_records=vet_records, habitats=habitats, consultation_counts=consultation_counts)

# # # import commands

# # # if __name__ == '__main__':
# # #     with app.app_context():
# # #         db.create_all()  # Crée la base de données si elle n'existe pas
# # #     app.run(debug=True)