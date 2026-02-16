# MyHealth 🏥

**MyHealth** est une application web complète de suivi de santé personnel permettant aux utilisateurs d'enregistrer et de visualiser leurs constantes vitales (Tension, Glycémie, Poids) de manière simple et intuitive. L'application propose une double interface pour les patients et les professionnels de santé.

## 🚀 Fonctionnalités Principales

### Pour les Patients

*   **Tableau de Bord Intuitif** : Visualisation rapide de la dernière mesure et des indicateurs de santé avec graphiques interactifs
*   **Suivi Multi-paramètres** :
    *   ❤️ **Tension Artérielle** (Systolique/Diastolique)
    *   🍬 **Glycémie** (Gestion optimisée avec analyse automatique)
    *   ⚖️ **Poids** (Suivi de l'évolution)
*   **Graphiques Dynamiques** : Visualisation de l'évolution des mesures via Chart.js (limité aux 8 dernières mesures par type pour la clarté)
*   **Saisie Intelligente** : Si deux mesures du même type sont saisies à moins de 30 minutes d'intervalle, l'application calcule automatiquement la moyenne
*   **Conseils Santé Personnalisés** : Recommandations alimentaires et conseils basés sur vos constantes vitales
*   **Système d'Alertes** : Indicateurs visuels colorés selon la sévérité des mesures (normal, warning, high)
*   **Exports Multi-formats** :
    *   📄 Génération de rapports en **PDF**
    *   📊 Exports **Excel** pour le partage avec les professionnels de santé
*   **Gestion des Rappels** : Système de configuration de rappels pour la prise de mesures ou médicaments avec activation/désactivation
*   **Prise de Rendez-vous** : Réservation de créneaux de consultation auprès des médecins (cabinet, visio, domicile)

### Pour les Médecins

*   **Dashboard Médecin** : Vue d'ensemble avec alertes patients et prochains rendez-vous
*   **Système d'Alertes Prioritaires** : Détection automatique des mesures anormales (Tension > 140/90, Glycémie > 180 mg/dL)
*   **Agenda Interactif** :
    *   Vue hebdomadaire avec navigation intuitive
    *   Gestion des créneaux de disponibilité
    *   Confirmation/rejet des demandes de rendez-vous
    *   Indicateur de temps réel pour la journée en cours
*   **Gestion des Patients** : Liste complète des patients avec accès rapide à leurs profils
*   **Historique Détaillé** : Visualisation complète de l'historique de santé de chaque patient avec graphiques multi-types
*   **Types de Consultation** : Support pour consultations en cabinet, visio et à domicile

## 🛠️ Stack Technique

### Backend
*   **Flask 3.1.2** - Framework web Python
*   **Flask-SQLAlchemy 3.1.1** - ORM pour la gestion de base de données
*   **Flask-Login 0.6.3** - Gestion des sessions utilisateur
*   **Flask-Migrate 4.1.0** - Migrations de base de données (Alembic)
*   **SQLite** - Base de données embarquée (peut être migrée vers PostgreSQL/MySQL)
*   **Werkzeug 3.1.5** - Sécurité (hachage de mots de passe)

### Frontend
*   **Tailwind CSS 4.1.18** - Framework CSS utilitaire
*   **Chart.js** - Bibliothèque de graphiques interactifs
*   **Jinja2 3.1.6** - Moteur de templates

### Exports & Rapports
*   **ReportLab** - Génération de PDF
*   **Pandas** - Manipulation de données
*   **OpenPyXL** - Génération de fichiers Excel

### Outils de Développement
*   **Python-dotenv 1.2.1** - Gestion des variables d'environnement
*   **Colorama 0.4.6** - Sortie console colorée

## 📋 Prérequis

*   **Python** 3.8+ (testé avec Python 3.10+)
*   **Node.js** & **npm** (pour la compilation Tailwind CSS)
*   **pip** (gestionnaire de paquets Python)

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

## 🎯 Utilisation

### Espace Patient

1. **Inscription/Connexion** : Créez un compte patient ou connectez-vous
2. **Tableau de bord** : Visualisez vos dernières mesures et graphiques
3. **Ajouter une mesure** : Enregistrez votre tension, glycémie ou poids
4. **Consulter l'historique** : Accédez à toutes vos mesures avec conseils santé personnalisés
5. **Gérer les rappels** : Configurez des rappels pour vos médicaments ou mesures
6. **Prendre rendez-vous** : Réservez un créneau de consultation avec un médecin
7. **Exporter** : Téléchargez vos données en PDF ou Excel

### Espace Médecin

1. **Connexion** : Connectez-vous avec un compte médecin
2. **Dashboard** : Consultez les alertes patients et vos prochains rendez-vous
3. **Agenda** :
   - Créez des créneaux de disponibilité
   - Confirmez ou rejetez les demandes de rendez-vous
   - Naviguez par jour/semaine
4. **Patients** : Accédez à la liste de vos patients
5. **Historique patient** : Visualisez l'historique complet de santé d'un patient

## ✨ Fonctionnalités Avancées

### Moyenne Automatique
Si vous saisissez deux mesures du même type en moins de 30 minutes, l'application met à jour automatiquement la mesure existante avec la moyenne des deux valeurs.

### Système d'Alertes Intelligent
*   **Normal** (vert) : Valeurs dans les normes
*   **Warning** (orange) : Tension ≥ 120/80, Glycémie ≥ 100 mg/dL
*   **High** (rouge) : Tension ≥ 140/90, Glycémie ≥ 126 mg/dL
*   **Alerte médecin** : Tension > 140/90 ou Glycémie > 180 mg/dL

### Conseils Santé Personnalisés
Le système analyse vos constantes et fournit des recommandations :
*   Aliments à éviter
*   Aliments à favoriser
*   Conseils d'activité physique
*   Messages d'encouragement

### Export Multi-format
*   **PDF** : Rapport formaté avec tableau récapitulatif
*   **Excel** : Données structurées pour analyse approfondie

## 🏗️ Structure du Projet

```
MyHealth/
├── app/
│   ├── __init__.py              # Initialisation Flask & extensions
│   ├── forms.py                 # Formulaires Flask-WTF
│   ├── models/                  # Modèles de données SQLAlchemy
│   │   ├── user.py             # Modèle utilisateur (Patient/Doctor)
│   │   ├── patient.py          # Profil patient
│   │   ├── measurement.py      # Mesures de santé
│   │   ├── reminder.py         # Rappels médicaments/mesures
│   │   └── appointment.py      # Rendez-vous médicaux
│   ├── routes/                  # Routes & logique métier (Blueprints)
│   │   ├── auth.py             # Authentification (login/register)
│   │   ├── patient.py          # Routes patients (dashboard, mesures, export)
│   │   ├── doctor.py           # Routes médecin (agenda, patients, alertes)
│   │   └── public.py           # Routes publiques
│   ├── utils/                   # Utilitaires
│   │   ├── exports.py          # Génération PDF/Excel
│   │   └── health_advice.py    # Système de conseils santé
│   ├── templates/               # Templates Jinja2
│   │   ├── base.html           # Template de base
│   │   ├── auth/               # Pages d'authentification
│   │   ├── measurement/        # Pages de gestion des mesures
│   │   ├── reminder/           # Pages de rappels
│   │   ├── patient/            # Pages patient (profil, booking)
│   │   └── doctor/             # Pages médecin (dashboard, agenda, patients)
│   └── static/                  # Fichiers statiques
│       ├── css/                # Tailwind CSS (input/output)
│       └── images/             # Images et assets
├── migrations/                  # Scripts de migration Alembic
├── instance/                    # Base de données SQLite (app.db)
├── venv/                        # Environnement virtuel Python
├── node_modules/                # Dépendances Node.js (Tailwind)
├── run.py                       # Point d'entrée de l'application
├── requirements.txt             # Dépendances Python
├── package.json                 # Configuration npm (Tailwind)
└── tailwind.config.js           # Configuration Tailwind CSS
```

## 🛡️ Sécurité & Confidentialité

*   **Authentification sécurisée** : Hachage des mots de passe avec Werkzeug (PBKDF2)
*   **Protection CSRF** : Tokens CSRF sur tous les formulaires
*   **Gestion des sessions** : Flask-Login pour la gestion sécurisée des sessions utilisateur
*   **Contrôle d'accès basé sur les rôles** : Séparation stricte entre interface patient et médecin
*   **Données médicales sensibles** : Stockage local sécurisé (SQLite par défaut)
*   **Variables d'environnement** : Clés secrètes et configurations sensibles dans fichier `.env`
*   **Validation des données** : Formulaires Flask-WTF avec validation côté serveur

## 📊 Modèle de Données

### User
*   Authentification (email, mot de passe haché)
*   Rôle : `patient` ou `doctor`
*   Relation avec Patient/Doctor

### Measurement (Mesure)
*   Type : tension, glycémie, poids
*   Valeurs : `value1` (systolique/glucose/poids), `value2` (diastolique pour tension)
*   Unité, date, notes
*   Propriétés calculées : `severity`, `status_color`, `is_alert`

### Reminder (Rappel)
*   Titre, heure, jours de la semaine
*   Statut actif/inactif
*   Lié à un utilisateur

### Appointment (Rendez-vous)
*   Médecin, patient, dates de début/fin
*   Type : cabinet, visio, domicile
*   Statut : free, pending, confirmed, cancelled, done
*   Lien vidéo optionnel, notes

### Patient
*   Informations personnelles (nom, prénom, date de naissance)
*   Adresse, téléphone
*   Contact d'urgence
*   Lié à un compte utilisateur

## 📄 Licence

Ce projet est sous licence MIT.
