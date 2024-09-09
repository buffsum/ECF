# Importation des modules Flask et des utilitaires
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session  # Flask et ses utilitaires pour la gestion des requêtes et des sessions
from functools import wraps  # Pour créer des décorateurs
from flask_wtf import FlaskForm  # Pour la gestion des formulaires avec Flask-WTF

# Importation des formulaires personnalisés
from forms import ServiceForm, AnimalForm, CreateUserForm

# Importation de Flask-Migrate pour la gestion des migrations de base de données
from flask_migrate import Migrate

# Importation des champs et des validateurs de WTForms
from wtforms import StringField, TextAreaField, SubmitField, MultipleFileField, PasswordField, SelectField  # Champs de formulaire
from wtforms.validators import DataRequired, Email  # Validateurs pour les champs de formulaire

# Importation des utilitaires de werkzeug pour la gestion des fichiers
from werkzeug.utils import secure_filename  # Pour sécuriser les noms de fichiers téléchargés

# Importation de Flask-Mail pour la gestion des emails
from flask_mail import Mail, Message  # Pour l'envoi d'emails

# Importation des modèles de base de données
from models import db, User, Habitat, Animal, VetRecord, Avis, Service, DailyFoodRecord  # Modèles de base de données

# Importation des fonctions utilitaires depuis commands.py
from commands import save_avis_to_json, load_avis_from_json, load_services_from_json, load_animals_from_json, save_animal_to_json, load_users_from_json, save_user_to_json, save_daily_food_to_json  # Fonctions utilitaires pour la gestion des données

# Importation des modules standard
import os  # Pour la gestion des chemins de fichiers et des opérations système
from werkzeug.security import check_password_hash, generate_password_hash  # Pour la gestion des mots de passe
from flask_sqlalchemy import SQLAlchemy  # Pour la gestion de la base de données avec SQLAlchemy
from datetime import date  # Pour la gestion des dates
import json  # Pour la gestion des fichiers JSON

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration des dossiers de téléchargement
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Fonction pour vérifier si le fichier a une extension autorisée
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zoo.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'laurane-c@hotmail.fr'
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_DEFAULT_SENDER'] = 'laurane-c@hotmail.fr'
mail = Mail(app)

# Initialiser l'instance de SQLAlchemy avec l'application
db.init_app(app)

# Créer toutes les tables si elles n'existent pas déjà
with app.app_context():
    db.create_all()

# Importer et enregistrer les commandes CLI
import commands
commands.register_commands(app)

# Définition d'un décorateur pour vérifier le rôle de l'utilisateur
def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session or session.get('user_role') not in roles:
                flash("Vous n'avez pas la permission d'accéder à cette page.", "danger")
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

# **** Gestion des routes pour les visiteurs ****
@app.route('/')
def home():
    avis_valides = Avis.query.filter_by(approuve=True).all()
    return render_template('index.html', avis_valides=avis_valides)

