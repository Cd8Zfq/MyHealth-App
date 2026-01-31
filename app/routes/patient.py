from flask import render_template, redirect, url_for, flash, request, send_file, abort
from flask_login import current_user, login_required
import json
from datetime import datetime, timedelta

from app import db
from app.models.measurement import Measurement
from app.models.reminder import Reminder
from app.models.appointment import Appointment
from app.forms import MeasurementForm, ReminderForm
from app.routes import bp
from app.utils.exports import generate_measurements_pdf, generate_measurements_excel
from app.utils.health_advice import get_health_advice

# --- DASHBOARD & MEASUREMENTS ---
@bp.route('/home', methods=['GET'])
@login_required
def home():
    """
    Tableau de bord principal (Dashboard).
    """
    m_type = request.args.get('type')
    
    query = Measurement.query.filter_by(user_id=current_user.id)
        
    if m_type:
        query = query.filter_by(type=m_type)
        
    measurements = query.order_by(Measurement.date.desc()).limit(8).all()
    latest = measurements[0] if measurements else None
    
    # Données pour Chart.js
    chart_data = []
    if measurements:
        chart_data = [{
            'date': m.date.strftime('%d/%m %H:%M'),
            'val1': m.value1,
            'val2': m.value2
        } for m in reversed(measurements)]

    return render_template('measurement/dashboard.html', 
                           measurements=measurements, 
                           latest=latest, 
                           m_type=m_type,
                           chart_data_json=json.dumps(chart_data))

@bp.route('/measurements/select', methods=['GET'])
@login_required
def select_measurement_method():
    return render_template('measurement/select_method.html')

@bp.route('/history', methods=['GET'])
@login_required
def history():
    """
    Historique complet des mesures.
    """
    measurements = Measurement.query.filter_by(user_id=current_user.id).order_by(Measurement.date.desc()).all()
    
    # Données pour le graphique global
    chart_data = []
    types = ['tension', 'glycemie', 'poids']
    
    # Extraction des dernières données pour l'analyse
    analysis_data = {}
    
    # Helper lambda to find latest measurements of a specific type
    get_ms = lambda t: [m for m in measurements if m.type == t]
    
    # Glycemie
    g_list = get_ms('glycemie')
    if g_list:
        analysis_data['glycemie'] = g_list[0].value1
        
    # Tension
    t_list = get_ms('tension')
    if t_list:
        analysis_data['tension'] = t_list[0].value1
        
    # Poids (Actuel + Précédent)
    p_list = get_ms('poids')
    if p_list:
        analysis_data['poids'] = p_list[0].value1
        if len(p_list) > 1:
            analysis_data['poids_precedent'] = p_list[1].value1

    # Génération des conseils
    health_tips = get_health_advice(analysis_data)
    
    # Chart Data Construction
    for t in types:
        type_measurements = [m for m in measurements if m.type == t][:8]
        for m in type_measurements:
            chart_data.append({
                'date': m.date.strftime('%d/%m %H:%M'),
                'type': m.type,
                'val1': m.value1,
                'val2': m.value2,
                'timestamp': m.date.timestamp()
            })
    
    chart_data.sort(key=lambda x: x['timestamp'])

    return render_template('measurement/history.html', 
                           measurements=measurements,
                           chart_data_json=json.dumps(chart_data),
                           health_tips=health_tips)

@bp.route('/measurements/add', methods=['GET', 'POST'])
@login_required
def add_measurement():
    """
    Ajout d'une nouvelle mesure.
    """
    form = MeasurementForm()
    if form.validate_on_submit():
        last_measurement = Measurement.query.filter_by(
            user_id=current_user.id, 
            type=form.type.data
        ).order_by(Measurement.date.desc()).first()
        
        updated = False
        if last_measurement:
            time_diff = datetime.utcnow() - last_measurement.date
            if time_diff < timedelta(minutes=30):
                last_measurement.value1 = (last_measurement.value1 + form.value1.data) / 2
                if form.value2.data and last_measurement.value2:
                    last_measurement.value2 = (last_measurement.value2 + form.value2.data) / 2
                elif form.value2.data:
                    last_measurement.value2 = form.value2.data
                
                last_measurement.date = datetime.utcnow()
                updated = True
                flash('Mesure mise à jour (moyenne sur 30min) avec succès!', 'info')

        if not updated:
            unit = ''
            if form.type.data == 'tension':
                unit = 'mmHg'
            elif form.type.data == 'glycemie':
                unit = 'mg/dL'
            elif form.type.data == 'poids':
                unit = 'kg'
                
            measurement = Measurement(
                user_id=current_user.id,
                type=form.type.data,
                value1=form.value1.data,
                value2=form.value2.data,
                unit=unit,
                notes=form.notes.data
            )
            db.session.add(measurement)
            flash('Mesure ajoutée avec succès!', 'success')
            
        db.session.commit()
        return redirect(url_for('main.home'))
    
    return render_template('measurement/add.html', form=form)

