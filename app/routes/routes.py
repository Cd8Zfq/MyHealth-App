from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, send_file, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models.user import User
from app.models.patient import Patient
from app.models.measurement import Measurement
from app.models.reminder import Reminder
from app.forms import MeasurementForm, ReminderForm
from urllib.parse import urlsplit
import json
import datetime
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

bp = Blueprint('main', __name__)

# --- MAIN ---
@bp.route('/')
def index():
    """
    Page d'accueil publique.
    Affiche la landing page avec les informations générales.
    """
    return render_template('index.html')

# --- AUTH ---
@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Gestion de la connexion utilisateur.
    Gère l'affichage du formulaire et le traitement de la soumission.
    Redirige vers le tableau de bord (patient) ou l'accueil (médecin) après succès.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Veuillez remplir tous les champs.', 'error')
            return redirect(url_for('main.login'))

        user = User.query.filter_by(email=email).first()
        
        if user is None or not user.check_password(password):
            flash('Email ou mot de passe invalide', 'error')
            return redirect(url_for('main.login'))
        
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            if user.role == 'patient':
                next_page = url_for('main.home')
            else:
                next_page = url_for('main.index')
        return redirect(next_page)
    
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Gestion de l'inscription utilisateur.
    Crée un nouvel utilisateur et un profil patient associé.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Veuillez remplir tous les champs.', 'error')
            return redirect(url_for('main.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Cet email est déjà enregistré', 'error')
            return redirect(url_for('main.register'))
            
        user = User(email=email, role='patient')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Création du profil patient vide
        patient = Patient(user_id=user.id)
        db.session.add(patient)
        db.session.commit()
        
        flash('Inscription réussie ! Veuillez vous connecter.', 'success')
        return redirect(url_for('main.login'))
        
    return render_template('auth/register.html')

@bp.route('/logout')
def logout():
    """
    Déconnexion de l'utilisateur courant.
    """
    logout_user()
    return redirect(url_for('main.index'))

# --- MEASUREMENT ---
@bp.route('/home', methods=['GET'])
@login_required
def home():
    """
    Tableau de bord principal (Dashboard).
    Affiche les dernières mesures, un graphique résitulatif et les actions rapides.
    """
    m_type = request.args.get('type')
    
    query = Measurement.query.filter_by(user_id=current_user.id)
        
    if m_type:
        query = query.filter_by(type=m_type)
        
    measurements = query.order_by(Measurement.date.desc()).limit(8).all()
    latest = measurements[0] if measurements else None
    
    # Données pour Chart.js (inversées pour l'ordre chronologique)
    chart_data = []
    if measurements:
        chart_data = [{
            'date': m.date.strftime('%d/%m %H:%M'),
            'val1': m.value1,
            'val2': m.value2
        } for m in reversed(measurements)] # 8 derniers points

    return render_template('measurement/dashboard.html', 
                           measurements=measurements, 
                           latest=latest, 
                           m_type=m_type,
                           chart_data_json=json.dumps(chart_data))

@bp.route('/measurements/select', methods=['GET'])
@login_required
def select_measurement_method():
    """
    Page de sélection de la méthode de saisie (Manuelle ou Capteur).
    """
    return render_template('measurement/select_method.html')

@bp.route('/history', methods=['GET'])
@login_required
def history():
    """
    Historique complet des mesures.
    Affiche toutes les mesures et prépare les données pour le graphique global.
    """
    measurements = Measurement.query.filter_by(user_id=current_user.id).order_by(Measurement.date.desc()).all()
    
    # Données pour le graphique global - Limité à 8 par type
    chart_data = []
    types = ['tension', 'glycemie', 'poids']
    for t in types:
        # Get last 8 measurements for this type (already sorted desc, so take top 8)
        type_measurements = [m for m in measurements if m.type == t][:8]
        for m in type_measurements:
            chart_data.append({
                'date': m.date.strftime('%d/%m %H:%M'),
                'type': m.type,
                'val1': m.value1,
                'val2': m.value2,
                'timestamp': m.date.timestamp()
            })
    
    # Trier par date croissante pour le graphique
    chart_data.sort(key=lambda x: x['timestamp'])

    return render_template('measurement/history.html', 
                           measurements=measurements,
                           chart_data_json=json.dumps(chart_data))

@bp.route('/measurements/add', methods=['GET', 'POST'])
@login_required
def add_measurement():
    """
    Ajout d'une nouvelle mesure (Saisie manuelle).
    Si une mesure du même type existe depuis moins de 30 min, on fait la moyenne.
    """
    form = MeasurementForm()
    if form.validate_on_submit():
        # Check for recent measurement (less than 30 mins)
        last_measurement = Measurement.query.filter_by(
            user_id=current_user.id, 
            type=form.type.data
        ).order_by(Measurement.date.desc()).first()
        
        updated = False
        if last_measurement:
            time_diff = datetime.datetime.utcnow() - last_measurement.date
            if time_diff < datetime.timedelta(minutes=30):
                # Update with mean
                last_measurement.value1 = (last_measurement.value1 + form.value1.data) / 2
                if form.value2.data and last_measurement.value2:
                    last_measurement.value2 = (last_measurement.value2 + form.value2.data) / 2
                elif form.value2.data: # If old didn't have val2 but new does (unlikely for same type but safe)
                    last_measurement.value2 = form.value2.data
                
                last_measurement.date = datetime.datetime.utcnow() # Update timestamp
                updated = True
                flash('Mesure mise à jour (moyenne sur 30min) avec succès!', 'info')

        if not updated:
            # Logique spécifique pour l'unité selon le type
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

# --- PATIENT ---
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Page de profil utilisateur.
    Gère l'affichage et la mise à jour des informations personnelles.
    Adapte l'affichage selon le rôle (Patient ou Docteur).
    """
    if current_user.role == 'patient':
        patient = current_user.patient
        
        if request.method == 'POST':
            patient.first_name = request.form.get('first_name')
            patient.last_name = request.form.get('last_name')
            dob_str = request.form.get('date_of_birth')
            if dob_str:
                try:
                    patient.date_of_birth = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date()
                except ValueError:
                    flash('Format de date invalide.')
            patient.address = request.form.get('address')
            patient.phone = request.form.get('phone')
            
            db.session.commit()
            flash('Profil mis à jour avec succès.', 'success')
            return redirect(url_for('main.profile'))
            
        return render_template('patient/profile.html', patient=patient)
    
    elif current_user.role == 'doctor':
        patient_count = User.query.filter_by(role='patient').count()
        return render_template('doctor/profile.html', patient_count=patient_count)
    
    else:
        return redirect(url_for('main.index'))

# --- REMINDER ---
@bp.route('/reminders')
@login_required
def reminders():
    """
    Liste des rappels de l'utilisateur.
    """
    reminders_list = Reminder.query.filter_by(user_id=current_user.id).order_by(Reminder.time).all()
    return render_template('reminder/reminders.html', reminders=reminders_list)

@bp.route('/reminders/add', methods=['GET', 'POST'])
@login_required
def add_reminder():
    """
    Ajout d'un nouveau rappel.
    """
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
    """
    Active ou désactive un rappel spécifique.
    """
    reminder = Reminder.query.get_or_404(id)
    if reminder.user_id != current_user.id:
        abort(403)
    reminder.is_active = not reminder.is_active
    db.session.commit()
    return redirect(url_for('main.reminders'))

# --- DOCTOR ---
def check_doctor():
    """
    Vérifie si l'utilisateur courant a le rôle 'doctor'.
    Lève une erreur 403 sinon.
    """
    if not current_user.is_authenticated or current_user.role != 'doctor':
        abort(403)

@bp.route('/doctor/patients')
@login_required
def patients():
    """
    Liste tous les patients (Vue Médecin).
    """
    check_doctor()
    patients_list = User.query.filter_by(role='patient').all()
    return render_template('doctor/patients.html', patients=patients_list)

@bp.route('/doctor/patient/<int:user_id>')
@login_required
def patient_history(user_id):
    """
    Affiche l'historique d'un patient spécifique (Vue Médecin).
    """
    check_doctor()
    patient = User.query.get_or_404(user_id)
    measurements = Measurement.query.filter_by(user_id=user_id).order_by(Measurement.date.desc()).all()
    return render_template('doctor/patient_history.html', patient=patient, measurements=measurements)

# --- EXPORT ---
@bp.route('/export/excel')
@login_required
def export_excel():
    """
    Exporte les données de mesure au format Excel.
    """
    user_id = current_user.id if current_user.is_authenticated else 1
    measurements = Measurement.query.filter_by(user_id=current_user.id).all()
    
    data = [{
        'Date': m.date.strftime('%Y-%m-%d %H:%M'),
        'Type': m.type,
        'Valeur 1': m.value1,
        'Valeur 2': m.value2,
        'Unité': m.unit,
        'Notes': m.notes
    } for m in measurements]
    
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Mesures')
    
    output.seek(0)
    return send_file(output, as_attachment=True, download_name=f"MyHealth_Export_{datetime.date.today()}.xlsx")

@bp.route('/export/pdf')
@login_required
def export_pdf():
    """
    Exporte les données de mesure au format PDF (Rapport simple).
    """
    user_id = current_user.id if current_user.is_authenticated else 1
    measurements = Measurement.query.filter_by(user_id=current_user.id).all()
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    elements.append(Paragraph(f"Rapport de Santé - MyHealth", styles['Title']))
    elements.append(Paragraph(f"Généré le: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    elements.append(Paragraph("<br/><br/>", styles['Normal']))
    
    data = [['Date', 'Type', 'Mesure', 'Unité']]
    for m in measurements:
        val = f"{m.value1}" + (f"/{m.value2}" if m.value2 else "")
        data.append([m.date.strftime('%d/%m/%Y'), m.type, val, m.unit])
    
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey)
    ]))
    elements.append(t)
    
    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"MyHealth_Rapport_{datetime.date.today()}.pdf")