# **** Gestion des routes pour les User ****
# **** Gestion des routes pour ADMIN ****
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

        # Sauvegarder l'utilisateur dans le fichier JSON
        user_data = {
            'username': email,
            'email': email,
            'password': generate_password_hash(password),
            'role': role
        }
        save_user_to_json(user_data)
        # Envoyer un email de notification avec une adresse d'expéditeur dynamique
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

        flash('Le compte a été créé avec succès.', 'success')
        return redirect(url_for('admin'))

    # Filtrer les avis vétérinaires
    filter_avis_date = request.args.get('date')
    filter_avis_animal_id = request.args.get('animal_id')
    query = VetRecord.query

    # Appliquer les filtre avis vétérinaire
    if filter_avis_animal_id and filter_avis_animal_id != '':
        query = query.filter(VetRecord.animal_id == filter_avis_animal_id)
    if filter_avis_date and filter_avis_date != '':
        query = query.filter(VetRecord.date == date.fromisoformat(filter_avis_date))
    if filter_avis_animal_id and filter_avis_animal_id != '' and filter_avis_date and filter_avis_date != '':
        query = query.filter(VetRecord.animal_id == filter_avis_animal_id)

    animals = Animal.query.all()
    vet_records = query.all()
    habitats = Habitat.query.all()
    
    # Compter le nombre de consultations pour chaque animal
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

    # Appliquer les filtres pour les enregistrements alimentaires
    if filter_avis_animal_id and filter_avis_animal_id != '':
        query = query.filter(VetRecord.animal_id == filter_avis_animal_id)
    if filter_avis_date and filter_avis_date != '':
        query = query.filter(VetRecord.date == date.fromisoformat(filter_avis_date))
    if filter_avis_animal_id and filter_avis_animal_id != '' and filter_avis_date and filter_avis_date != '':
        query = query.filter(VetRecord.animal_id == filter_avis_animal_id)

    daily_food_records = food_query.all()

    return render_template('admin.html', form=form, avis_a_valider=avis_a_valider, animals=animals, vet_records=vet_records, habitats=habitats, consultation_counts=consultation_counts, all_animals=all_animals, selected_animal_id=selected_animal_id, filtered_animals=filtered_animals, daily_food_records=daily_food_records, filter_avis_date=filter_avis_date, filter_avis_animal_id=filter_avis_animal_id, filter_food_date=filter_food_date, filter_food_animal_id=filter_food_animal_id)

# Route pour modifier les informations pratiques
@app.route('/edit_info_pratique', methods=['GET', 'POST'])
@role_required('admin')
def edit_info_pratique():
    if request.method == 'POST':
        # Logique pour mettre à jour les informations pratiques
        new_info = request.form['info']
        # Mettez à jour les informations dans la base de données ou le fichier
        flash('Informations pratiques mises à jour avec succès.', 'success')
        return redirect(url_for('home'))
    
    # Récupérez les informations actuelles pour les afficher dans le formulaire
    current_info = "Retrouvez nous tous les jours de 10h à 20h au 1 place du roi Saint-Judicaël 35380 Paimpont Bretagne"
    return render_template('edit_info_pratique.html', current_info=current_info)

# Route pour afficher les avis vétérinaires ?
@app.route('/admin/vet_records', methods=['GET'])
@role_required('admin')
def view_vet_records_admin():
    filter_avis_date = request.args.get('date')
    filter_avis_animal_id = request.args.get('animal_id')

    query = VetRecord.query

    if filter_avis_date:
        query = query.filter(VetRecord.date == date.fromisoformat(filter_avis_date))

    if filter_avis_animal_id:
        query = query.filter(VetRecord.animal_id == filter_avis_animal_id)

    vet_records = query.all()
    animals = Animal.query.all()

    return render_template('admin_vet_records.html', vet_records=vet_records, animals=animals, filter_avis_date=filter_avis_date, filter_avis_animal_id=filter_avis_animal_id)

# **** Fin de la gestion des routes pour ADMIN ****

