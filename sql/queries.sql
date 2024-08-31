-- Sélectionner toutes les lignes de la table Animal
SELECT * FROM animal;

-- Sélectionner toutes les lignes de la table Habitat
SELECT * FROM habitat;

-- Sélectionner toutes les lignes de la table VetRecord (correspond à vet_record dans SQLite)
SELECT * FROM vet_record;

-- Sélectionner un animal spécifique par son ID
SELECT * FROM animal WHERE id = 1;

-- Voir les fiches vétérinaires pour un animal spécifique
SELECT * FROM vet_record WHERE animal_id = 1;

-- Pour chopper les users
SELECT * FROM user;