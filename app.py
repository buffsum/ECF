from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
from functools import wraps
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from wtforms import StringField, TextAreaField, SubmitField, MultipleFileField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import os
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import date
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

# Configuration de Flask-Mail
# app.config['MAIL_SERVER'] = 'smtp.example.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'laurane-c@hotmail.fr'
# app.config['MAIL_PASSWORD'] = 'laurane-c@hotmail.fr'
# app.config['MAIL_DEFAULT_SENDER'] = 'laurane-c@hotmail.fr'

# mail = Mail(app)

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modèles
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)

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
    description = db.Column(db.Text, nullable=True)

class VetRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    health_status = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text, nullable=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    animal = db.relationship('Animal', back_populates='vet_records')
    consultation_count = db.Column(db.Integer, default=0)

class Avis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    pseudo = db.Column(db.String(100), nullable=False)
    titre = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    approuve = db.Column(db.Boolean, default=False)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    images_url = db.Column(db.PickleType, nullable=True)

    def __init__(self, title, description, images_url=None):
        self.title = title
        self.description = description
        self.images_url = images_url if images_url is not None else []

class ServiceForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    images = MultipleFileField('Images')
    submit = SubmitField('Submit')

class AnimalForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    species = StringField('Species', validators=[DataRequired()])
    images = MultipleFileField('Images')
    description = TextAreaField('Description')
    submit = SubmitField('Submit')

class DailyFoodRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    food = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    animal = db.relationship('Animal', backref=db.backref('daily_food_records', lazy=True))

class CreateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    role = SelectField('Rôle', choices=[('employee', 'Employé'), ('veterinarian', 'Vétérinaire')], validators=[DataRequired()])
    submit = SubmitField('Créer un compte')

def role_required(role):
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

@app.route('/submit_review', methods=['POST'])
def submit_review():
    nom = request.form['nom']
    pseudo = request.form['pseudo']
    titre = request.form['title']
    message = request.form['message']
    
    nouvel_avis = Avis(nom=nom, pseudo=pseudo, titre=titre, message=message)
    db.session.add(nouvel_avis)
    db.session.commit()
    
    save_avis_to_json()
    
    flash('Votre avis a été soumis et est en attente de validation.')
    return redirect(url_for('home'))

@app.route('/approve_review/<int:avis_id>')
def approve_review(avis_id):
    avis = Avis.query.get_or_404(avis_id)
    avis.approuve = True
    db.session.commit()
    save_avis_to_json()
    flash('Avis approuvé.')
    return redirect(url_for('admin'))

@app.route('/disapprove_review/<int:avis_id>')
def disapprove_review(avis_id):
    avis = Avis.query.get_or_404(avis_id)
    db.session.delete(avis)
    db.session.commit()
    flash('Avis supprimé.')
    return redirect(url_for('admin'))

@app.route('/delete_review/<int:avis_id>', methods=['POST'])
def delete_review(avis_id):
    avis = Avis.query.get_or_404(avis_id)
    db.session.delete(avis)
    db.session.commit()
    save_avis_to_json()
    flash('Avis supprimé.')
    return redirect(url_for('home'))

@app.route('/')
def home():
    avis_valides = Avis.query.filter_by(approuve=True).all()
    return render_template('index.html', avis_valides=avis_valides)

@app.route('/login', methods=['GET', 'POST'])
def login():
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
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'danger')
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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        objet = request.form['objet']
        message = request.form['message']

        msg = Message(subject=objet,
                      sender=email,
                      recipients=['laurane-cl@hotmail.fr'],
                      body=f"Nom: {nom}\nEmail: {email}\n\nMessage:\n{message}")
        mail.send(msg)
        flash('Votre message a été envoyé avec succès!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/services')
def services():
    services = Service.query.all()
    return render_template('services.html', services=services)

@app.route('/service/new', methods=['GET', 'POST'])
def new_service():
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('login'))
    
    form = ServiceForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        images = form.images.data
        image_filenames = []
        for image in images:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_filenames.append(filename)
        
        new_service = Service(title=title, description=description, images_url=image_filenames)
        db.session.add(new_service)
        db.session.commit()
        
        flash('Service ajouté avec succès!', 'success')
        return redirect(url_for('services'))
    return render_template('service_form.html', form=form)

@app.route('/service/<int:service_id>/edit', methods=['GET', 'POST'])
def edit_service(service_id):
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('login'))
    service = Service.query.get_or_404(service_id)
    form = ServiceForm()
    if form.validate_on_submit():
        service.title = form.title.data
        service.description = form.description.data
        db.session.commit()
        flash('Service modifié avec succès!', 'success')
        return redirect(url_for('services'))
    elif request.method == 'GET':
        form.title.data = service.title
        form.description.data = service.description
    return render_template('service_form.html', form=form)

@app.route('/service/<int:service_id>/delete', methods=['POST'])
def delete_service(service_id):
    if 'user_role' not in session or session['user_role'] != 'admin':
        return redirect(url_for('login'))
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash('Service supprimé avec succès!', 'success')
    return redirect(url_for('services'))