# **** Gestion des routes pour EMPLOYEE ****
# Route pour ajouter une fiche d'alimentation et afficher les avis à valider
@app.route('/employee', methods=['GET', 'POST'])
@role_required('employee')
def employee():
    if request.method == 'POST':
        try:
            date_str = request.form['date']
            food = request.form['food']
            weight = float(request.form['weight'])
            animal_id = int(request.form['animal_id'])

            new_record = DailyFoodRecord(
                date=date.fromisoformat(date_str),
                food=food,
                weight=weight,
                animal_id=animal_id
            )

            db.session.add(new_record)
            db.session.commit()

            # Sauvegarder les enregistrements dans le fichier dailyfood.json
            save_daily_food_to_json()

            flash('Fiche d\'alimentation ajoutée avec succès!', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'ajout de la fiche: {str(e)}", 'danger')

    animals = Animal.query.all()
    avis_a_valider = Avis.query.filter_by(approuve=False).all()
    return render_template('employee.html', animals=animals, avis_a_valider=avis_a_valider)

# Route pour approuver un avis
@app.route('/employee/approve_review/<int:avis_id>')
@role_required('employee')
def approve_review(avis_id):
    avis = Avis.query.get_or_404(avis_id)
    avis.approuve = True
    db.session.commit()
    save_avis_to_json()
    flash('Avis approuvé.')
    return redirect(url_for('employee'))

# Route pour désapprouver un avis
@app.route('/employee/disapprove_review/<int:avis_id>')
@role_required('employee')
def disapprove_review(avis_id):
    avis = Avis.query.get_or_404(avis_id)
    db.session.delete(avis)
    db.session.commit()
    flash('Avis supprimé.')
    return redirect(url_for('employee'))

# Route pour supprimer un avis (après publication)
@app.route('/employee/delete_review/<int:avis_id>', methods=['POST'])
@role_required('employee')
def delete_review(avis_id):
    avis = Avis.query.get_or_404(avis_id)
    db.session.delete(avis)
    db.session.commit()
    save_avis_to_json()
    flash('Avis supprimé.')
    return redirect(url_for('home'))
# **** Fin de la gestion des routes pour EMPLOYEE ****

# **** Gestion des routes pour VETERINARIAN ****
# Route pour afficher les fiches vétérinaires
@app.route('/veterinarian', methods=['GET', 'POST'])
@role_required('veterinarian')
def veterinarian():
    vet_records = []
    daily_food_records = []
    filter_avis_date = None
    filter_avis_animal_id = None
    filter_food_date = None
    filter_food_animal_id = None

    if request.method == 'POST':
        try:
            animal_id = int(request.form['animal_id'])
            date_str = request.form['date']
            record_date = date.fromisoformat(date_str)

            # Filtrer les enregistrements vétérinaires
            vet_records = VetRecord.query.filter_by(animal_id=animal_id, date=record_date).all()

            if not vet_records:
                flash('Aucune fiche vétérinaire trouvée pour cet animal et cette date.', 'warning')
            else:
                flash('Fiches vétérinaires trouvées avec succès!', 'success')

            # Filtrer les enregistrements alimentaires
            daily_food_records = DailyFoodRecord.query.filter_by(animal_id=animal_id, date=record_date).all()

            if not daily_food_records:
                flash('Aucune fiche alimentaire trouvée pour cet animal et cette date.', 'warning')
            else:
                flash('Fiches alimentaires trouvées avec succès!', 'success')

        except Exception as e:
            flash(f"Erreur lors de la récupération des fiches: {str(e)}", 'danger')

    animals = Animal.query.all()
    return render_template('veterinarian.html', animals=animals, vet_records=vet_records, daily_food_records=daily_food_records, filter_avis_date=filter_avis_date, filter_avis_animal_id=filter_avis_animal_id, filter_food_date=filter_food_date, filter_food_animal_id=filter_food_animal_id)

# Route pour ajouter une fiche vétérinaire
@app.route('/veterinarian/add', methods=['POST'])
@role_required('veterinarian')
def add_vet_record():
    if request.method == 'POST':
        try:
            date_str = request.form['date']
            health_status = request.form['health_status']
            food = request.form['food']
            weight = request.form['weight']
            details = request.form['details']
            animal_id = int(request.form['animal_id'])

            record_date = date.fromisoformat(date_str)

            new_record = VetRecord(
                date=record_date,
                health_status=health_status,
                food=food,
                weight=weight,
                details=details,
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
                'food': food,
                'weight': weight,
                'details': details,
                'animal_id': animal_id
            })

            with open('vet_records.json', 'w') as f:
                json.dump(vet_records, f, indent=4)

            flash('Fiche vétérinaire ajoutée avec succès!', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'ajout de la fiche: {str(e)}", 'danger')

    return redirect(url_for('veterinarian'))

# Route pour afficher les fiches alimentaires
@app.route('/veterinarian/view', methods=['GET'])
@role_required('veterinarian')
def view_vet_records():
    filter_avis_date = request.args.get('date')
    filter_avis_animal_id = request.args.get('animal_id')

    query = VetRecord.query

    if filter_avis_date:
        query = query.filter(VetRecord.date == date.fromisoformat(filter_avis_date))

    if filter_avis_animal_id:
        query = query.filter(VetRecord.animal_id == filter_avis_animal_id)

    vet_records = query.all()
    animals = Animal.query.all()

    return render_template('veterinarian.html', vet_records=vet_records, animals=animals, filter_avis_date=filter_avis_date, filter_avis_animal_id=filter_avis_animal_id)

@app.route('/veterinarian/food_records', methods=['GET'])
@role_required('veterinarian')
def view_food_records():
    filter_food_date = request.args.get('food_date')
    filter_food_animal_id = request.args.get('food_animal_id')

    food_query = DailyFoodRecord.query

    if filter_food_date:
        food_query = food_query.filter(DailyFoodRecord.date == date.fromisoformat(filter_food_date))

    if filter_food_animal_id:
        food_query = food_query.filter(DailyFoodRecord.animal_id == filter_food_animal_id)

    daily_food_records = food_query.all()
    animals = Animal.query.all()

    return render_template('veterinarian.html', daily_food_records=daily_food_records, animals=animals, filter_food_date=filter_food_date, filter_food_animal_id=filter_food_animal_id)

# **** Fin de la gestion des routes pour VETERINARIAN ****

# **** Gestion des routes pour se login et logout ****
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
# **** Fin de la gestion des routes pour se login et logout ****

# **** Gestion des routes pour contact ****
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
# **** Fin de la gestion des routes pour contact ****

@app.route('/services')
def services():
    services = Service.query.all()
    for service in services:
        service.images_url = service.images_url.split(",") if service.images_url else []
    return render_template('services.html', services=services)

@app.route('/service/new', methods=['GET', 'POST'])
@role_required('admin', 'employee')
def new_service():
    form = ServiceForm()
    if form.validate_on_submit():
        images_urls = []
        for file in form.images_url.data:
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_url = 'uploads/' + filename
                images_urls.append(image_url)

        new_service = Service(
            title=form.title.data,
            description=form.description.data,
            images_url=images_urls  # Passer la liste directement
        )
        db.session.add(new_service)
        db.session.commit()
        flash('Service ajouté avec succès!', 'success')
        return redirect(url_for('services'))
    return render_template('service_form.html', form=form)

@app.route('/service/<int:service_id>/edit', methods=['GET', 'POST'])
@role_required('admin', 'employee')
def edit_service(service_id):
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
@role_required('admin', 'employee')
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash('Service supprimé avec succès!', 'success')
    return redirect(url_for('services'))

# **** Gestion des routes pour les animaux et les habitats ****
@app.route('/habitats')
def habitats():
    habitats = Habitat.query.all()
    return render_template('habitats.html', habitats=habitats)

# Route pour afficher les détails d'un habitat
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

# Route pour ajouter un animal
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
        
         # Sauvegarder l'animal dans le fichier JSON
        animal_data = {
            'name': name,
            'species': species,
            'image': ','.join(image_filenames),
            'description': description,
            'habitat_id': habitat_id
        }
        save_animal_to_json(animal_data)

        flash('Animal ajouté avec succès!', 'success')
        return redirect(url_for('habitat', habitat_id=habitat_id))
    return render_template('animal_form.html', form=form, habitat=habitat)

# Route pour modifier un animal
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

# Route pour supprimer un animal
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
# **** Fin de la gestion des routes pour les animaux et les habitats ****

# **** Gestion des routes pour les incrémentations des cliques sur fiches vétérinaires ****
@app.route('/increment-consultation/<int:animal_id_here>', methods=['POST'])
def increment_consultation(animal_id_here):
    animal_in_question = Animal.query.get_or_404(animal_id_here)
    last_vet_record = VetRecord.query.filter_by(animal_id=animal_in_question.id).order_by(VetRecord.date.desc()).first()
    if last_vet_record:
        last_vet_record.consultation_count += 1
    db.session.commit()
    return redirect(request.referrer)
# **** Fin de la gestion des routes pour les incrémentations des cliques sur fiches vétérinaires ****

# **** Route pour submit les avis
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
# **** Fin de la gestion des routes pour submit les avis ****

if __name__ == '__main__':
    app.run(debug=True)