from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from datetime import datetime, timedelta

from app import db
from app.models.user import User
from app.models.patient import Patient
from app.models.measurement import Measurement
from app.models.appointment import Appointment
from app.routes import bp

def check_doctor():
    """
    Vérifie si l'utilisateur courant a le rôle 'doctor'.
    Lève une erreur 403 sinon.
    """
    if not current_user.is_authenticated or current_user.role != 'doctor':
        abort(403)

@bp.route('/doctor/dashboard')
@login_required
def doctor_dashboard():
    """
    Dashboard Médecin.
    """
    check_doctor()
    
    # 1. ALERTES
    recent_measurements = Measurement.query.join(User).join(Patient)\
        .order_by(Measurement.date.desc())\
        .limit(50).all()
        
    alerts = [m for m in recent_measurements if m.is_alert]
    
    # 2. PROCHAINS RDV
    now = datetime.now()
    next_appointments = Appointment.query.filter(
        Appointment.doctor_id == current_user.id,
        Appointment.start_time >= now,
        Appointment.status != 'cancelled'
    ).order_by(Appointment.start_time).limit(3).all()

    return render_template('doctor/dashboard.html', alerts=alerts, next_appointments=next_appointments)

@bp.route('/doctor/agenda')
@login_required
def agenda():
    check_doctor()
    
    date_str = request.args.get('date')
    if date_str:
        try:
            current_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            current_date = datetime.today().date()
    else:
        current_date = datetime.today().date()
        
    # Week Strip Logic: Yesterday, Today, +5 days (relative to selected date)
    week_days = []
    start_strip = current_date - timedelta(days=1)
    
    french_days = {0: 'Lun', 1: 'Mar', 2: 'Mer', 3: 'Jeu', 4: 'Ven', 5: 'Sam', 6: 'Dim'}
    
    for i in range(7):
        day = start_strip + timedelta(days=i)
        week_days.append({
            'date_str': day.strftime('%Y-%m-%d'),
            'day_name': french_days[day.weekday()],
            'day_num': day.strftime('%d'),
            'is_active': (day == current_date)
        })
        
    day_start = datetime.combine(current_date, datetime.min.time())
    day_end = datetime.combine(current_date, datetime.max.time())
    
    appointments = Appointment.query.filter(
        Appointment.doctor_id == current_user.id,
        Appointment.start_time >= day_start,
        Appointment.start_time <= day_end,
        Appointment.status != 'cancelled'
    ).order_by(Appointment.start_time).all()
    
    now_offset_percent = -1
    is_today = (current_date == datetime.today().date())
    
    if is_today:
        now = datetime.now()
        start_hour = 8
        total_minutes = (now.hour * 60 + now.minute) - (start_hour * 60)
        if 0 <= total_minutes <= 660:
            now_offset_percent = (total_minutes / 660) * 100

    return render_template('doctor/agenda.html', 
                           current_date=current_date, 
                           week_days=week_days, 
                           appointments=appointments,
                           now_offset_percent=now_offset_percent,
                           is_today=is_today)

@bp.route('/appointment/<int:id>/accept')
@login_required
def accept_appointment(id):
    check_doctor()
    apt = Appointment.query.get_or_404(id)
    if apt.doctor_id != current_user.id:
        abort(403)
        
    apt.status = 'confirmed'
    db.session.commit()
    flash('Rendez-vous confirmé.', 'success')
    return redirect(url_for('main.agenda', date=apt.start_time.strftime('%Y-%m-%d')))

@bp.route('/appointment/<int:id>/reject')
@login_required
def reject_appointment(id):
    check_doctor()
    apt = Appointment.query.get_or_404(id)
    if apt.doctor_id != current_user.id:
        abort(403)
        
    # If it was a pending request, we cancel it. If it was a 'free' slot, we remove it (cancel/delete)
    apt.status = 'cancelled'
    db.session.commit()
    flash('Rendez-vous annulé/supprimé.', 'info')
    return redirect(url_for('main.agenda', date=apt.start_time.strftime('%Y-%m-%d')))

@bp.route('/appointment/create_slot', methods=['POST'])
@login_required
def create_slot():
    check_doctor()
    
    date_str = request.form.get('date')
    time_str = request.form.get('time')
    end_time_str = request.form.get('end_time')
    
    if not date_str or not time_str:
        flash('Date et heure requises.', 'error')
        return redirect(url_for('main.agenda'))
        
    start_dt = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
    
    if end_time_str:
        end_dt = datetime.strptime(f"{date_str} {end_time_str}", '%Y-%m-%d %H:%M')
        duration = int((end_dt - start_dt).total_seconds() / 60)
        if duration <= 0:
            flash('L\'heure de fin doit être après l\'heure de début.', 'error')
            return redirect(url_for('main.agenda', date=date_str))
    else:
        end_dt = start_dt + timedelta(minutes=30)
        duration = 30
    
    # Create a free slot
    slot = Appointment(
        doctor_id=current_user.id,
        patient_id=None, # No patient yet
        start_time=start_dt,
        end_time=end_dt,
        duration=duration,
        status='free',
        type='cabinet' # Default
    )
    db.session.add(slot)
    db.session.commit()
    
    flash('Créneau libre ajouté.', 'success')
    return redirect(url_for('main.agenda', date=date_str))

@bp.route('/doctor/patients')
@login_required
def patients():
    check_doctor()
    patients_list = Patient.query.join(User).filter(User.role == 'patient').all()
    return render_template('doctor/patients.html', patients=patients_list)

import json

@bp.route('/doctor/patient/<int:user_id>')
@login_required
def patient_history(user_id):
    check_doctor()
    
    target_user = User.query.get_or_404(user_id)
    if target_user.role != 'patient':
        flash('Cet utilisateur n\'est pas un patient.', 'warning')
        return redirect(url_for('main.patients'))
        
    patient = target_user.patient
    measurements = Measurement.query.filter_by(user_id=user_id).order_by(Measurement.date.desc()).all()
    
    # Prepare chart data
    chart_data = []
    types = ['tension', 'glycemie', 'poids']
    for t in types:
        type_measurements = [m for m in measurements if m.type == t][:20] # Limit points per type
        for m in type_measurements:
            chart_data.append({
                'date': m.date.strftime('%d/%m %H:%M'),
                'type': m.type,
                'val1': m.value1,
                'val2': m.value2,
                'timestamp': m.date.timestamp()
            })
            
    chart_data.sort(key=lambda x: x['timestamp'])
    
    return render_template('doctor/patient_history.html', 
                           patient=patient, 
                           measurements=measurements,
                           chart_data_json=json.dumps(chart_data))
