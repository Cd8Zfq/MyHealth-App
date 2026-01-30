from app import db

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.String(256))
    phone = db.Column(db.String(20))
    
    def __repr__(self):
        return f'<Patient {self.first_name} {self.last_name}>'
