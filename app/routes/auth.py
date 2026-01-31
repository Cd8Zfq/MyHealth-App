from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlsplit
from datetime import datetime
from app import db
from app.models.user import User
from app.models.patient import Patient
from app.routes import bp

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Gestion de la connexion utilisateur.
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
                next_page = url_for('main.doctor_dashboard')
        return redirect(next_page)
    
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Gestion de l'inscription utilisateur.
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

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Page de profil utilisateur.
    """
    # Ensure profile record exists
    if not current_user.patient:
        new_profile = Patient(user_id=current_user.id)
        db.session.add(new_profile)
        db.session.commit()
    
    patient = current_user.patient
    
    if request.method == 'POST':
        patient.first_name = request.form.get('first_name')
        patient.last_name = request.form.get('last_name')
        dob_str = request.form.get('date_of_birth')
        if dob_str:
            try:
                patient.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Format de date invalide.')
        patient.address = request.form.get('address')
        patient.phone = request.form.get('phone')
        
        db.session.commit()
        flash('Profil mis à jour avec succès.', 'success')
        return redirect(url_for('main.profile'))
        
    if current_user.role == 'doctor':
        return render_template('doctor/profile.html', patient=patient)
    else:
        return render_template('patient/profile.html', patient=patient)
