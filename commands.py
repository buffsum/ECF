from flask import current_app
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from models import db, User, Habitat, Animal, VetRecord, Avis, Service, DailyFoodRecord
from datetime import date
import json
import click

@click.command('reset-db')
@with_appcontext
def reset_db():
    db.drop_all()
    db.create_all()
    print("Base de données réinitialisée avec succès.")

@click.command('add-data')
@with_appcontext
def add_data():
    # Assurez-vous que les habitats existent d'abord
    habitat1 = Habitat(name="Habitat 1 - Savane Africaine", description="Description de l'habitat 1", image="habitat1.jpg")
    habitat2 = Habitat(name="Habitat 2 - Forêt d'eucalyptus", description="Description de l'habitat 2", image="habitat2.jpg")
    habitat3 = Habitat(name="Habitat 3 - Forêt Tempérée", description="Description de l'habitat 3", image="habitat3.jpg")
    habitat4 = Habitat(name="Habitat 4 - Jungle Tropicale", description="Description de l'habitat 4", image="habitat4.jpg")

    db.session.add_all([habitat1, habitat2, habitat3, habitat4])
    db.session.commit()

    # Crée des instances d'animaux pour chaque habitat avec des IDs spécifiques
    animals = [
        Animal(id=1, name="Kibo", species="Zèbre", image="zebre1.jpg", habitat_id=1),
        Animal(id=2, name="Zara", species="Zèbre", image="zebre2.jpg", habitat_id=1),
        Animal(id=3, name="Luna", species="Gazelle", image="gazelle1.jpg", habitat_id=1),
        Animal(id=4, name="Tara", species="Gazelle", image="gazelle2.jpg", habitat_id=1),
        Animal(id=5, name="Mara", species="Girafe", image="girafe1.jpg", habitat_id=1),
        Animal(id=6, name="Jengo", species="Girafe", image="girafe2.jpg", habitat_id=1),
        Animal(id=7, name="Olga", species="Autruche", image="autruche1.jpg", habitat_id=1),
        Animal(id=8, name="Bibi", species="Autruche", image="autruche2.jpg", habitat_id=1),
        Animal(id=9, name="Rico", species="Autruche", image="autruche3.jpg", habitat_id=1),
        Animal(id=10, name="Togo", species="Phacochère", image="phacochere1.jpg", habitat_id=1),
        Animal(id=11, name="Eucalyptus", species="Koala", image="Koala1.jpg", habitat_id=2),
        Animal(id=12, name="Bamboo", species="Koala", image="Koala2.jpg", habitat_id=2),
        Animal(id=13, name="Walt", species="Kangourou", image="kangourou1.jpg", habitat_id=2),
        Animal(id=14, name="Riley", species="Kangourou", image="kangourou2.jpg", habitat_id=2),
        Animal(id=15, name="Pip", species="Possum", image="possum1.jpg", habitat_id=2),
        Animal(id=16, name="Cléo", species="Possum", image="possum2.jpg", habitat_id=2),
        Animal(id=17, name="Thorn", species="Échidné", image="echidne1.jpg", habitat_id=2),
        Animal(id=18, name="Moss", species="Échidné", image="echidne2.jpg", habitat_id=2),
        Animal(id=19, name="Tilly", species="Wallaby", image="wallaby1.jpg", habitat_id=2),
        Animal(id=20, name="Buddy", species="Wallaby", image="wallaby2.jpg", habitat_id=2),
        Animal(id=21, name="Grizz", species="Ours", image="ours1.jpg", habitat_id=3),
        Animal(id=22, name="Willow", species="Ours", image="ours2.jpg", habitat_id=3),
        Animal(id=23, name="Rusty", species="Cerf", image="cerf1.jpg", habitat_id=3),
        Animal(id=24, name="Bella", species="Biche", image="cerf2.jpg", habitat_id=3),
        Animal(id=25, name="Rocky", species="Raton laveur", image="raton1.jpg", habitat_id=3),
        Animal(id=26, name="Misty", species="Raton laveur", image="raton2.jpg", habitat_id=3),
        Animal(id=27, name="Chipper", species="Écureuil", image="ecureuil1.jpg", habitat_id=3),
        Animal(id=28, name="Nutmeg", species="Écureuil", image="ecureuil2.jpg", habitat_id=3),
        Animal(id=29, name="Ollie", species="Chouette rayée", image="chouette1.jpg", habitat_id=3),
        Animal(id=30, name="Hoot", species="Chouette rayée", image="chouette2.jpg", habitat_id=3),
        Animal(id=31, name="Milo", species="Capucin", image="capucin1.jpg", habitat_id=4),
        Animal(id=32, name="Maya", species="Capucin", image="capucin2.jpg", habitat_id=4),
        Animal(id=33, name="Coco", species="Paresseux", image="paresseux1.jpg", habitat_id=4),
        Animal(id=34, name="Gigi", species="Paresseux", image="paresseux2.jpg", habitat_id=4),
        Animal(id=35, name="Mango", species="Toucan", image="toucan1.jpg", habitat_id=4),
        Animal(id=36, name="Kiwi", species="Toucan", image="toucan2.jpg", habitat_id=4),
        Animal(id=37, name="Nina", species="Agouti", image="agouti1.jpg", habitat_id=4),
        Animal(id=38, name="Oscar", species="Agouti", image="agouti2.jpg", habitat_id=4),
        Animal(id=39, name="Vlad", species="Singes-araignée", image="singe-araignee1.jpg", habitat_id=4),
        Animal(id=40, name="Léo", species="Singes-araignée", image="singe-araignee2.jpg", habitat_id=4)
    ]

    db.session.add_all(animals)
    db.session.commit()

    # Ajoute des fiches vétérinaires pour les animaux
    vet_records = [
        VetRecord(date=date(2024, 1, 1), health_status="Bonne santé", details="Aucun problème détecté", animal_id=1),
        VetRecord(date=date(2024, 1, 10), health_status="Excellente santé", details="Contrôle de routine", animal_id=2),
        # Ajoutez d'autres fiches vétérinaires ici si nécessaire...
    ]

    db.session.add_all(vet_records)
    db.session.commit()

    # Créez un utilisateur admin avec un mot de passe haché
    admin = User(username='admin@admin.fr', email='admin@admin.fr', password=generate_password_hash('admin'), role='admin')
    db.session.add(admin)
    db.session.commit()

    print("Admin user created with username 'admin@admin.fr' and password 'admin'")

    # Ajoute des utilisateurs avec des rôles spécifiques
    users = [
        User(username="employee@company.com", email="employee@company.com", password=generate_password_hash("employee"), role="employee"),
        User(username="veterinarian@clinic.com", email="veterinarian@clinic.com", password=generate_password_hash("veterinarian"), role="veterinarian"),
        User(username="admin2@admin.fr", email="admin2@admin.fr", password=generate_password_hash("admin3"), role="admin")
    ]

    db.session.add_all(users)
    db.session.commit()

    print("Données ajoutées avec succès!")

def load_vet_records_from_json():
    try:
        with open('vet_records.json', 'r') as file:
            vet_records = json.load(file)
            return vet_records
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON: {e}")
        with open('vet_records.json', 'w') as file:
            json.dump([], file, indent=4)
        return []

def save_vet_record_to_json(vet_record):
    vet_records = load_vet_records_from_json()
    vet_records.append(vet_record)
    with open('vet_records.json', 'w') as file:
        json.dump(vet_records, file, indent=4)

