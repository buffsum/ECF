Étape 1 - Cloner le repository GitHub
Ouvrez un terminal et exécutez la commande suivante pour cloner le repository :
>git clone https://github.com/votre-utilisateur/votre-repository.git
>cd votre-repository

Étape 2 - installer Python si ce n'est pas le cas
## Guide d'installation et de configuration

### Prérequis

- **Python** : Assurez-vous d'avoir Python installé sur votre machine. Suivez les instructions ci-dessous pour installer Python si nécessaire.
- **Git** : Assurez-vous d'avoir Git installé pour cloner le repository. Vous pouvez télécharger Git depuis [git-scm.com](https://git-scm.com/downloads).

### Étape 1 - Cloner le repository GitHub

Ouvrez un terminal et exécutez la commande suivante pour cloner le repository :

```bash
>git clone https://github.com/votre-utilisateur/votre-repository.git
>cd votre-repository

Debian/Ubuntu :
>sudo apt update
>sudo apt install python3 python3-venv python3-pip

MacOs :
>/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
>brew install python

Étape 3 - Créer et activer un environnement virtuel
Créez un environnement virtuel pour isoler les dépendances de votre projet :
>python -m venv venv
>source venv/bin/activate

Linux :
>python3 -m venv .venv
>source .venv/bin/activate

Étape 4 - Installer les dépendances
Installez les dépendances nécessaires à partir du fichier requirements.txt :
>pip install -r requirements.txt

Linux :
>python3 -m pip install -r requirements.txt

Étape 5 - Configurer la base de données
Initialisez la base de données en exécutant les commandes suivantes dans le terminal :
>flask reset-db
>flask add-data
>flask load-users
>flask load-animals
>flask load-vet-records
>flask load-avis
>flask load-services
>flask load-daily-food

Étape 6 - Lancer l'application
>flask run

L'application sera accessible à l'adresse suivante : http://127.0.0.1:5000
