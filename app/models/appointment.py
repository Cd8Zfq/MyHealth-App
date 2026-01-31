from app import db
from datetime import datetime

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    start_time = db.Column(db.DateTime, nullable=False, index=True)
    duration = db.Column(db.Integer, default=30)
    end_time = db.Column(db.DateTime, nullable=False)
    
    # 'cabinet', 'visio', 'domicile'
    type = db.Column(db.String(20), default='cabinet') 
    
    # 'scheduled', 'pending', 'cancelled', 'free', 'done'
    status = db.Column(db.String(20), default='pending')
    
    # Lien pour la visio (optionnel)
    video_link = db.Column(db.String(255), nullable=True)
    
    notes = db.Column(db.Text, nullable=True)

    # Relations
    doctor = db.relationship('User', foreign_keys=[doctor_id], backref='doctor_appointments')
    patient = db.relationship('User', foreign_keys=[patient_id], backref='patient_appointments')

    def __repr__(self):
        pid = self.patient_id if self.patient_id else 'No Patient'
        return f'<Appointment {self.start_time} - {pid}>'

    def is_visio(self):
        return self.type == 'visio'

    def is_past(self):
        return self.start_time < datetime.now()
