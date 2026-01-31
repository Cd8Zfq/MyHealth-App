# MyHealth 🏥

**MyHealth** est une application web de suivi de santé personnel permettant aux utilisateurs d'enregistrer et de visualiser leurs constantes vitales (Tension, Glycémie, Poids) de manière simple et intuitive.

## 🚀 Fonctionnalités Principales

*   **Tableau de Bord Intuitif** : Visualisation rapide de la dernière mesure et des indicateurs de santé.
*   **Suivi Multi-paramètres** :
    *   ❤️ **Tension Artérielle** (Systolique/Diastolique)
    *   🍬 **Glycémie**
    *   ⚖️ **Poids**
*   **Graphiques Dynamiques** : Visualisation de l'évolution des mesures via Chart.js (limité aux 8 dernières mesures par type pour la clarté).
*   **Saisie Intelligente** : Si deux mesures du même type sont saisies à moins de 30 minutes d'intervalle, l'application calcule automatiquement la moyenne.
*   **Exports** : Génération de rapports en **PDF** et exports **Excel** pour le partage avec les professionnels de santé.
*   **Rappels** : Système de configuration de rappels pour la prise de mesures ou médicaments.
*   **Interface Médecin** : Vue dédiée pour les professionnels de santé permettant de suivre leurs patients.

## 🛠️ Prérequis

*   **Python** 3.8+
*   **Node.js** & **npm** (pour la compilation Tailwind CSS)

## ⚙️ Installation

1.  **Cloner le dépôt**
    ```bash
    git clone https://github.com/Cd8Zfq/MyHealth-App.git
    cd MyHealth
    ```

2.  **Configurer l'environnement virtuel Python**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Installer les dépendances Python**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Installer les dépendances Frontend (Tailwind CSS)**
    ```bash
    npm install
    ```

5.  **Configuration**
    Créez un fichier `.env` à la racine du projet (basé sur l'exemple ci-dessous) :
    ```env
    SECRET_KEY=votre_cle_secrete_tres_longue
    DATABASE_URL=sqlite:///app.db
    ```

6.  **Initialiser la Base de Données**
    ```bash
    flask db upgrade
    # Optionnel : Peupler avec des données de test
    python seed.py
    ```

## ▶️ Lancement

1.  **Compiler le CSS (Tailwind)**
    ```bash
    # Compilation unique
    npm run build:css
    
    # Ou mode "watch" pour le développement
    npm run watch:css
    ```

2.  **Lancer le serveur Flask**
    ```bash
    python run.py
    ```

3.  Accédez à l'application via `http://localhost:5000`

## 🏗️ Structure du Projet

*   `app/` : Code source de l'application Flask
    *   `models/` : Modèles de base de données (User, Measurement, etc.)
    *   `routes/` : Logique des vues (Blueprints)
    *   `templates/` : Fichiers HTML (Jinja2)
    *   `static/` : CSS (Tailwind input/output), Images, JS
*   `migrations/` : Scripts de migration de base de données (Alembic)
*   `instance/` : Base de données SQLite locale

## 🛡️ Sécurité & Confidentialité

*   Mots de passe hachés.
*   Protection CSRF sur les formulaires.
*   Données stockées localement (SQLite par défaut).

## 📄 Licence

Ce projet est sous licence MIT.
