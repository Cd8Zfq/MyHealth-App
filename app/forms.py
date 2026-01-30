from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Optional

class MeasurementForm(FlaskForm):
    type = RadioField('Type de mesure', choices=[
        ('tension', 'Tension Artérielle (mmHg)'),
        ('glycemie', 'Glycémie (mg/dL)'),
        ('poids', 'Poids (kg)')
    ], validators=[DataRequired()])
    
    value1 = FloatField('Valeur 1 (Systolique / Glucose / Poids)', validators=[DataRequired()])
    value2 = FloatField('Valeur 2 (Diastolique - Tension uniquement)', validators=[Optional()])
    
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Ajouter une mesure')

from wtforms import StringField, BooleanField

class ReminderForm(FlaskForm):
    title = StringField('Titre du rappel (ex: Médicament, Glycémie)', validators=[DataRequired()])
    time = StringField('Heure (HH:MM)', validators=[DataRequired()])
    days = StringField('Jours (ex: Tous les jours, Lun-Ven)', validators=[Optional()])
    submit = SubmitField('Enregistrer le rappel')
