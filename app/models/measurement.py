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
    
    # Relationship
    user = db.relationship('User', backref='measurements')

    def __repr__(self):
        return f'<Measurement {self.type}: {self.value1}/{self.value2} {self.unit}>'

    @property
    def severity(self):
        """
        Determine severity level: 'normal', 'warning', 'high'.
        """
        if self.type == 'tension':
            if self.value1 >= 140 or (self.value2 and self.value2 >= 90):
                return 'high'
            elif self.value1 >= 120 or (self.value2 and self.value2 >= 80):
                return 'warning'
        
        elif self.type == 'glycemie':
            if self.value1 >= 126:
                return 'high'
            elif self.value1 >= 100:
                return 'warning'
                
        return 'normal'

    @property
    def status_color(self):
        # Returns Tailwind color class part
        sev = self.severity
        if sev == 'high':
            return 'text-red-600'
        elif sev == 'warning':
            return 'text-amber-500'
        return 'text-green-600'

    @property
    def is_alert(self):
        """
        Checks if the measurement should trigger a doctor alert.
        Thresholds: Tension > 140/90, Glycemie > 180.
        """
        if self.type == 'tension':
            # Keeping strict > 140 to match original doctor dashboard logic
            return self.value1 > 140 or (self.value2 and self.value2 > 90)
        elif self.type == 'glycemie':
            return self.value1 > 180
        return False
