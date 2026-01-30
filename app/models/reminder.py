from app import db
from datetime import datetime

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(5), nullable=False) # Format HH:MM
    days = db.Column(db.String(50)) # e.g., "Lundi, Mercredi"
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Reminder {self.title} at {self.time}>'