@bp.route('/measurements/list')
@login_required
def list_measurements():
    m_type = request.args.get('type')
    query = Measurement.query.filter_by(user_id=current_user.id)
    
    if m_type:
        query = query.filter_by(type=m_type)
        
    measurements = query.order_by(Measurement.date.desc()).all()
    return render_template('measurement/list.html', measurements=measurements, m_type=m_type)

@bp.route('/measurements/export/pdf')
@login_required
def export_pdf():
    measurements = Measurement.query.filter_by(user_id=current_user.id).order_by(Measurement.date.desc()).all()
    
    buffer = generate_measurements_pdf(measurements, current_user.email)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"mesures_{datetime.now().strftime('%Y%m%d')}.pdf",
        mimetype='application/pdf'
    )

@bp.route('/measurements/export/excel')
@login_required
def export_excel():
    measurements = Measurement.query.filter_by(user_id=current_user.id).order_by(Measurement.date.desc()).all()
    
    buffer = generate_measurements_excel(measurements)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"mesures_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# --- REMINDERS & APPOINTMENTS ---
@bp.route('/reminders')
@login_required
def reminders():
    reminders_list = Reminder.query.filter_by(user_id=current_user.id).order_by(Reminder.time).all()
    appointments_list = Appointment.query.filter_by(patient_id=current_user.id).order_by(Appointment.start_time.desc()).all()
    return render_template('reminder/reminders.html', reminders=reminders_list, appointments=appointments_list)

@bp.route('/patient/book', methods=['GET', 'POST'])
@login_required
def book_appointment():
    if request.method == 'POST':
        slot_id = request.form.get('slot_id')
        reason = request.form.get('reason')
        
        if not slot_id:
            flash('Veuillez sélectionner un créneau.', 'error')
            return redirect(url_for('main.book_appointment'))
            
        slot = Appointment.query.get(slot_id)
        if slot and slot.status == 'free':
            slot.patient_id = current_user.id
            slot.status = 'pending'
            slot.notes = reason
            db.session.commit()
            
            # Flash message with doctor name if possible, or generic
            flash('Votre demande a été envoyée au médecin.', 'success')
            return redirect(url_for('main.reminders'))
        else:
            flash('Ce créneau n\'est plus disponible.', 'error')
            return redirect(url_for('main.book_appointment'))

    # GET: List free slots grouped by day
    now = datetime.now()
    free_slots = Appointment.query.filter(
        Appointment.status == 'free',
        Appointment.start_time > now
    ).order_by(Appointment.start_time).all()
    
    # Group by day
    grouped_slots = {}
    for slot in free_slots:
        day_key = slot.start_time.strftime('%Y-%m-%d')
        if day_key not in grouped_slots:
            grouped_slots[day_key] = {
                'date_obj': slot.start_time,
                'slots': []
            }
        grouped_slots[day_key]['slots'].append(slot)
        
    return render_template('patient/booking.html', grouped_slots=grouped_slots)

@bp.route('/reminders/add', methods=['GET', 'POST'])
@login_required
def add_reminder():
    form = ReminderForm()
    if form.validate_on_submit():
        reminder = Reminder(
            user_id=current_user.id,
            title=form.title.data,
            time=form.time.data,
            days=form.days.data
        )
        db.session.add(reminder)
        db.session.commit()
        flash('Rappel ajouté!', 'success')
        return redirect(url_for('main.reminders'))
    return render_template('reminder/add.html', form=form)

@bp.route('/reminders/toggle/<int:id>')
@login_required
def toggle_reminder(id):
    reminder = Reminder.query.get_or_404(id)
    if reminder.user_id != current_user.id:
        abort(403)
    reminder.is_active = not reminder.is_active
    db.session.commit()
    return redirect(url_for('main.reminders'))

@bp.route('/reminders/delete/<int:id>')
@login_required
def delete_reminder(id):
    reminder = Reminder.query.get_or_404(id)
    if reminder.user_id != current_user.id:
        abort(403)
    db.session.delete(reminder)
    db.session.commit()
    flash('Rappel supprimé.', 'success')
    return redirect(url_for('main.reminders'))