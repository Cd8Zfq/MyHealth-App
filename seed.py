"""
Script de peuplement de la base de données avec des données de test.
Usage: python seed.py
"""
from app import create_app, db
from app.models.user import User
from app.models.patient import Patient
from app.models.measurement import Measurement
from app.models.reminder import Reminder
from app.models.appointment import Appointment
from datetime import datetime, timedelta
import random

def seed_database():
    app = create_app()

    with app.app_context():
        # Nettoyer la base de données existante
        print("🗑️  Nettoyage de la base de données...")
        db.drop_all()
        db.create_all()

        # Créer des médecins
        print("👨‍⚕️  Création des médecins...")
        doctors = []

        doctor1 = User(email='dr.martin@myhealth.fr', role='doctor')
        doctor1.set_password('password123')
        doctors.append(doctor1)

        doctor2 = User(email='dr.dubois@myhealth.fr', role='doctor')
        doctor2.set_password('password123')
        doctors.append(doctor2)

        doctor3 = User(email='isseabdizakaria@gmail.com', role='doctor')
        doctor3.set_password('password123')
        doctors.append(doctor3)

        db.session.add_all(doctors)
        db.session.commit()

        # Créer des patients
        print("👥 Création des patients...")
        patients_data = [
            {
                'email': 'sophie.bernard@email.fr',
                'first_name': 'Sophie',
                'last_name': 'Bernard',
                'date_of_birth': datetime(1985, 3, 15).date(),
                'address': '12 Rue de la République, 75001 Paris',
                'phone': '0601020304'
            },
            {
                'email': 'jean.dupont@email.fr',
                'first_name': 'Jean',
                'last_name': 'Dupont',
                'date_of_birth': datetime(1972, 7, 22).date(),
                'address': '45 Avenue des Champs, 69002 Lyon',
                'phone': '0612345678'
            },
            {
                'email': 'marie.lambert@email.fr',
                'first_name': 'Marie',
                'last_name': 'Lambert',
                'date_of_birth': datetime(1990, 11, 8).date(),
                'address': '8 Boulevard Victor Hugo, 33000 Bordeaux',
                'phone': '0698765432'
            },
            {
                'email': 'pierre.rousseau@email.fr',
                'first_name': 'Pierre',
                'last_name': 'Rousseau',
                'date_of_birth': datetime(1965, 5, 30).date(),
                'address': '23 Rue de la Liberté, 13001 Marseille',
                'phone': '0687654321'
            },
            {
                'email': 'claire.moreau@email.fr',
                'first_name': 'Claire',
                'last_name': 'Moreau',
                'date_of_birth': datetime(1995, 9, 12).date(),
                'address': '56 Rue du Faubourg, 31000 Toulouse',
                'phone': '0623456789'
            }
        ]

        users = []
        for patient_data in patients_data:
            user = User(email=patient_data['email'], role='patient')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()

            patient = Patient(
                user_id=user.id,
                first_name=patient_data['first_name'],
                last_name=patient_data['last_name'],
                date_of_birth=patient_data['date_of_birth'],
                address=patient_data['address'],
                phone=patient_data['phone']
            )
            db.session.add(patient)
            users.append(user)

        db.session.commit()

        # Créer des mesures pour chaque patient
        print("📊 Création des mesures...")
        measurement_types = ['tension', 'glycemie', 'poids']

        for user in users:
            # Créer des mesures sur les 30 derniers jours
            for i in range(15):
                date = datetime.now() - timedelta(days=random.randint(0, 30))

                # Tension artérielle
                systolic = random.randint(110, 155)
                diastolic = random.randint(70, 100)
                measurement = Measurement(
                    user_id=user.id,
                    type='tension',
                    value1=systolic,
                    value2=diastolic,
                    unit='mmHg',
                    date=date,
                    notes='Mesure du matin' if i % 2 == 0 else 'Mesure du soir'
                )
                db.session.add(measurement)

                # Glycémie (certains patients seulement)
                if random.random() > 0.3:
                    glycemie_date = datetime.now() - timedelta(days=random.randint(0, 30))
                    glycemie = random.randint(80, 140)
                    measurement = Measurement(
                        user_id=user.id,
                        type='glycemie',
                        value1=glycemie,
                        unit='mg/dL',
                        date=glycemie_date,
                        notes='À jeun' if i % 3 == 0 else 'Après repas'
                    )
                    db.session.add(measurement)

                # Poids (moins fréquent)
                if i % 3 == 0:
                    poids_date = datetime.now() - timedelta(days=random.randint(0, 30))
                    poids = random.uniform(60, 90)
                    measurement = Measurement(
                        user_id=user.id,
                        type='poids',
                        value1=round(poids, 1),
                        unit='kg',
                        date=poids_date,
                        notes='Pesée hebdomadaire'
                    )
                    db.session.add(measurement)

        db.session.commit()

        # Créer des rappels pour quelques patients
        print("⏰ Création des rappels...")
        reminders_data = [
            {
                'user_id': users[0].id,
                'title': 'Aspirine 100mg',
                'time': '08:00',
                'days': 'Tous les jours'
            },
            {
                'user_id': users[0].id,
                'title': 'Mesure tension',
                'time': '09:00',
                'days': 'Lundi, Mercredi, Vendredi'
            },
            {
                'user_id': users[1].id,
                'title': 'Metformine 500mg',
                'time': '12:00',
                'days': 'Tous les jours'
            },
            {
                'user_id': users[1].id,
                'title': 'Contrôle glycémie',
                'time': '07:30',
                'days': 'Lundi, Jeudi'
            },
            {
                'user_id': users[2].id,
                'title': 'Vitamine D',
                'time': '20:00',
                'days': 'Tous les jours'
            },
            {
                'user_id': users[3].id,
                'title': 'Statine 20mg',
                'time': '21:00',
                'days': 'Tous les jours'
            },
            {
                'user_id': users[4].id,
                'title': 'Contrôle poids',
                'time': '08:30',
                'days': 'Lundi'
            }
        ]

        for reminder_data in reminders_data:
            reminder = Reminder(**reminder_data)
            db.session.add(reminder)

        db.session.commit()

        # Créer des rendez-vous
        print("📅 Création des rendez-vous...")
        appointment_types = ['cabinet', 'visio', 'domicile']
        appointment_statuses = ['scheduled', 'pending', 'done', 'free']

        # Rendez-vous passés
        for i in range(10):
            doctor = random.choice(doctors)
            patient = random.choice(users) if random.random() > 0.2 else None

            days_ago = random.randint(1, 60)
            start_time = datetime.now() - timedelta(days=days_ago, hours=random.randint(8, 17))
            duration = random.choice([30, 45, 60])
            end_time = start_time + timedelta(minutes=duration)

            appointment = Appointment(
                doctor_id=doctor.id,
                patient_id=patient.id if patient else None,
                start_time=start_time,
                duration=duration,
                end_time=end_time,
                type=random.choice(appointment_types),
                status='done' if patient else 'free',
                notes='Consultation de suivi' if patient else None
            )

            if appointment.type == 'visio' and patient:
                appointment.video_link = 'https://meet.example.com/' + str(random.randint(1000, 9999))

            db.session.add(appointment)

        # Rendez-vous futurs
        for i in range(15):
            doctor = random.choice(doctors)
            patient = random.choice(users) if random.random() > 0.3 else None

            days_ahead = random.randint(1, 30)
            start_time = datetime.now() + timedelta(days=days_ahead, hours=random.randint(8, 17))
            duration = random.choice([30, 45, 60])
            end_time = start_time + timedelta(minutes=duration)

            status = 'scheduled' if patient else 'free'
            if patient and random.random() > 0.7:
                status = 'pending'

            appointment = Appointment(
                doctor_id=doctor.id,
                patient_id=patient.id if patient else None,
                start_time=start_time,
                duration=duration,
                end_time=end_time,
                type=random.choice(appointment_types),
                status=status,
                notes='Consultation initiale' if patient and status == 'pending' else None
            )

            if appointment.type == 'visio' and patient:
                appointment.video_link = 'https://meet.example.com/' + str(random.randint(1000, 9999))

            db.session.add(appointment)

        db.session.commit()

        print("\n✅ Base de données peuplée avec succès !")
        print("\n📋 Comptes créés :")
        print("\n👨‍⚕️ Médecins :")
        print("   - dr.martin@myhealth.fr / password123")
        print("   - dr.dubois@myhealth.fr / password123")
        print("   - isseabdizakaria@gmail.com / password123")
        print("\n👥 Patients :")
        for patient_data in patients_data:
            print(f"   - {patient_data['email']} / password123")
        print("\n💡 Statistiques :")
        print(f"   - {User.query.count()} utilisateurs")
        print(f"   - {Patient.query.count()} patients")
        print(f"   - {Measurement.query.count()} mesures")
        print(f"   - {Reminder.query.count()} rappels")
        print(f"   - {Appointment.query.count()} rendez-vous")

if __name__ == '__main__':
    seed_database()
