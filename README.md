### Prérequis

- **Python** : Assurez-vous d'avoir Python installé sur votre machine. Suivez les instructions ci-dessous pour installer Python si nécessaire.
- **Git** : Assurez-vous d'avoir Git installé pour cloner le repository. Vous pouvez télécharger Git depuis [git-scm.com](https://git-scm.com/downloads).

### Étape 1 - Cloner le repository GitHub

Ouvrez un terminal et exécutez la commande suivante pour cloner le repository :
>git clone git@github.com:buffsum/ECF.git
>cd votre-repository

### Étape 2 - Installer Python si ce n'est pas le cas
Ouvrez un terminal et exécutez la commande suivante pour cloner le repository :

## Debian/Ubuntu :
>sudo apt update
>sudo apt install python3 python3-venv python3-pip

## MacOs :
>/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
>brew install python

### Étape 3 - Créer et activer un environnement virtuel
Créez un environnement virtuel pour isoler les dépendances de votre projet :

## MacOs :
>python -m venv venv
>source venv/bin/activate

## Debian/Ubuntu :
>python3 -m venv .venv
>source .venv/bin/activate

### Étape 4 - Installer les dépendances
Installez les dépendances nécessaires à partir du fichier requirements.txt :

## MacOs :
>pip install -r requirements.txt

## Debian/Ubuntu :
>python3 -m pip install -r requirements.txt

### Étape 5 - Configurer la base de données
Initialisez la base de données en exécutant les commandes suivantes dans le terminal :

## MacOs :
>flask reset-db
>./start_mac.sh

## Debian/Ubuntu :
>flask reset-db
>./start_linux.sh

### Étape 6 - Lancer l'application (dans un autre terminal)
>flask run

L'application sera accessible à l'adresse suivante : http://127.0.0.1:5000