def save_services_to_json(file_path='services.json'):
    services = Service.query.all()
    services_list = []
    for service in services:
        services_list.append({
            'title': service.title,
            'description': service.description,
            'images_url': service.images_url
        })
    with open(file_path, 'w') as file:
        json.dump(services_list, file, indent=4)
    print("Services sauvegardés dans le fichier JSON.")

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

def load_users_from_json():
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
            return users
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON: {e}")
        with open('users.json', 'w') as file:
            json.dump([], file, indent=4)
        return []

def save_user_to_json(user):
    users = load_users_from_json()
    users.append(user)
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

@click.command('load-users')
@with_appcontext
def load_users():
    users = load_users_from_json()
    for user in users:
        new_user = User(
            username=user['username'],
            email=user['email'],
            password=user['password'],
            role=user['role']
        )
        db.session.add(new_user)
    db.session.commit()
    print("Utilisateurs chargés depuis le fichier JSON.")

def load_animals_from_json():
    try:
        with open('animals.json', 'r') as file:
            animals = json.load(file)
            return animals
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON: {e}")
        with open('animals.json', 'w') as file:
            json.dump([], file, indent=4)
        return []

def save_animal_to_json(animal):
    animals = load_animals_from_json()
    animals.append(animal)
    with open('animals.json', 'w') as file:
        json.dump(animals, file, indent=4)

@click.command('load-animals')
@with_appcontext
def load_animals():
    animals = load_animals_from_json()
    for animal in animals:
        new_animal = Animal(
            name=animal['name'],
            species=animal['species'],
            image=animal['image'],
            habitat_id=animal['habitat_id']
        )
        db.session.add(new_animal)
    db.session.commit()
    print("Animaux chargés depuis le fichier JSON.")

@click.command('restore-data')
@with_appcontext
def restore_data():
    vet_records = load_vet_records_from_json()
    for record in vet_records:
        vet_record = VetRecord(
            date=date.fromisoformat(record['date']),
            health_status=record['health_status'],
            details=record['details'],
            animal_id=record['animal_id']
        )
        db.session.add(vet_record)
    db.session.commit()

    print("Données restaurées avec succès!")

@click.command('load-vet-records')
@with_appcontext
def load_vet_records():
    vet_records = load_vet_records_from_json()
    for record in vet_records:
        new_record = VetRecord(
            date=date.fromisoformat(record['date']),
            health_status=record['health_status'],
            details=record['details'],
            animal_id=record['animal_id']
        )
        db.session.add(new_record)
    db.session.commit()
    print("Fiches vétérinaires chargées depuis le fichier JSON.")

@click.command('load-avis')
@with_appcontext
def load_avis():
    try:
        with open('avis.json', 'r') as f:
            avis_data = json.load(f)
        for record in avis_data:
            new_avis = Avis(
                nom=record['nom'],
                pseudo=record['pseudo'],
                titre=record['titre'],
                message=record['message'],
                approuve=record['approuve']
            )
            db.session.add(new_avis)
        db.session.commit()
        print("Avis chargés depuis le fichier JSON.")
    except FileNotFoundError:
        print("Le fichier avis.json n'existe pas.")

@click.command('save-services')
@with_appcontext
def save_services():
    save_services_to_json()
    print("Services sauvegardés dans le fichier JSON.")