@app.route('/habitats')
def habitats():
    habitats = Habitat.query.all()
    return render_template('habitats.html', habitats=habitats)

@app.route('/habitat/<int:habitat_id>')
def habitat(habitat_id):
    habitat = Habitat.query.get_or_404(habitat_id)
    animals = Animal.query.filter_by(habitat_id=habitat_id).all()
    last_vet_records_by_animal = {}
    for animal in animals:
        last_vet_record = VetRecord.query.filter_by(animal_id=animal.id).order_by(VetRecord.date.desc()).first()
        last_vet_records_by_animal[animal.id] = last_vet_record
    template_name = f'habitat{habitat_id}.html'
    return render_template(template_name, habitat=habitat, animals=animals, vet_records_by_animal=last_vet_records_by_animal)

# @app.route('/animal/new/<int:habitat_id>', methods=['GET', 'POST'])
# @role_required('admin')
# def add_animal(habitat_id):
#     form = AnimalForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         species = form.species.data
#         images = form.images.data
#         image_filenames = []
#         for image in images:
#             filename = secure_filename(image.filename)
#             image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             image_filenames.append(filename)
#         description = form.description.data
#         new_animal = Animal(name=name, species=species, image=image, description=description, habitat_id=habitat_id)
#         db.session.add(new_animal)
#         db.session.commit()
#         flash('Animal ajouté avec succès!', 'success')
#         return redirect(url_for('habitat', habitat_id=habitat_id))
#     return render_template('animal_form.html', form=form)
@app.route('/animal/new/<int:habitat_id>', methods=['GET', 'POST'])
@role_required('admin')
def add_animal(habitat_id):
    form = AnimalForm()
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        images = form.images.data
        image_filenames = []
        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filenames.append(filename)
        description = form.description.data
        new_animal = Animal(name=name, species=species, image=','.join(image_filenames), description=description, habitat_id=habitat_id)
        db.session.add(new_animal)
        db.session.commit()
        flash('Animal ajouté avec succès!', 'success')
        return redirect(url_for('habitat', habitat_id=habitat_id))
    return render_template('animal_form.html', form=form, habitat=habitat)

# @app.route('/animal/<int:animal_id>/edit', methods=['GET', 'POST'])
# @role_required('admin')
# def edit_animal(animal_id):
#     animal = Animal.query.get_or_404(animal_id)
#     form = AnimalForm()
#     if form.validate_on_submit():
#         animal.name = form.name.data
#         animal.species = form.species.data
#         animal.image = form.images.data
#         animal.description = form.description.data
#         db.session.commit()
#         flash('Animal modifié avec succès!', 'success')
#         return redirect(url_for('habitat', habitat_id=animal.habitat_id))
#     elif request.method == 'GET':
#         form.name.data = animal.name
#         form.species.data = animal.species
#         form.images.data = animal.image
#         form.description.data = animal.description
#     return render_template('animal_form.html', form=form)

