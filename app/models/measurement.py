from app import db
from datetime import datetime

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False) # 'tension', 'glycemie', 'poids'
    
    # Store values. For tension, we need two. For others, one.
    # value1: Systolic / Glucose / Weight
    # value2: Diastolic (only for tension)
    value1 = db.Column(db.Float, nullable=False)
    value2 = db.Column(db.Float, nullable=True)
    
    unit = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Measurement {self.type}: {self.value1}/{self.value2} {self.unit}>'

    @property
    def status_color(self):
        # Returns Tailwind color class part: 'green-600', 'amber-500', 'red-600'
        # Green #16A34A -> text-green-600
        # Orange #F59E0B -> text-amber-500
        # Red #DC2626 -> text-red-600
        
        if self.type == 'tension':
            if self.value1 >= 140 or (self.value2 and self.value2 >= 90):
                return 'text-red-600'
            elif self.value1 >= 120 or (self.value2 and self.value2 >= 80):
                return 'text-amber-500'
            else:
                return 'text-green-600'
        
        elif self.type == 'glycemie':
            if self.value1 >= 126:
                return 'text-red-600'
            elif self.value1 >= 100:
                return 'text-amber-500'
            else:
                return 'text-green-600'
                
        # Default green for others
        return 'text-green-600'
