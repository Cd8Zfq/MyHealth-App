from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, TextAreaField, RadioField, StringField
from wtforms.validators import DataRequired, Optional, NumberRange


class MeasurementForm(FlaskForm):
    type = RadioField('Measurement type', choices=[
        ('tension', 'Blood Pressure (mmHg)'),
        ('glycemie', 'Blood Sugar (mg/dL)'),
        ('poids', 'Weight (kg)')
    ], validators=[DataRequired()])

    value1 = FloatField('Value 1', validators=[DataRequired(), NumberRange(min=0, max=500)])
    value2 = FloatField('Value 2 (Diastolic)', validators=[Optional(), NumberRange(min=0, max=300)])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save')


class ReminderForm(FlaskForm):
    title = StringField('Reminder title', validators=[DataRequired()])
    time = StringField('Time (HH:MM)', validators=[DataRequired()])
    days = StringField('Days (optional)', validators=[Optional()])
    submit = SubmitField('Save reminder')
