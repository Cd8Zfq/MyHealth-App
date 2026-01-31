from app import create_app, db
from app.models.user import User
from app.models.patient import Patient
from app.models.measurement import Measurement
from app.models.appointment import Appointment
from app.models.reminder import Reminder
from datetime import datetime, timedelta
import random

app = create_app()

def create_dummy_data():
    with app.app_context():
        # 1. Create Doctor
        doctor_email = 'doctor@test.com'
        doctor = User.query.filter_by(email=doctor_email).first()
        if not doctor:
            print(f"Creating doctor: {doctor_email}")
            doctor = User(email=doctor_email, role='doctor')
            doctor.set_password('password')
            db.session.add(doctor)
            db.session.commit()
            
            # Doctor Profile
            doc_profile = Patient(
                user_id=doctor.id,
                first_name='Gregory',
                last_name='House',
                phone='0123456789'
            )
            db.session.add(doc_profile)
        else:
            print(f"Doctor {doctor_email} already exists")

        # 2. Create Patients
        patients_data = [
            ('alice@test.com', 'Alice', 'Wonderland'),
            ('bob@test.com', 'Bob', 'Builder'),
            ('charlie@test.com', 'Charlie', 'Chaplin')
        ]
        
        created_patients = []
        for email, fname, lname in patients_data:
            user = User.query.filter_by(email=email).first()
            if not user:
                print(f"Creating patient: {email}")
                user = User(email=email, role='patient')
                user.set_password('password')
                db.session.add(user)
                db.session.commit()
                
                profile = Patient(
                    user_id=user.id,
                    first_name=fname,
                    last_name=lname,
                    date_of_birth=datetime(1990, 1, 1).date(),
                    phone='0987654321',
                    address='123 Fake St'
                )
                db.session.add(profile)
                db.session.commit()
            else:
                print(f"Patient {email} already exists")
            created_patients.append(user)

        # 3. Create Measurements for Alice
        alice = User.query.filter_by(email='alice@test.com').first()
        if alice:
            print("Adding measurements for Alice...")
            # Delete existing to avoid duplicates if re-run? No, just add some.
            base_time = datetime.now()
            
            # Blood Pressure
            for i in range(5):
                m = Measurement(
                    user_id=alice.id,
                    type='tension',
                    value1=120 + random.randint(-10, 10), # Sys
                    value2=80 + random.randint(-5, 5),   # Dia
                    unit='mmHg',
                    date=base_time - timedelta(days=i),
                    notes='Routine check'
                )
                db.session.add(m)
                
            # Weight
            for i in range(5):
                m = Measurement(
                    user_id=alice.id,
                    type='poids',
                    value1=65 + random.uniform(-0.5, 0.5),
                    unit='kg',
                    date=base_time - timedelta(days=i*2)
                )
                db.session.add(m)
        
        # 4. Create Appointments
        # Doctor needs to be refreshed from session or queried again if committed? 
        # It's attached to session if not closed.
        
        if doctor:
            print("Creating appointments...")
            today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Future Slots (Free)
            for i in range(1, 4):
                start = today + timedelta(days=1, hours=9 + i)
                slot = Appointment(
                    doctor_id=doctor.id,
                    start_time=start,
                    end_time=start + timedelta(minutes=30),
                    status='free',
                    type='cabinet'
                )
                db.session.add(slot)
                
            # Confirmed Appointment (Alice)
            start = today + timedelta(days=2, hours=14)
            apt1 = Appointment(
                doctor_id=doctor.id,
                patient_id=alice.id,
                start_time=start,
                end_time=start + timedelta(minutes=30),
                status='confirmed',
                type='visio',
                video_link='https://meet.google.com/abc-defg-hij'
            )
            db.session.add(apt1)
            
            # Pending Appointment (Bob)
            bob = User.query.filter_by(email='bob@test.com').first()
            if bob:
                start = today + timedelta(days=3, hours=10)
                apt2 = Appointment(
                    doctor_id=doctor.id,
                    patient_id=bob.id,
                    start_time=start,
                    end_time=start + timedelta(minutes=30),
                    status='pending',
                    type='cabinet',
                    notes="Mal de gorge"
                )
                db.session.add(apt2)

        # 5. Reminders for Alice
        if alice:
            print("Adding reminders for Alice...")
            r1 = Reminder(
                user_id=alice.id,
                title='Prendre Vitamine C',
                time='08:00',
                days='Lun,Mer,Ven',
                is_active=True
            )
            db.session.add(r1)

        db.session.commit()
        print("Dummy data creation complete!")

if __name__ == '__main__':
    create_dummy_data()
