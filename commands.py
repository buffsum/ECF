from app import app, db, Animal, Habitat, VetRecord
from datetime import date

@app.cli.command("add-data")
def add_data():
    # Assurez-vous que les habitats existent d'abord
    habitat1 = Habitat(name="Habitat 1 - Savane Africaine", description="Description de l'habitat 1", image="habitat1.jpg")
    habitat2 = Habitat(name="Habitat 2 - Forêt d'eucalyptus", description="Description de l'habitat 2", image="habitat2.jpg")
    habitat3 = Habitat(name="Habitat 3 - Forêt Tempérée", description="Description de l'habitat 3", image="habitat3.jpg")
    habitat4 = Habitat(name="Habitat 4 - Jungle Tropicale", description="Description de l'habitat 4", image="habitat4.jpg")

    db.session.add_all([habitat1, habitat2, habitat3, habitat4])
    db.session.commit()

    # Crée des animaux pour chaque habitat
    # animals = [
    #     animal1 = Animal(id=1, name="Kibo", species="Zèbre", image="zebre1.jpg", habitat_id=1),
    #     animal2 = Animal(id=2, name="Luna", species="Gazelle", image="gazelle1.jpg", habitat_id=1),
    #     animal3 = Animal(id=3, name="Milo", species="Lion", image="lion1.jpg", habitat_id=2),
    #     animal4 = Animal(id=4, name="Zara", species="Tigre", image="tigre1.jpg", habitat_id=2),
    # ]

    # Crée des instances d'animaux pour chaque habitat avec des IDs spécifiques
    animal1 = Animal(id=1, name="Kibo", species="Zèbre", image="zebre1.jpg", habitat_id=1)
    animal2 = Animal(id=2, name="Zara", species="Zèbre", image="zebre2.jpg", habitat_id=1)
    animal3 = Animal(id=3, name="Luna", species="Gazelle", image="gazelle1.jpg", habitat_id=1)
    animal4 = Animal(id=4, name="Tara", species="Gazelle", image="gazelle2.jpg", habitat_id=1)
    animal5 = Animal(id=5, name="Mara", species="Girafe", image="girafe1.jpg", habitat_id=1)
    animal6 = Animal(id=6, name="Jengo", species="Girafe", image="girafe2.jpg", habitat_id=1)
    animal7 = Animal(id=7, name="Olga", species="Autruche", image="autruche1.jpg", habitat_id=1)
    animal8 = Animal(id=8, name="Bibi", species="Autruche", image="autruche2.jpg", habitat_id=1)
    animal9 = Animal(id=9, name="Rico", species="Autruche", image="autruche3.jpg", habitat_id=1)
    animal10 = Animal(id=10, name="Togo", species="Phacochère", image="phacochere1.jpg", habitat_id=1)
    animal11 = Animal(id=11, name="Eucalyptus", species="Koala", image="Koala1.jpg", habitat_id=2)
    animal12 = Animal(id=12, name="Bamboo", species="Koala", image="Koala2.jpg", habitat_id=2)
    animal13 = Animal(id=13, name="Walt", species="Kangourou", image="kangourou1.jpg", habitat_id=2)
    animal14 = Animal(id=14, name="Riley", species="Kangourou", image="kangourou2.jpg", habitat_id=2)
    animal15 = Animal(id=15, name="Pip", species="Possum", image="possum1.jpg", habitat_id=2)
    animal16 = Animal(id=16, name="Cléo", species="Possum", image="possum2.jpg", habitat_id=2)
    animal17 = Animal(id=17, name="Thorn", species="Échidné", image="echidne1.jpg", habitat_id=2)
    animal18 = Animal(id=18, name="Moss", species="Échidné", image="echidne2.jpg", habitat_id=2)
    animal19 = Animal(id=19, name="Tilly", species="Wallaby", image="wallaby1.jpg", habitat_id=2)
    animal20 = Animal(id=20, name="Buddy", species="Wallaby", image="wallaby2.jpg", habitat_id=2)

    # Ajoute les instances à la session de la base de données
    db.session.add_all([animal1, animal2, animal3, animal4, animal5, animal6, animal7, animal8, animal9, animal10])
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
    db.session.commit()
    print("Animaux ajoutés avec succès!")

@app.cli.command("reset-db")
def reset_db():
    # Supprimer toutes les tables
    db.drop_all()
    # Recréer toutes les tables
    db.create_all()
    print("Base de données réinitialisée!")
