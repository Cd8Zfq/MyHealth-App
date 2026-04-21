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
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('main.login'))

        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash('Invalid email or password.', 'error')
            return redirect(url_for('main.login'))

        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.home') if user.role == 'patient' else url_for('main.doctor_dashboard')
        return redirect(next_page)

    return render_template('auth/login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('main.register'))

        if User.query.filter_by(email=email).first():
            flash('This email is already registered.', 'error')
            return redirect(url_for('main.register'))

        user = User(email=email, role='patient')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        patient = Patient(user_id=user.id)
        db.session.add(patient)
        db.session.commit()

        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('auth/register.html')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if not current_user.patient:
        db.session.add(Patient(user_id=current_user.id))
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
                flash('Invalid date format.', 'error')
        patient.address = request.form.get('address')
        patient.phone = request.form.get('phone')

        db.session.commit()
        flash('Profile saved.', 'success')
        return redirect(url_for('main.profile'))

    template = 'doctor/profile.html' if current_user.role == 'doctor' else 'patient/profile.html'
    return render_template(template, patient=patient)
