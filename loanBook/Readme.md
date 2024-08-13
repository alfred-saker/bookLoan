# BookLoan Application

## Description
Bookstore est une application web qui permet aux utilisateurs de parcourir, télécharger et évaluer des livres et des versions de livres. L'application inclut des fonctionnalités d'authentification, de favoris, de commentaires et de téléchargement.

## Table des Matières
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [API](#api)
- [Fonctionnalités](#fonctionnalités)
- [Structure du Projet](#structure-du-projet)
- [Contribuer](#contribuer)
- [Licence](#licence)

## Installation

### Prérequis
- Node.js et npm: [Installation](https://nodejs.org/)
- Python 3 et pip: [Installation](https://www.python.org/)
- Vue CLI: `npm install -g @vue/cli`

### Backend

1. Clonez le dépôt:
    ```bash
    git clone [https://github.com/votre-utilisateur/bookstore.git](https://github.com/alfred-saker/bookLoan.git)
    cd loanbook/backend
    ```

2. Créez et activez un environnement virtuel:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    .\venv\Scripts\activate  # Windows
    ```

3. Installez les dépendances:
    ```bash
    pip install -r requirements.txt
    ```

4. Appliquez les migrations:
    ```bash
    python manage.py migrate
    ```

5. Créez un super utilisateur:
    ```bash
    python manage.py createsuperuser
    ```

6. Lancez le serveur de développement:
    ```bash
    python manage.py runserver
    ```

### Frontend

1. Naviguez vers le répertoire frontend:
    ```bash
    cd ../frontend
    ```

2. Installez les dépendances:
    ```bash
    npm install
    ```

3. Lancez le serveur de développement:
    ```bash
    npm run serve
    ```

## Configuration

### Backend



### Frontend



## Utilisation

1. Ouvrez votre navigateur et accédez à `http://localhost:8080` pour voir l'application frontend.
2. Accédez à `http://localhost:8000/admin` pour accéder à l'interface d'administration du backend.

## API

### Endpoints Principaux

- **Authentification**
  - `POST /login/` - Connexion de l'utilisateur
  - `POST /logout/` - Déconnexion de l'utilisateur

- **Utilisateurs**
  - `GET /users/` - Liste des utilisateurs
  - `GET /users/:id/` - Détails de l'utilisateur
  - `PATCH /users/:id/update_password/` - Mise à jour du mot de passe
  - `PATCH /users/:id/update_image_user/` - Mise à jour de l'image de profil

- **Livres**
  - `GET /books/` - Liste des livres
  - `GET /books/:id/` - Détails du livre
  - `POST /books/` - Création d'un livre
  - `PATCH /books/:id/` - Mise à jour d'un livre
  - `DELETE /books/:id/` - Suppression d'un livre
  - `GET /books/download/:id/` - Téléchargement du fichier du livre

- **Versions de Livres**
  - `GET /book_versions/` - Liste des versions de livres
  - `GET /book_versions/:id/` - Détails de la version de livre
  - `POST /book_versions/` - Création d'une version de livre
  - `PATCH /book_versions/:id/` - Mise à jour d'une version de livre
  - `DELETE /book_versions/:id/` - Suppression d'une version de livre

- **Favoris**
  - `GET /favorites/` - Liste des favoris
  - `POST /favorites/` - Ajout aux favoris
  - `DELETE /favorites/:id/` - Suppression des favoris

- **Évaluations**
  - `GET /ratings/` - Liste des évaluations
  - `POST /ratings/` - Ajout d'une évaluation
  - `PATCH /ratings/:id/` - Mise à jour d'une évaluation
  - `DELETE /ratings/:id/` - Suppression d'une évaluation

- **Commentaires**
  - `GET /comments/` - Liste des commentaires
  - `POST /comments/` - Ajout d'un commentaire
  - `PATCH /comments/:id/` - Mise à jour d'un commentaire
  - `DELETE /comments/:id/` - Suppression d'un commentaire

## Fonctionnalités

- **Authentification** : Connexion, déconnexion et gestion des utilisateurs.
- **Gestion des Livres** : Création, mise à jour, suppression et téléchargement de livres et de leurs versions.
- **Favoris** : Ajout et suppression de livres et de versions de livres aux favoris.
- **Évaluations** : Ajout et gestion des notes pour les livres.
- **Commentaires** : Ajout et gestion des commentaires sur les livres.

## Structure du Projet

loanbook/
├── backend/
│ ├── manage.py
│ ├── backend/
│ │ ├── settings.py
│ │ ├── urls.py
│ │ ├── models.py
│ │ ├── views.py
│ │ ├── serializers.py
│ │ ├── permissions.py
│ ├── requirements.txt
│ ├── .env.example
├── frontend/
│ ├── public/
│ │ ├── index.html
│ ├── src/
│ │ ├── assets/
│ │ ├── components/
│ │ ├── views/
│ │ ├── router/
│ │ ├── store/
│ │ ├── App.vue
│ │ ├── main.js
│ ├── package.json
│ ├── .env.example


## Contribuer

Les contributions sont les bienvenues ! Veuillez soumettre des demandes de tirage, signaler des problèmes ou suggérer des améliorations.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.