@click.command('load-services')
@with_appcontext
def load_services():
    try:
        services = load_services_from_json()
        if not services:
            print("Aucun service à charger.")
            return
        
        for service in services:
            new_service = Service(
                title=service['title'],
                description=service['description'],
                images_url=service.get('images_url', [])
            )
            db.session.add(new_service)
        db.session.commit()
        print("Services chargés depuis le fichier JSON.")
    except FileNotFoundError:
        print("Le fichier services.json n'existe pas.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

@click.command('add-vet-record')
@with_appcontext
def add_vet_record():
    record = {
        'date': '2024-08-21',
        'health_status': 'Bonne santé',
        'details': 'Aucun problème détecté',
        'animal_id': 5
    }
    save_vet_record_to_json(record)
    print("Fiche vétérinaire ajoutée au fichier JSON.")

@click.command('load-all')
@with_appcontext
def load_all():
    load_users()
    load_animals()
    load_vet_records()
    load_avis()
    load_services()
    print("Toutes les données ont été chargées avec succès.")

def register_commands(app):
    app.cli.add_command(reset_db)
    app.cli.add_command(add_data)
    app.cli.add_command(load_users)
    app.cli.add_command(load_animals)
    app.cli.add_command(restore_data)
    app.cli.add_command(load_vet_records)
    app.cli.add_command(load_avis)
    app.cli.add_command(save_services)
    app.cli.add_command(load_services)
    app.cli.add_command(add_vet_record)
    app.cli.add_command(load_all)
# from flask import current_app
# from flask.cli import with_appcontext
# from app import app, db, Animal, Habitat, VetRecord, User, Avis, Service
# from werkzeug.security import generate_password_hash
# from models import db, User, Habitat, Animal, VetRecord, Avis, Service, DailyFoodRecord
# from datetime import date
# import json
# import click

# @app.cli.command("add-data")
# def add_data():
#     # Assurez-vous que les habitats existent d'abord
#     habitat1 = Habitat(name="Habitat 1 - Savane Africaine", description="Description de l'habitat 1", image="habitat1.jpg")
#     habitat2 = Habitat(name="Habitat 2 - Forêt d'eucalyptus", description="Description de l'habitat 2", image="habitat2.jpg")
#     habitat3 = Habitat(name="Habitat 3 - Forêt Tempérée", description="Description de l'habitat 3", image="habitat3.jpg")
#     habitat4 = Habitat(name="Habitat 4 - Jungle Tropicale", description="Description de l'habitat 4", image="habitat4.jpg")

#     db.session.add_all([habitat1, habitat2, habitat3, habitat4])
#     db.session.commit()

#     # Crée des instances d'animaux pour chaque habitat avec des IDs spécifiques
#     animal1 = Animal(id=1, name="Kibo", species="Zèbre", image="zebre1.jpg", habitat_id=1)
#     animal2 = Animal(id=2, name="Zara", species="Zèbre", image="zebre2.jpg", habitat_id=1)
#     animal3 = Animal(id=3, name="Luna", species="Gazelle", image="gazelle1.jpg", habitat_id=1)
#     animal4 = Animal(id=4, name="Tara", species="Gazelle", image="gazelle2.jpg", habitat_id=1)
#     animal5 = Animal(id=5, name="Mara", species="Girafe", image="girafe1.jpg", habitat_id=1)
#     animal6 = Animal(id=6, name="Jengo", species="Girafe", image="girafe2.jpg", habitat_id=1)
#     animal7 = Animal(id=7, name="Olga", species="Autruche", image="autruche1.jpg", habitat_id=1)
#     animal8 = Animal(id=8, name="Bibi", species="Autruche", image="autruche2.jpg", habitat_id=1)
#     animal9 = Animal(id=9, name="Rico", species="Autruche", image="autruche3.jpg", habitat_id=1)
#     animal10 = Animal(id=10, name="Togo", species="Phacochère", image="phacochere1.jpg", habitat_id=1)
#     animal11 = Animal(id=11, name="Eucalyptus", species="Koala", image="Koala1.jpg", habitat_id=2)
#     animal12 = Animal(id=12, name="Bamboo", species="Koala", image="Koala2.jpg", habitat_id=2)
#     animal13 = Animal(id=13, name="Walt", species="Kangourou", image="kangourou1.jpg", habitat_id=2)
#     animal14 = Animal(id=14, name="Riley", species="Kangourou", image="kangourou2.jpg", habitat_id=2)
#     animal15 = Animal(id=15, name="Pip", species="Possum", image="possum1.jpg", habitat_id=2)
#     animal16 = Animal(id=16, name="Cléo", species="Possum", image="possum2.jpg", habitat_id=2)
#     animal17 = Animal(id=17, name="Thorn", species="Échidné", image="echidne1.jpg", habitat_id=2)
#     animal18 = Animal(id=18, name="Moss", species="Échidné", image="echidne2.jpg", habitat_id=2)
#     animal19 = Animal(id=19, name="Tilly", species="Wallaby", image="wallaby1.jpg", habitat_id=2)
#     animal20 = Animal(id=20, name="Buddy", species="Wallaby", image="wallaby2.jpg", habitat_id=2)
#     animal21 = Animal(id=21, name="Grizz", species="Ours", image="ours1.jpg", habitat_id=3)
#     animal22 = Animal(id=22, name="Willow", species="Ours", image="ours2.jpg", habitat_id=3)
#     animal23 = Animal(id=23, name="Rusty", species="Cerf", image="cerf1.jpg", habitat_id=3)
#     animal24 = Animal(id=24, name="Bella", species="Biche", image="cerf2.jpg", habitat_id=3)
#     animal25 = Animal(id=25, name="Rocky", species="Raton laveur", image="raton1.jpg", habitat_id=3)
#     animal26 = Animal(id=26, name="Misty", species="Raton laveur", image="raton2.jpg", habitat_id=3)
#     animal27 = Animal(id=27, name="Chipper", species="Écureuil", image="ecureuil1.jpg", habitat_id=3)
#     animal28 = Animal(id=28, name="Nutmeg", species="Écureuil", image="ecureuil2.jpg", habitat_id=3)
#     animal29 = Animal(id=29, name="Ollie", species="Chouette rayée", image="chouette1.jpg", habitat_id=3)
#     animal30 = Animal(id=30, name="Hoot", species="Chouette rayée", image="chouette2.jpg", habitat_id=3)
#     animal31 = Animal(id=31, name="Milo", species="Capucin", image="capucin1.jpg", habitat_id=4)
#     animal32 = Animal(id=32, name="Maya", species="Capucin", image="capucin2.jpg", habitat_id=4)
#     animal33 = Animal(id=33, name="Coco", species="Paresseux", image="paresseux1.jpg", habitat_id=4)
#     animal34 = Animal(id=34, name="Gigi", species="Paresseux", image="paresseux2.jpg", habitat_id=4)
#     animal35 = Animal(id=35, name="Mango", species="Toucan", image="toucan1.jpg", habitat_id=4)
#     animal36 = Animal(id=36, name="Kiwi", species="Toucan", image="toucan2.jpg", habitat_id=4)
#     animal37 = Animal(id=37, name="Nina", species="Agouti", image="agouti1.jpg", habitat_id=4)
#     animal38 = Animal(id=38, name="Oscar", species="Agouti", image="agouti2.jpg", habitat_id=4)
#     animal39 = Animal(id=39, name="Vlad", species="Singes-araignée", image="singe-araignee1.jpg", habitat_id=4)
#     animal40 = Animal(id=40, name="Léo", species="Singes-araignée", image="singe-araignee2.jpg", habitat_id=4)

#     # Ajoute les instances à la session de la base de données
#     db.session.add_all([animal1, animal2, animal3, animal4, animal5, animal6, animal7, animal8, animal9, animal10, 
#                         animal11, animal12, animal13, animal14, animal15, animal16, animal17, animal18, animal19, animal20, 
#                         animal21, animal22, animal23, animal24, animal25, animal26, animal27, animal28, animal29, animal30,
#                         animal31, animal32, animal33, animal34, animal35, animal36, animal37, animal38, animal39, animal40])
#     db.session.commit()

#     # Ajoute des fiches vétérinaires pour les animaux
#     vet_records = [
#         VetRecord(date=date(2024, 1, 1), health_status="Bonne santé", details="Aucun problème détecté", animal_id=1),
#         VetRecord(date=date(2024, 1, 10), health_status="Excellente santé", details="Contrôle de routine", animal_id=2),
#         # Ajoutez d'autres fiches vétérinaires ici si nécessaire...
#     ]

#     db.session.add_all(vet_records)
#     db.session.commit()

#     # # Créez un utilisateur admin avec un mot de passe haché
#     # admin = User(username='admin', password=generate_password_hash('admin'), role='admin')
#     # # à voir pour les autres du coup
#     # db.session.add(admin)
#     # db.session.commit()
#     # Créez un utilisateur admin avec un mot de passe haché
#     admin = User(username='admin@admin.fr', email='admin@admin.fr', password=generate_password_hash('admin'), role='admin')
#     db.session.add(admin)
#     db.session.commit()

#     print("Admin user created with username 'admin@admin.fr' and password 'admin'")

#     # Ajoute des utilisateurs avec des rôles spécifiques
#     user1 = User(username="employee@company.com", email="employee@company.com", password=generate_password_hash("employee"), role="employee")
#     user2 = User(username="veterinarian@clinic.com", email="veterinarian@clinic.com", password=generate_password_hash("veterinarian"), role="veterinarian")
#     user3 = User(username="admin2@admin.fr", email="admin2@admin.fr", password=generate_password_hash("admin3"), role="admin")

#     # print("Admin user created with username 'admin' and password 'adminpassword'")

#     # # Ajoute des utilisateurs avec des rôles spécifiques
#     # user1 = User(username="employee", password=generate_password_hash("employee"), role="employee")
#     # user2 = User(username="veterinarian", password=generate_password_hash("veterinarian"), role="veterinarian")
#     # user3 = User(username="admin2", password=generate_password_hash("admin3"), role="admin")

#     db.session.add_all([user1, user2, user3])
#     db.session.commit()

#     print("Données ajoutées avec succès!")

# def load_vet_records_from_json():
#     try:
#         with open('vet_records.json', 'r') as file:
#             vet_records = json.load(file)
#             # print(f"Loaded vet records: {vet_records}")  # Ajoutez cette ligne pour déboguer
#             return vet_records
#     except FileNotFoundError:
#         return []
#     except json.JSONDecodeError as e:
#         print(f"Erreur de décodage JSON: {e}")
#         # Réinitialiser le fichier en cas d'erreur de décodage
#         with open('vet_records.json', 'w') as file:
#             json.dump([], file, indent=4)
#         return []

# def save_vet_record_to_json(vet_record):
#     vet_records = load_vet_records_from_json()
#     vet_records.append(vet_record)
#     with open('vet_records.json', 'w') as file:
#         json.dump(vet_records, file, indent=4)

# # SERVICES
# def save_services_to_json(file_path='services.json'):
#     services = Service.query.all()
#     services_list = []
#     for service in services:
#         services_list.append({
#             'title': service.title,
#             'description': service.description,
#             'images_url': service.images_url
#         })
#     with open(file_path, 'w') as file:
#         json.dump(services_list, file, indent=4)
#     print("Services sauvegardés dans le fichier JSON.")

# def load_services_from_json(file_path='services.json'):
#     with open(file_path, 'r') as file:
#         services = json.load(file)
#         for service in services:
#             new_service = Service(
#                 title=service['title'],
#                 description=service['description'],
#                 images_url=service.get('images_url', [])
#             )
#             db.session.add(new_service)
#         db.session.commit()
#         print("Services chargés depuis le fichier JSON.")

# def load_users_from_json():
#     try:
#         with open('users.json', 'r') as file:
#             users = json.load(file)
#             return users
#     except FileNotFoundError:
#         return []
#     except json.JSONDecodeError as e:
#         print(f"Erreur de décodage JSON: {e}")
#         # Réinitialiser le fichier en cas d'erreur de décodage
#         with open('users.json', 'w') as file:
#             json.dump([], file, indent=4)
#         return []

# def save_user_to_json(user):
#     users = load_users_from_json()
#     users.append(user)
#     with open('users.json', 'w') as file:
#         json.dump(users, file, indent=4)

# @app.cli.command("load-users")
# def load_users():
#     users = load_users_from_json()
#     for user in users:
#         new_user = User(
#             username=user['username'],
#             email=user['email'],
#             password=user['password'],
#             role=user['role']
#         )
#         db.session.add(new_user)
#     db.session.commit()
#     print("Utilisateurs chargés depuis le fichier JSON.")

# def load_animals_from_json():
#     try:
#         with open('animals.json', 'r') as file:
#             animals = json.load(file)
#             return animals
#     except FileNotFoundError:
#         return []
#     except json.JSONDecodeError as e:
#         print(f"Erreur de décodage JSON: {e}")
#         # Réinitialiser le fichier en cas d'erreur de décodage
#         with open('animals.json', 'w') as file:
#             json.dump([], file, indent=4)
#         return []

# def save_animal_to_json(animal):
#     animals = load_animals_from_json()
#     animals.append(animal)
#     with open('animals.json', 'w') as file:
#         json.dump(animals, file, indent=4)

# @app.cli.command("load-animals")
# def load_animals():
#     animals = load_animals_from_json()
#     for animal in animals:
#         new_animal = Animal(
#             name=animal['name'],
#             species=animal['species'],
#             image=animal['image'],
#             habitat_id=animal['habitat_id']
#         )
#         db.session.add(new_animal)
#     db.session.commit()
#     print("Animaux chargés depuis le fichier JSON.")

# @app.cli.command("restore-data")
# def restore_data():
#     vet_records = load_vet_records_from_json()
#     for record in vet_records:
#         vet_record = VetRecord(
#             date=date.fromisoformat(record['date']),
#             health_status=record['health_status'],
#             details=record['details'],
#             animal_id=record['animal_id']
#         )
#         db.session.add(vet_record)
#     db.session.commit()

#     print("Données restaurées avec succès!")

# @app.cli.command("load-vet-records")
# def load_vet_records():
#     vet_records = load_vet_records_from_json()
#     for record in vet_records:
#         new_record = VetRecord(
#             date=date.fromisoformat(record['date']),
#             health_status=record['health_status'],
#             details=record['details'],
#             animal_id=record['animal_id']
#         )
#         db.session.add(new_record)
#     db.session.commit()
#     print("Fiches vétérinaires chargées depuis le fichier JSON.")

# @app.cli.command("load-avis")
# def load_avis():
#     try:
#         with open('avis.json', 'r') as f:
#             avis_data = json.load(f)
#         for record in avis_data:
#             new_avis = Avis(
#                 nom=record['nom'],
#                 pseudo=record['pseudo'],
#                 titre=record['titre'],
#                 message=record['message'],
#                 approuve=record['approuve']
#             )
#             db.session.add(new_avis)
#         db.session.commit()
#         print("Avis chargés depuis le fichier JSON.")
#     except FileNotFoundError:
#         print("Le fichier avis.json n'existe pas.")

# @app.cli.command("save-services")
# def save_services():
#     save_services_to_json()
#     print("Services sauvegardés dans le fichier JSON.")

# @app.cli.command("load-services")
# def load_services():
#     try:
#         services = load_services_from_json()
#         if not services:
#             print("Aucun service à charger.")
#             return
        
#         for service in services:
#             new_service = Service(
#                 title=service['title'],
#                 description=service['description'],
#                 images_url=service.get('images_url', [])
#             )
#             db.session.add(new_service)
#         db.session.commit()
#         print("Services chargés depuis le fichier JSON.")
#     except FileNotFoundError:
#         print("Le fichier services.json n'existe pas.")
#     except Exception as e:
#         print(f"Une erreur s'est produite : {e}")
# # @app.cli.command("load-services")
# # def load_services():
# #     load_services_from_json()
# #     print("Services chargés depuis le fichier JSON.")

# @app.cli.command("add-vet-record")
# def add_vet_record():
#     record = {
#         'date': '2024-08-21',
#         'health_status': 'Bonne santé',
#         'details': 'Aucun problème détecté',
#         'animal_id': 5
#     }
#     save_vet_record_to_json(record)
#     print("Fiche vétérinaire ajoutée au fichier JSON.")

# def get_latest_vet_records(vet_records):
#     latest_records = {}
#     for record in vet_records:
#         animal_id = record['animal_id']
#         if animal_id not in latest_records or record['date'] > latest_records[animal_id]['date']:
#             latest_records[animal_id] = record
#     return latest_records

# @app.cli.command("load-all")
# def load_all():
#     load_users()
#     load_animals()
#     load_vet_records()
#     load_avis()
#     load_services()
#     print("Toutes les données ont été chargées avec succès.")

# @app.cli.command("reset-db")
# def reset_db():
#     # Supprimer toutes les tables
#     db.drop_all()
#     # Recréer toutes les tables
#     db.create_all()
#     print("Base de données réinitialisée!")
# from flask import current_app
# from flask.cli import with_appcontext
# from werkzeug.security import generate_password_hash
# from models import db, User, Habitat, Animal, VetRecord, Avis, Service, DailyFoodRecord
# from datetime import date
# import json
# import click

# @click.command('reset-db')
# @with_appcontext
# def reset_db():
#     db.drop_all()
#     db.create_all()
#     print("Base de données réinitialisée avec succès.")

# @click.command('add-data')
# @with_appcontext
# def add_data():
#     # Assurez-vous que les habitats existent d'abord
#     habitat1 = Habitat(name="Habitat 1 - Savane Africaine", description="Description de l'habitat 1", image="habitat1.jpg")
#     habitat2 = Habitat(name="Habitat 2 - Forêt d'eucalyptus", description="Description de l'habitat 2", image="habitat2.jpg")
#     habitat3 = Habitat(name="Habitat 3 - Forêt Tempérée", description="Description de l'habitat 3", image="habitat3.jpg")
#     habitat4 = Habitat(name="Habitat 4 - Jungle Tropicale", description="Description de l'habitat 4", image="habitat4.jpg")

#     db.session.add_all([habitat1, habitat2, habitat3, habitat4])
#     db.session.commit()

#     # Crée des instances d'animaux pour chaque habitat avec des IDs spécifiques
#     animals = [
#         Animal(id=1, name="Kibo", species="Zèbre", image="zebre1.jpg", habitat_id=1),
#         Animal(id=2, name="Zara", species="Zèbre", image="zebre2.jpg", habitat_id=1),
#         Animal(id=3, name="Luna", species="Gazelle", image="gazelle1.jpg", habitat_id=1),
#         Animal(id=4, name="Tara", species="Gazelle", image="gazelle2.jpg", habitat_id=1),
#         Animal(id=5, name="Mara", species="Girafe", image="girafe1.jpg", habitat_id=1),
#         Animal(id=6, name="Jengo", species="Girafe", image="girafe2.jpg", habitat_id=1),
#         Animal(id=7, name="Olga", species="Autruche", image="autruche1.jpg", habitat_id=1),
#         Animal(id=8, name="Bibi", species="Autruche", image="autruche2.jpg", habitat_id=1),
#         Animal(id=9, name="Rico", species="Autruche", image="autruche3.jpg", habitat_id=1),
#         Animal(id=10, name="Togo", species="Phacochère", image="phacochere1.jpg", habitat_id=1),
#         Animal(id=11, name="Eucalyptus", species="Koala", image="Koala1.jpg", habitat_id=2),
#         Animal(id=12, name="Bamboo", species="Koala", image="Koala2.jpg", habitat_id=2),
#         Animal(id=13, name="Walt", species="Kangourou", image="kangourou1.jpg", habitat_id=2),
#         Animal(id=14, name="Riley", species="Kangourou", image="kangourou2.jpg", habitat_id=2),
#         Animal(id=15, name="Pip", species="Possum", image="possum1.jpg", habitat_id=2),
#         Animal(id=16, name="Cléo", species="Possum", image="possum2.jpg", habitat_id=2),
#         Animal(id=17, name="Thorn", species="Échidné", image="echidne1.jpg", habitat_id=2),
#         Animal(id=18, name="Moss", species="Échidné", image="echidne2.jpg", habitat_id=2),
#         Animal(id=19, name="Tilly", species="Wallaby", image="wallaby1.jpg", habitat_id=2),
#         Animal(id=20, name="Buddy", species="Wallaby", image="wallaby2.jpg", habitat_id=2),
#         Animal(id=21, name="Grizz", species="Ours", image="ours1.jpg", habitat_id=3),
#         Animal(id=22, name="Willow", species="Ours", image="ours2.jpg", habitat_id=3),
#         Animal(id=23, name="Rusty", species="Cerf", image="cerf1.jpg", habitat_id=3),
#         Animal(id=24, name="Bella", species="Biche", image="cerf2.jpg", habitat_id=3),
#         Animal(id=25, name="Rocky", species="Raton laveur", image="raton1.jpg", habitat_id=3),
#         Animal(id=26, name="Misty", species="Raton laveur", image="raton2.jpg", habitat_id=3),
#         Animal(id=27, name="Chipper", species="Écureuil", image="ecureuil1.jpg", habitat_id=3),
#         Animal(id=28, name="Nutmeg", species="Écureuil", image="ecureuil2.jpg", habitat_id=3),
#         Animal(id=29, name="Ollie", species="Chouette rayée", image="chouette1.jpg", habitat_id=3),
#         Animal(id=30, name="Hoot", species="Chouette rayée", image="chouette2.jpg", habitat_id=3),
#         Animal(id=31, name="Milo", species="Capucin", image="capucin1.jpg", habitat_id=4),
#         Animal(id=32, name="Maya", species="Capucin", image="capucin2.jpg", habitat_id=4),
#         Animal(id=33, name="Coco", species="Paresseux", image="paresseux1.jpg", habitat_id=4),
#         Animal(id=34, name="Gigi", species="Paresseux", image="paresseux2.jpg", habitat_id=4),
#         Animal(id=35, name="Mango", species="Toucan", image="toucan1.jpg", habitat_id=4),
#         Animal(id=36, name="Kiwi", species="Toucan", image="toucan2.jpg", habitat_id=4),
#         Animal(id=37, name="Nina", species="Agouti", image="agouti1.jpg", habitat_id=4),
#         Animal(id=38, name="Oscar", species="Agouti", image="agouti2.jpg", habitat_id=4),
#         Animal(id=39, name="Vlad", species="Singes-araignée", image="singe-araignee1.jpg", habitat_id=4),
#         Animal(id=40, name="Léo", species="Singes-araignée", image="singe-araignee2.jpg", habitat_id=4)
#     ]

#     db.session.add_all(animals)
#     db.session.commit()

#     # Ajoute des fiches vétérinaires pour les animaux
#     vet_records = [
#         VetRecord(date=date(2024, 1, 1), health_status="Bonne santé", details="Aucun problème détecté", animal_id=1),
#         VetRecord(date=date(2024, 1, 10), health_status="Excellente santé", details="Contrôle de routine", animal_id=2),
#         # Ajoutez d'autres fiches vétérinaires ici si nécessaire...
#     ]

#     db.session.add_all(vet_records)
#     db.session.commit()

#     # Créez un utilisateur admin avec un mot de passe haché
#     admin = User(username='admin@admin.fr', email='admin@admin.fr', password=generate_password_hash('admin'), role='admin')
#     db.session.add(admin)
#     db.session.commit()

#     print("Admin user created with username 'admin@admin.fr' and password 'admin'")

#     # Ajoute des utilisateurs avec des rôles spécifiques
#     users = [
#         User(username="employee@company.com", email="employee@company.com", password=generate_password_hash("employee"), role="employee"),
#         User(username="veterinarian@clinic.com", email="veterinarian@clinic.com", password=generate_password_hash("veterinarian"), role="veterinarian"),
#         User(username="admin2@admin.fr", email="admin2@admin.fr", password=generate_password_hash("admin3"), role="admin")
#     ]

#     db.session.add_all(users)
#     db.session.commit()

#     print("Données ajoutées avec succès!")

# def load_vet_records_from_json():
#     try:
#         with open('vet_records.json', 'r') as file:
#             vet_records = json.load(file)
#             return vet_records
#     except FileNotFoundError:
#         return []
#     except json.JSONDecodeError as e:
#         print(f"Erreur de décodage JSON: {e}")
#         with open('vet_records.json', 'w') as file:
#             json.dump([], file, indent=4)
#         return []

# def save_vet_record_to_json(vet_record):
#     vet_records = load_vet_records_from_json()
#     vet_records.append(vet_record)
#     with open('vet_records.json', 'w') as file:
#         json.dump(vet_records, file, indent=4)

# def save_services_to_json(file_path='services.json'):
#     services = Service.query.all()
#     services_list = []
#     for service in services:
#         services_list.append({
#             'title': service.title,
#             'description': service.description,
#             'images_url': service.images_url
#         })
#     with open(file_path, 'w') as file:
#         json.dump(services_list, file, indent=4)
#     print("Services sauvegardés dans le fichier JSON.")

# # def load_services_from_json(file_path='services.json'):
# #     with open(file_path, 'r') as file:
# #         services = json.load(file)
# #         for service in services:
# #             new_service = Service(
# #                 title=service['title'],
# #                 description=service['description'],
# #                 images_url=service.get('images_url', [])
# #             )
# #             db.session.add(new_service)
# #         db.session.commit()
# #         print("Services chargés depuis le fichier JSON.")

# # Correction de la fonction load_services_from_json
# def load_services_from_json(file_path='services.json'):
#     with open(file_path, 'r') as file:
#         services = json.load(file)
#         for service in services:
#             new_service = Service(
#                 title=service['title'],
#                 description=service['description'],
#                 images_url=service.get('images_url', [])
#             )
#             db.session.add(new_service)
#         db.session.commit()
#         print("Services chargés depuis le fichier JSON.")

# # def load_users_from_json():
# #     try:
# #         with open('users.json', 'r') as file:
# #             users = json.load(file)
# #             return users
# #     except FileNotFoundError:
# #         return []
# #     except json.JSONDecodeError as e:
# #         print(f"Erreur de décodage JSON: {e}")
# #         with open('users.json', 'w') as file:
# #             json.dump([], file, indent=4)
# #         return []
# # Correction de la fonction load_users_from_json
# def load_users_from_json():
#     try:
#         with open('users.json', 'r') as file:
#             users = json.load(file)
#             return users
#     except FileNotFoundError:
#         return []
#     except json.JSONDecodeError as e:
#         print(f"Erreur de décodage JSON: {e}")
#         with open('users.json', 'w') as file:
#             json.dump([], file, indent=4)
#         return []

# def save_user_to_json(user):
#     users = load_users_from_json()
#     users.append(user)
#     with open('users.json', 'w') as file:
#         json.dump(users, file, indent=4)

# @click.command('load-users')
# @with_appcontext
# def load_users():
#     users = load_users_from_json()
#     for user in users:
#         new_user = User(
#             username=user['username'],
#             email=user['email'],
#             password=user['password'],
#             role=user['role']
#         )
#         db.session.add(new_user)
#     db.session.commit()
#     print("Utilisateurs chargés depuis le fichier JSON.")

# def load_animals_from_json():
#     try:
#         with open('animals.json', 'r') as file:
#             animals = json.load(file)
#             return animals
#     except FileNotFoundError:
#         return []
#     except json.JSONDecodeError as e:
#         print(f"Erreur de décodage JSON: {e}")
#         with open('animals.json', 'w') as file:
#             json.dump([], file, indent=4)
#         return []

# def save_animal_to_json(animal):
#     animals = load_animals_from_json()
#     animals.append(animal)
#     with open('animals.json', 'w') as file:
#         json.dump(animals, file, indent=4)

# @click.command('load-animals')
# @with_appcontext
# def load_animals():
#     animals = load_animals_from_json()
#     for animal in animals:
#         new_animal = Animal(
#             name=animal['name'],
#             species=animal['species'],
#             image=animal['image'],
#             habitat_id=animal['habitat_id']
#         )
#         db.session.add(new_animal)
#     db.session.commit()
#     print("Animaux chargés depuis le fichier JSON.")

# @click.command('restore-data')
# @with_appcontext
# def restore_data():
#     vet_records = load_vet_records_from_json()
#     for record in vet_records:
#         vet_record = VetRecord(
#             date=date.fromisoformat(record['date']),
#             health_status=record['health_status'],
#             details=record['details'],
#             animal_id=record['animal_id']
#         )
#         db.session.add(vet_record)
#     db.session.commit()

#     print("Données restaurées avec succès!")

# @click.command('load-vet-records')
# @with_appcontext
# def load_vet_records():
#     vet_records = load_vet_records_from_json()
#     for record in vet_records:
#         new_record = VetRecord(
#             date=date.fromisoformat(record['date']),
#             health_status=record['health_status'],
#             details=record['details'],
#             animal_id=record['animal_id']
#         )
#         db.session.add(new_record)
#     db.session.commit()
#     print("Fiches vétérinaires chargées depuis le fichier JSON.")

# @click.command('load-avis')
# @with_appcontext
# def load_avis():
#     try:
#         with open('avis.json', 'r') as f:
#             avis_data = json.load(f)
#         for record in avis_data:
#             new_avis = Avis(
#                 nom=record['nom'],
#                 pseudo=record['pseudo'],
#                 titre=record['titre'],
#                 message=record['message'],
#                 approuve=record['approuve']
#             )
#             db.session.add(new_avis)
#         db.session.commit()
#         print("Avis chargés depuis le fichier JSON.")
#     except FileNotFoundError:
#         print("Le fichier avis.json n'existe pas.")

# @click.command('save-services')
# @with_appcontext
# def save_services():
#     save_services_to_json()
#     print("Services sauvegardés dans le fichier JSON.")

# @click.command('load-services')
# @with_appcontext
# def load_services():
#     try:
#         services = load_services_from_json()
#         if not services:
#             print("Aucun service à charger.")
#             return
        
#         for service in services:
#             new_service = Service(
#                 title=service['title'],
#                 description=service['description'],
#                 images_url=service.get('images_url', [])
#             )
#             db.session.add(new_service)
#         db.session.commit()
#         print("Services chargés depuis le fichier JSON.")
#     except FileNotFoundError:
#         print("Le fichier services.json n'existe pas.")
#     except Exception as e:
#         print(f"Une erreur s'est produite : {e}")

# @click.command('add-vet-record')
# @with_appcontext
# def add_vet_record():
#     record = {
#         'date': '2024-08-21',
#         'health_status': 'Bonne santé',
#         'details': 'Aucun problème détecté',
#         'animal_id': 5
#     }
#     save_vet_record_to_json(record)
#     print("Fiche vétérinaire ajoutée au fichier JSON.")

# @click.command('load-all')
# @with_appcontext
# def load_all():
#     load_users()
#     load_animals()
#     load_vet_records()
#     load_avis()
#     load_services()
#     print("Toutes les données ont été chargées avec succès.")

# def register_commands(app):
#     app.cli.add_command(reset_db)
#     app.cli.add_command(add_data)
#     app.cli.add_command(load_users)
#     app.cli.add_command(load_animals)
#     app.cli.add_command(restore_data)
#     app.cli.add_command(load_vet_records)
#     app.cli.add_command(load_avis)
#     app.cli.add_command(save_services)
#     app.cli.add_command(load_services)
#     app.cli.add_command(add_vet_record)
#     app.cli.add_command(load_all)
# # from flask import current_app
# # from flask.cli import with_appcontext
# # from app import app, db, Animal, Habitat, VetRecord, User, Avis, Service
# # from werkzeug.security import generate_password_hash
# # from models import db, User, Habitat, Animal, VetRecord, Avis, Service, DailyFoodRecord
# # from datetime import date
# # import json
# # import click

# # @app.cli.command("add-data")
# # def add_data():
# #     # Assurez-vous que les habitats existent d'abord
# #     habitat1 = Habitat(name="Habitat 1 - Savane Africaine", description="Description de l'habitat 1", image="habitat1.jpg")
# #     habitat2 = Habitat(name="Habitat 2 - Forêt d'eucalyptus", description="Description de l'habitat 2", image="habitat2.jpg")
# #     habitat3 = Habitat(name="Habitat 3 - Forêt Tempérée", description="Description de l'habitat 3", image="habitat3.jpg")
# #     habitat4 = Habitat(name="Habitat 4 - Jungle Tropicale", description="Description de l'habitat 4", image="habitat4.jpg")

# #     db.session.add_all([habitat1, habitat2, habitat3, habitat4])
# #     db.session.commit()

# #     # Crée des instances d'animaux pour chaque habitat avec des IDs spécifiques
# #     animal1 = Animal(id=1, name="Kibo", species="Zèbre", image="zebre1.jpg", habitat_id=1)
# #     animal2 = Animal(id=2, name="Zara", species="Zèbre", image="zebre2.jpg", habitat_id=1)
# #     animal3 = Animal(id=3, name="Luna", species="Gazelle", image="gazelle1.jpg", habitat_id=1)
# #     animal4 = Animal(id=4, name="Tara", species="Gazelle", image="gazelle2.jpg", habitat_id=1)
# #     animal5 = Animal(id=5, name="Mara", species="Girafe", image="girafe1.jpg", habitat_id=1)
# #     animal6 = Animal(id=6, name="Jengo", species="Girafe", image="girafe2.jpg", habitat_id=1)
# #     animal7 = Animal(id=7, name="Olga", species="Autruche", image="autruche1.jpg", habitat_id=1)
# #     animal8 = Animal(id=8, name="Bibi", species="Autruche", image="autruche2.jpg", habitat_id=1)
# #     animal9 = Animal(id=9, name="Rico", species="Autruche", image="autruche3.jpg", habitat_id=1)
# #     animal10 = Animal(id=10, name="Togo", species="Phacochère", image="phacochere1.jpg", habitat_id=1)
# #     animal11 = Animal(id=11, name="Eucalyptus", species="Koala", image="Koala1.jpg", habitat_id=2)
# #     animal12 = Animal(id=12, name="Bamboo", species="Koala", image="Koala2.jpg", habitat_id=2)
# #     animal13 = Animal(id=13, name="Walt", species="Kangourou", image="kangourou1.jpg", habitat_id=2)
# #     animal14 = Animal(id=14, name="Riley", species="Kangourou", image="kangourou2.jpg", habitat_id=2)
# #     animal15 = Animal(id=15, name="Pip", species="Possum", image="possum1.jpg", habitat_id=2)
# #     animal16 = Animal(id=16, name="Cléo", species="Possum", image="possum2.jpg", habitat_id=2)
# #     animal17 = Animal(id=17, name="Thorn", species="Échidné", image="echidne1.jpg", habitat_id=2)
# #     animal18 = Animal(id=18, name="Moss", species="Échidné", image="echidne2.jpg", habitat_id=2)
# #     animal19 = Animal(id=19, name="Tilly", species="Wallaby", image="wallaby1.jpg", habitat_id=2)
# #     animal20 = Animal(id=20, name="Buddy", species="Wallaby", image="wallaby2.jpg", habitat_id=2)
# #     animal21 = Animal(id=21, name="Grizz", species="Ours", image="ours1.jpg", habitat_id=3)
# #     animal22 = Animal(id=22, name="Willow", species="Ours", image="ours2.jpg", habitat_id=3)
# #     animal23 = Animal(id=23, name="Rusty", species="Cerf", image="cerf1.jpg", habitat_id=3)
# #     animal24 = Animal(id=24, name="Bella", species="Biche", image="cerf2.jpg", habitat_id=3)
# #     animal25 = Animal(id=25, name="Rocky", species="Raton laveur", image="raton1.jpg", habitat_id=3)
# #     animal26 = Animal(id=26, name="Misty", species="Raton laveur", image="raton2.jpg", habitat_id=3)
# #     animal27 = Animal(id=27, name="Chipper", species="Écureuil", image="ecureuil1.jpg", habitat_id=3)
# #     animal28 = Animal(id=28, name="Nutmeg", species="Écureuil", image="ecureuil2.jpg", habitat_id=3)
# #     animal29 = Animal(id=29, name="Ollie", species="Chouette rayée", image="chouette1.jpg", habitat_id=3)
# #     animal30 = Animal(id=30, name="Hoot", species="Chouette rayée", image="chouette2.jpg", habitat_id=3)
# #     animal31 = Animal(id=31, name="Milo", species="Capucin", image="capucin1.jpg", habitat_id=4)
# #     animal32 = Animal(id=32, name="Maya", species="Capucin", image="capucin2.jpg", habitat_id=4)
# #     animal33 = Animal(id=33, name="Coco", species="Paresseux", image="paresseux1.jpg", habitat_id=4)
# #     animal34 = Animal(id=34, name="Gigi", species="Paresseux", image="paresseux2.jpg", habitat_id=4)
# #     animal35 = Animal(id=35, name="Mango", species="Toucan", image="toucan1.jpg", habitat_id=4)
# #     animal36 = Animal(id=36, name="Kiwi", species="Toucan", image="toucan2.jpg", habitat_id=4)
# #     animal37 = Animal(id=37, name="Nina", species="Agouti", image="agouti1.jpg", habitat_id=4)
# #     animal38 = Animal(id=38, name="Oscar", species="Agouti", image="agouti2.jpg", habitat_id=4)
# #     animal39 = Animal(id=39, name="Vlad", species="Singes-araignée", image="singe-araignee1.jpg", habitat_id=4)
# #     animal40 = Animal(id=40, name="Léo", species="Singes-araignée", image="singe-araignee2.jpg", habitat_id=4)

# #     # Ajoute les instances à la session de la base de données
# #     db.session.add_all([animal1, animal2, animal3, animal4, animal5, animal6, animal7, animal8, animal9, animal10, 
# #                         animal11, animal12, animal13, animal14, animal15, animal16, animal17, animal18, animal19, animal20, 
# #                         animal21, animal22, animal23, animal24, animal25, animal26, animal27, animal28, animal29, animal30,
# #                         animal31, animal32, animal33, animal34, animal35, animal36, animal37, animal38, animal39, animal40])
# #     db.session.commit()

# #     # Ajoute des fiches vétérinaires pour les animaux
# #     vet_records = [
# #         VetRecord(date=date(2024, 1, 1), health_status="Bonne santé", details="Aucun problème détecté", animal_id=1),
# #         VetRecord(date=date(2024, 1, 10), health_status="Excellente santé", details="Contrôle de routine", animal_id=2),
# #         # Ajoutez d'autres fiches vétérinaires ici si nécessaire...
# #     ]

# #     db.session.add_all(vet_records)
# #     db.session.commit()

# #     # # Créez un utilisateur admin avec un mot de passe haché
# #     # admin = User(username='admin', password=generate_password_hash('admin'), role='admin')
# #     # # à voir pour les autres du coup
# #     # db.session.add(admin)
# #     # db.session.commit()
# #     # Créez un utilisateur admin avec un mot de passe haché
# #     admin = User(username='admin@admin.fr', email='admin@admin.fr', password=generate_password_hash('admin'), role='admin')
# #     db.session.add(admin)
# #     db.session.commit()

# #     print("Admin user created with username 'admin@admin.fr' and password 'admin'")

# #     # Ajoute des utilisateurs avec des rôles spécifiques
# #     user1 = User(username="employee@company.com", email="employee@company.com", password=generate_password_hash("employee"), role="employee")
# #     user2 = User(username="veterinarian@clinic.com", email="veterinarian@clinic.com", password=generate_password_hash("veterinarian"), role="veterinarian")
# #     user3 = User(username="admin2@admin.fr", email="admin2@admin.fr", password=generate_password_hash("admin3"), role="admin")

# #     # print("Admin user created with username 'admin' and password 'adminpassword'")

# #     # # Ajoute des utilisateurs avec des rôles spécifiques
# #     # user1 = User(username="employee", password=generate_password_hash("employee"), role="employee")
# #     # user2 = User(username="veterinarian", password=generate_password_hash("veterinarian"), role="veterinarian")
# #     # user3 = User(username="admin2", password=generate_password_hash("admin3"), role="admin")

# #     db.session.add_all([user1, user2, user3])
# #     db.session.commit()

# #     print("Données ajoutées avec succès!")

# # def load_vet_records_from_json():
# #     try:
# #         with open('vet_records.json', 'r') as file:
# #             vet_records = json.load(file)
# #             # print(f"Loaded vet records: {vet_records}")  # Ajoutez cette ligne pour déboguer
# #             return vet_records
# #     except FileNotFoundError:
# #         return []
# #     except json.JSONDecodeError as e:
# #         print(f"Erreur de décodage JSON: {e}")
# #         # Réinitialiser le fichier en cas d'erreur de décodage
# #         with open('vet_records.json', 'w') as file:
# #             json.dump([], file, indent=4)
# #         return []

# # def save_vet_record_to_json(vet_record):
# #     vet_records = load_vet_records_from_json()
# #     vet_records.append(vet_record)
# #     with open('vet_records.json', 'w') as file:
# #         json.dump(vet_records, file, indent=4)

# # # SERVICES
# # def save_services_to_json(file_path='services.json'):
# #     services = Service.query.all()
# #     services_list = []
# #     for service in services:
# #         services_list.append({
# #             'title': service.title,
# #             'description': service.description,
# #             'images_url': service.images_url
# #         })
# #     with open(file_path, 'w') as file:
# #         json.dump(services_list, file, indent=4)
# #     print("Services sauvegardés dans le fichier JSON.")

# # def load_services_from_json(file_path='services.json'):
# #     with open(file_path, 'r') as file:
# #         services = json.load(file)
# #         for service in services:
# #             new_service = Service(
# #                 title=service['title'],
# #                 description=service['description'],
# #                 images_url=service.get('images_url', [])
# #             )
# #             db.session.add(new_service)
# #         db.session.commit()
# #         print("Services chargés depuis le fichier JSON.")

# # def load_users_from_json():
# #     try:
# #         with open('users.json', 'r') as file:
# #             users = json.load(file)
# #             return users
# #     except FileNotFoundError:
# #         return []
# #     except json.JSONDecodeError as e:
# #         print(f"Erreur de décodage JSON: {e}")
# #         # Réinitialiser le fichier en cas d'erreur de décodage
# #         with open('users.json', 'w') as file:
# #             json.dump([], file, indent=4)
# #         return []

# # def save_user_to_json(user):
# #     users = load_users_from_json()
# #     users.append(user)
# #     with open('users.json', 'w') as file:
# #         json.dump(users, file, indent=4)

# # @app.cli.command("load-users")
# # def load_users():
# #     users = load_users_from_json()
# #     for user in users:
# #         new_user = User(
# #             username=user['username'],
# #             email=user['email'],
# #             password=user['password'],
# #             role=user['role']
# #         )
# #         db.session.add(new_user)
# #     db.session.commit()
# #     print("Utilisateurs chargés depuis le fichier JSON.")

# # def load_animals_from_json():
# #     try:
# #         with open('animals.json', 'r') as file:
# #             animals = json.load(file)
# #             return animals
# #     except FileNotFoundError:
# #         return []
# #     except json.JSONDecodeError as e:
# #         print(f"Erreur de décodage JSON: {e}")
# #         # Réinitialiser le fichier en cas d'erreur de décodage
# #         with open('animals.json', 'w') as file:
# #             json.dump([], file, indent=4)
# #         return []

# # def save_animal_to_json(animal):
# #     animals = load_animals_from_json()
# #     animals.append(animal)
# #     with open('animals.json', 'w') as file:
# #         json.dump(animals, file, indent=4)

# # @app.cli.command("load-animals")
# # def load_animals():
# #     animals = load_animals_from_json()
# #     for animal in animals:
# #         new_animal = Animal(
# #             name=animal['name'],
# #             species=animal['species'],
# #             image=animal['image'],
# #             habitat_id=animal['habitat_id']
# #         )
# #         db.session.add(new_animal)
# #     db.session.commit()
# #     print("Animaux chargés depuis le fichier JSON.")

# # @app.cli.command("restore-data")
# # def restore_data():
# #     vet_records = load_vet_records_from_json()
# #     for record in vet_records:
# #         vet_record = VetRecord(
# #             date=date.fromisoformat(record['date']),
# #             health_status=record['health_status'],
# #             details=record['details'],
# #             animal_id=record['animal_id']
# #         )
# #         db.session.add(vet_record)
# #     db.session.commit()

# #     print("Données restaurées avec succès!")

# # @app.cli.command("load-vet-records")
# # def load_vet_records():
# #     vet_records = load_vet_records_from_json()
# #     for record in vet_records:
# #         new_record = VetRecord(
# #             date=date.fromisoformat(record['date']),
# #             health_status=record['health_status'],
# #             details=record['details'],
# #             animal_id=record['animal_id']
# #         )
# #         db.session.add(new_record)
# #     db.session.commit()
# #     print("Fiches vétérinaires chargées depuis le fichier JSON.")

# # @app.cli.command("load-avis")
# # def load_avis():
# #     try:
# #         with open('avis.json', 'r') as f:
# #             avis_data = json.load(f)
# #         for record in avis_data:
# #             new_avis = Avis(
# #                 nom=record['nom'],
# #                 pseudo=record['pseudo'],
# #                 titre=record['titre'],
# #                 message=record['message'],
# #                 approuve=record['approuve']
# #             )
# #             db.session.add(new_avis)
# #         db.session.commit()
# #         print("Avis chargés depuis le fichier JSON.")
# #     except FileNotFoundError:
# #         print("Le fichier avis.json n'existe pas.")

# # @app.cli.command("save-services")
# # def save_services():
# #     save_services_to_json()
# #     print("Services sauvegardés dans le fichier JSON.")

# # @app.cli.command("load-services")
# # def load_services():
# #     try:
# #         services = load_services_from_json()
# #         if not services:
# #             print("Aucun service à charger.")
# #             return
        
# #         for service in services:
# #             new_service = Service(
# #                 title=service['title'],
# #                 description=service['description'],
# #                 images_url=service.get('images_url', [])
# #             )
# #             db.session.add(new_service)
# #         db.session.commit()
# #         print("Services chargés depuis le fichier JSON.")
# #     except FileNotFoundError:
# #         print("Le fichier services.json n'existe pas.")
# #     except Exception as e:
# #         print(f"Une erreur s'est produite : {e}")
# # # @app.cli.command("load-services")
# # # def load_services():
# # #     load_services_from_json()
# # #     print("Services chargés depuis le fichier JSON.")

# # @app.cli.command("add-vet-record")
# # def add_vet_record():
# #     record = {
# #         'date': '2024-08-21',
# #         'health_status': 'Bonne santé',
# #         'details': 'Aucun problème détecté',
# #         'animal_id': 5
# #     }
# #     save_vet_record_to_json(record)
# #     print("Fiche vétérinaire ajoutée au fichier JSON.")

# # def get_latest_vet_records(vet_records):
# #     latest_records = {}
# #     for record in vet_records:
# #         animal_id = record['animal_id']
# #         if animal_id not in latest_records or record['date'] > latest_records[animal_id]['date']:
# #             latest_records[animal_id] = record
# #     return latest_records

# # @app.cli.command("load-all")
# # def load_all():
# #     load_users()
# #     load_animals()
# #     load_vet_records()
# #     load_avis()
# #     load_services()
# #     print("Toutes les données ont été chargées avec succès.")

# # @app.cli.command("reset-db")
# # def reset_db():
# #     # Supprimer toutes les tables
# #     db.drop_all()
# #     # Recréer toutes les tables
# #     db.create_all()
# #     print("Base de données réinitialisée!")