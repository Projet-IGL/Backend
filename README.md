# Backend Health

## Description

Health est une plateforme conçue pour faciliter les interactions entre le personnel médical et les patients.Cette partie du projet se concentre sur l'implémentation du backend en utilisant Python, Django et SQL pour la gestion de base de donnée.

---

## Table des Matières

- [Installation](#installation)
- [Utilisation](#utilisation)
- [Fonctionnalités](#fonctionnalités)
- [Tests](#tests)
- [Documentation](#documentation)
- [Contact](#contact)

---

## Installation

### Prérequis

- Python installé sur votre système
- Pipenv pour la gestion de l'environnement virtuel
- SQL server
- SQL workbench ou un autre outil de gestion de BDD 

### Étapes

1. Clonez le dépôt :
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```
2.Activez l'environnement virtuel :
   ```bash
   pipenv shell
   ```
3.  Configurez l'environnement virtuel et installez les dépendances :
   ```bash
   pipenv install
   ```

5. Configurez la base de données :
   ```bash
   Veuillez notez qu'il faut changer le mot de passe de la BDD dans settings.py avec votre mot de passe de SQL afin de pouvoir travailler avec une BDD locale sans problème .
    ``` 
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

---

## Utilisation

Exécutez le serveur de développement avec :

```bash
python manage.py runserver
```

Accédez à l'application via l'URL fournie par le serveur local.

---

## Fonctionnalités

- Gestion des fonctionnalités des utilisateurs du personnel médical (médecins , infermiers , laborantins , radiologues )et les patients avec un dossier médical informatisé.
- Intégration de base de données basée sur SQL.
- Tests unitaires backend pour assurer la qualité du code.
- Documentation générée automatiquement avec Sphinx.

---

## Tests

Les tests unitaires sont implémentés dans le fichier `tests.py` situé dans le dossier `backendapp`.

Pour exécuter les tests unitaires, utilisez :

```bash
python manage.py test backendapp
```

---

## Documentation

La documentation pour le backend est générée avec Sphinx.

Pour générer la version PDF de la documentation, exécutez :

```bash
cd docs/source
sphinx-build -b html . _build/html
```
Vous pouvez consulter le repetroire local de votre clone et aller dans
```bash
Backend\build\pdf
``` 
pour y trouver Gestion_DPI_backend.pdf qui est la documentation du code du back end 

## Contact

- **Auteurs :** Bouameur Besmala , Messadia Ishak , Hammou manel
- **Emails :**
  - mb_bouameur@esi.dz
  - mm_messadia@esi.dz
  - mm_hammou@esi.dz
  &#x20;



