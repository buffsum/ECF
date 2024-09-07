from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

class DailyFoodRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    food = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    animal = db.relationship('Animal', backref=db.backref('daily_food_records', lazy=True))
    
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# # Modèles
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(120), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)
#     role = db.Column(db.String(20), nullable=False)

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
#     description = db.Column(db.Text, nullable=True)

# class VetRecord(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     date = db.Column(db.Date, nullable=False)
#     health_status = db.Column(db.String(200), nullable=False)
#     details = db.Column(db.Text, nullable=True)
#     animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
#     animal = db.relationship('Animal', back_populates='vet_records')
#     consultation_count = db.Column(db.Integer, default=0)

# class Avis(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nom = db.Column(db.String(100), nullable=False)
#     pseudo = db.Column(db.String(100), nullable=False)
#     titre = db.Column(db.String(100), nullable=False)
#     message = db.Column(db.Text, nullable=False)
#     approuve = db.Column(db.Boolean, default=False)

# class Service(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     images_url = db.Column(db.PickleType, nullable=True)

#     def __init__(self, title, description, images_url=None):
#         self.title = title
#         self.description = description
#         self.images_url = images_url if images_url is not None else []

# class DailyFoodRecord(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.Date, nullable=False)
#     food = db.Column(db.String(100), nullable=False)
#     weight = db.Column(db.Float, nullable=False)
#     animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
#     animal = db.relationship('Animal', backref=db.backref('daily_food_records', lazy=True))