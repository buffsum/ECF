from app import app, db, Animal, Habitat, VetRecord
from datetime import date

@app.cli.command("add-data")
def add_data():
    # Assurez-vous que les habitats existent d'abord
    habitat1 = Habitat(name="Habitat 1", description="Description de l'habitat 1", image="habitat1.jpg")
    habitat2 = Habitat(name="Habitat 2", description="Description de l'habitat 2", image="habitat2.jpg")
    habitat3 = Habitat(name="Habitat 3", description="Description de l'habitat 3", image="habitat3.jpg")
    habitat4 = Habitat(name="Habitat 4", description="Description de l'habitat 4", image="habitat4.jpg")

    db.session.add_all([habitat1, habitat2, habitat3, habitat4])
    db.session.commit()

    # Crée des animaux pour chaque habitat
    animals = [
        Animal(name="Kibo", species="Zèbre", image="zebre1.jpg", habitat_id=1),
        Animal(name="Luna", species="Gazelle", image="gazelle1.jpg", habitat_id=1),
        Animal(name="Milo", species="Lion", image="lion1.jpg", habitat_id=2),
        Animal(name="Zara", species="Tigre", image="tigre1.jpg", habitat_id=2),
    ]

    db.session.add_all(animals)
    db.session.commit()

    # Crée des fiches vétérinaires pour les animaux
    vet_records = [
        VetRecord(date=date(2024, 1, 1), food="Herbes", weight=300, health_status="Bonne santé", details="Aucun problème détecté", animal_id=1),
        VetRecord(date=date(2024, 1, 10), food="Herbes", weight=305, health_status="Excellente santé", details="Contrôle de routine", animal_id=2),
    ]

    db.session.add_all(vet_records)
    db.session.commit()

    print("Données ajoutées avec succès!")

@app.cli.command("add-animals")
def add_animals():
    animaux = [
        {"name": "Kibo", "species": "Zèbre", "description": "Description du zèbre", "image": "zebre1.jpg", "habitat_id": 1},
        {"name": "Luna", "species": "Gazelle", "description": "Description de la gazelle", "image": "gazelle1.jpg", "habitat_id": 1},
        {"name": "Milo", "species": "Lion", "description": "Description du lion", "image": "lion1.jpg", "habitat_id": 2},
        {"name": "Zara", "species": "Tigre", "description": "Description du tigre", "image": "tigre1.jpg", "habitat_id": 2},
    ]

    for animal in animaux:
        a = Animal(
            name=animal["name"],
            species=animal["species"],
            image=animal["image"],
            habitat_id=animal["habitat_id"]
        )
        db.session.add(a)

@app.cli.command("reset-db")
def reset_db():
    # Supprimer toutes les tables
    db.drop_all()
    # Recréer toutes les tables
    db.create_all()
    print("Base de données réinitialisée!")


    db.session.commit()
    print("Animaux ajoutés avec succès!")
