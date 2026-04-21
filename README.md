# SahtekFlbal 🏥

Application web de suivi de santé personnel avec double interface patient/médecin.

## 🚀 Fonctionnalités

### Patients
*   Suivi des constantes : Tension, Glycémie, Poids
*   Graphiques d'évolution et conseils santé
*   Export PDF/Excel
*   Rappels médicaments
*   Prise de rendez-vous

### Médecins
*   Dashboard avec alertes patients
*   Agenda et gestion des consultations
*   Historique patients
*   Types de consultation : cabinet, visio, domicile

## 🛠️ Technologies

*   **Backend** : Flask, SQLAlchemy, Flask-Login
*   **Frontend** : Tailwind CSS, Chart.js, Jinja2
*   **Exports** : ReportLab (PDF), Pandas/OpenPyXL (Excel)
*   **BDD** : SQLite (peut être migrée vers PostgreSQL/MySQL)

## 📋 Prérequis

*   Python 3.8+
*   Node.js & npm

## ⚙️ Installation

1.  **Cloner le dépôt**
    ```bash
    git clone https://github.com/Cd8Zfq/SahtekFlbal-App.git
    cd SahtekFlbal
    ```

    > **Note Windows** : Utilisez Git Bash, PowerShell ou CMD pour exécuter ces commandes.

2.  **Configurer l'environnement virtuel Python**

    **Windows :**
    ```cmd
    python -m venv venv
    venv\Scripts\activate
    ```

    **macOS/Linux :**
    ```bash
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
    Créez un fichier `.env` à la racine du projet :

    **Windows (PowerShell) :**
    ```powershell
    New-Item -Path .env -ItemType File
    notepad .env
    ```

    **Windows (CMD) :**
    ```cmd
    type nul > .env
    notepad .env
    ```

    **macOS/Linux :**
    ```bash
    touch .env
    nano .env
    ```

    Ajoutez-y le contenu suivant :
    ```env
    SECRET_KEY=votre_cle_secrete_tres_longue
    DATABASE_URL=sqlite:///app.db
    ```

6.  **Initialiser la Base de Données**
    ```bash
    flask db upgrade
    ```

    **Optionnel : Peupler avec des données de test**
    ```bash
    python seed.py
    ```

## ▶️ Lancement

1.  **Activer l'environnement virtuel**

    **Windows :**
    ```cmd
    venv\Scripts\activate
    ```

    **macOS/Linux :**
    ```bash
    source venv/bin/activate
    ```

2.  **Compiler le CSS (Tailwind)**
    ```bash
    # Compilation unique
    npm run build:css

    # Ou mode "watch" pour le développement
    npm run watch:css
    ```

3.  **Lancer le serveur Flask**
    ```bash
    python run.py
    ```

4.  Accédez à l'application via `http://localhost:5000`


## 🏗️ Structure du Projet

```
SahtekFlbal/
├── app/
│   ├── __init__.py              # Initialisation Flask & extensions
│   ├── forms.py                 # Formulaires Flask-WTF
│   ├── models/                  # Modèles de données SQLAlchemy
│   │   ├── __init__.py
│   │   ├── user.py             # Modèle utilisateur (Patient/Doctor)
│   │   ├── patient.py          # Profil patient
│   │   ├── measurement.py      # Mesures de santé
│   │   ├── reminder.py         # Rappels médicaments/mesures
│   │   └── appointment.py      # Rendez-vous médicaux
│   ├── routes/                  # Routes & logique métier (Blueprints)
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentification (login/register)
│   │   ├── patient.py          # Routes patients (dashboard, mesures, export)
│   │   ├── doctor.py           # Routes médecin (agenda, patients, alertes)
│   │   └── public.py           # Routes publiques
│   ├── utils/                   # Utilitaires
│   │   ├── __init__.py
│   │   ├── exports.py          # Génération PDF/Excel
│   │   └── health_advice.py    # Système de conseils santé
│   ├── templates/               # Templates Jinja2
│   │   ├── base.html           # Template de base
│   │   ├── index.html
│   │   ├── auth/               # Pages d'authentification
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── measurement/        # Pages de gestion des mesures
│   │   │   ├── dashboard.html
│   │   │   ├── add.html
│   │   │   ├── list.html
│   │   │   ├── history.html
│   │   │   └── select_method.html
│   │   ├── reminder/           # Pages de rappels
│   │   │   ├── reminders.html
│   │   │   └── add.html
│   │   ├── patient/            # Pages patient
│   │   │   ├── profile.html
│   │   │   └── booking.html
│   │   └── doctor/             # Pages médecin
│   │       ├── dashboard.html
│   │       ├── agenda.html
│   │       ├── patients.html
│   │       ├── patient_history.html
│   │       └── profile.html
│   └── static/                  # Fichiers statiques
│       ├── css/
│       │   ├── input.css       # Tailwind source
│       │   └── output.css      # Tailwind compilé
│       └── images/
├── migrations/                  # Scripts de migration Alembic
├── instance/                    # Base de données SQLite (app.db)
├── venv/                        # Environnement virtuel Python
├── node_modules/                # Dépendances Node.js (Tailwind)
├── run.py                       # Point d'entrée de l'application
├── requirements.txt             # Dépendances Python
├── package.json                 # Configuration npm (Tailwind)
└── .env                         # Variables d'environnement (à créer)
```

## 🛡️ Sécurité

*   Mots de passe hachés (Werkzeug)
*   Protection CSRF
*   Contrôle d'accès par rôles
*   Variables d'environnement (.env)

## 📄 Licence

Ce projet est sous licence MIT.