@app.route('/animal/<int:animal_id>/edit', methods=['GET', 'POST'])
@role_required('admin')
def edit_animal(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    form = AnimalForm()
    if form.validate_on_submit():
        animal.name = form.name.data
        animal.species = form.species.data
        images = form.images.data
        image_filenames = []
        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filenames.append(filename)
        if image_filenames:
            animal.image = ','.join(image_filenames)
        animal.description = form.description.data
        db.session.commit()
        flash('Animal modifié avec succès!', 'success')
        return redirect(url_for('habitat', habitat_id=animal.habitat_id))
    elif request.method == 'GET':
        form.name.data = animal.name
        form.species.data = animal.species
        form.description.data = animal.description
    return render_template('animal_form.html', form=form)

@app.route('/animal/<int:animal_id>/delete', methods=['POST'])
@role_required('admin')
def delete_animal(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    VetRecord.query.filter_by(animal_id=animal_id).delete()
    # habitat_id = animal.habitat_id
    db.session.delete(animal)
    db.session.commit()
    flash('Animal supprimé avec succès!', 'success')
    return redirect(url_for('habitat', habitat_id=animal.habitat_id))

@app.route('/increment-consultation/<int:animal_id_here>', methods=['POST'])
def increment_consultation(animal_id_here):
    animal_in_question = Animal.query.get_or_404(animal_id_here)
    last_vet_record = VetRecord.query.filter_by(animal_id=animal_in_question.id).order_by(VetRecord.date.desc()).first()
    if last_vet_record:
        last_vet_record.consultation_count += 1
    db.session.commit()
    return redirect(request.referrer)

@app.route('/admin', methods=['GET', 'POST'])
@role_required('admin')
def admin():
    form = CreateUserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        role = form.role.data

        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Un utilisateur avec cet email existe déjà.', 'danger')
            return redirect(url_for('admin'))

        # Créer un nouvel utilisateur
        new_user = User(
            username=email,
            email=email,
            password=generate_password_hash(password),
            role=role
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Le compte a été créé avec succès.', 'success')
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        try:
            date_str = request.form['date']
            health_status = request.form['health_status']
            details = request.form['details']
            animal_id = int(request.form['animal_id'])

            record_date = date.fromisoformat(date_str)

            new_record = VetRecord(
                date=record_date,
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

    filter_avis_date = request.args.get('date')
    filter_avis_animal_id = request.args.get('animal_id')

    query = VetRecord.query

    if filter_avis_date:
        query = query.filter(VetRecord.date == date.fromisoformat(filter_avis_date))

    if filter_avis_animal_id:
        query = query.filter(VetRecord.animal_id == filter_avis_animal_id)

    animals = Animal.query.all()
    vet_records = query.all()
    habitats = Habitat.query.all()
    
    consultation_counts = {animal.id: 0 for animal in animals}
    for record in vet_records:
        if record.animal_id in consultation_counts:
            consultation_counts[record.animal_id] += record.consultation_count
        else:
            consultation_counts[record.animal_id] = record.consultation_count

    avis_a_valider = Avis.query.filter_by(approuve=False).all()

    selected_animal_id = request.args.get('filter_animal_id')
    all_animals = Animal.query.all()
    
    if selected_animal_id and selected_animal_id != 'all':
        filtered_animals = Animal.query.filter_by(id=selected_animal_id).all()
    else:
        filtered_animals = all_animals if selected_animal_id == 'all' else []

    filter_food_date = request.args.get('food_date')
    filter_food_animal_id = request.args.get('food_animal_id')

    food_query = DailyFoodRecord.query

    if filter_food_date:
        food_query = food_query.filter(DailyFoodRecord.date == date.fromisoformat(filter_food_date))

    if filter_food_animal_id:
        food_query = food_query.filter(DailyFoodRecord.animal_id == filter_food_animal_id)

    daily_food_records = food_query.all()

    return render_template('admin.html', form=form, avis_a_valider=avis_a_valider, animals=animals, vet_records=vet_records, habitats=habitats, consultation_counts=consultation_counts, all_animals=all_animals, selected_animal_id=selected_animal_id, filtered_animals=filtered_animals, daily_food_records=daily_food_records, filter_avis_date=filter_avis_date, filter_avis_animal_id=filter_avis_animal_id, filter_food_date=filter_food_date, filter_food_animal_id=filter_food_animal_id)

@app.route('/employee', methods=['GET', 'POST'])
@role_required('employee')
def employee():
    if request.method == 'POST':
        try:
            date_str = request.form['date']
            food = request.form['food']
            weight = float(request.form['weight'])
            animal_id = int(request.form['animal_id'])

            record_date = date.fromisoformat(date_str)

            new_record = DailyFoodRecord(
                date=record_date, food=food, weight=weight, animal_id=animal_id
            )

            db.session.add(new_record)
            db.session.commit()

            flash('Fiche d\'alimentation ajoutée avec succès!', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'ajout de la fiche: {str(e)}", 'danger')

    animals = Animal.query.all()
    return render_template('employee.html', animals=animals)

@app.route('/veterinarian')
@role_required('veterinarian')
def veterinarian():
    return render_template('veterinarian.html')

# @app.route('/admin/create_user', methods=['GET', 'POST'])
# def create_user():
#     form = CreateUserForm()
#     if form.validate_on_submit():
#         email = form.email.data
#         password = form.password.data
#         role = form.role.data

#         # Vérifier si l'utilisateur existe déjà
#         existing_user = User.query.filter_by(email=email).first()
#         if existing_user:
#             flash('Un utilisateur avec cet email existe déjà.', 'danger')
#             return redirect(url_for('create_user'))

#         # Créer un nouvel utilisateur
#         new_user = User(
#             username=email,
#             email=email,
#             password=generate_password_hash(password),
#             role=role
#         )
#         db.session.add(new_user)
#         db.session.commit()
#         # Envoyer un email de notification avec une adresse d'expéditeur dynamique
#         # msg = Message(
#         #     'Votre compte a été créé',
#         #     recipients=[email],
#         #     sender='fake-email@example.com'  # Adresse d'expéditeur dynamique
#         # )
#         # msg.body = f"Bonjour,\n\nVotre compte a été créé avec succès. Votre nom d'utilisateur est {email}.\n\nMerci."
#         # mail.send(msg)

#         # Envoyer un email de notification
#         # msg = Message('Votre compte a été créé', recipients=[email])
#         # msg.body = f"Bonjour,\n\nVotre compte a été créé avec succès. Votre nom d'utilisateur est {email}.\n\nMerci."
#         # mail.send(msg)

#         flash('Le compte a été créé avec succès et un email a été envoyé à l\'utilisateur.', 'success')
#         return redirect(url_for('admin_dashboard'))

#     return render_template('create_user.html', form=form)

import commands

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#         app.cli.invoke(app.cli.commands['load-avis'])  # Charger les avis depuis le fichier JSON
#     app.run(debug=True)