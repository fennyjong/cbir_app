from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Cek apakah username sudah ada
        if User.query.filter_by(username=username).first():
            flash('Username sudah terdaftar!', 'danger')
            return redirect(url_for('auth.register'))

        # Cek apakah email sudah ada
        if User.query.filter_by(email=email).first():
            flash('Email sudah terdaftar!', 'danger')
            return redirect(url_for('auth.register'))

        # Validasi email sederhana
        if '@' not in email or '.' not in email:
            flash('Email tidak valid!', 'danger')
            return redirect(url_for('auth.register'))

        # Buat user baru
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email')  # Updated to match the form input
        password = request.form.get('password')

        # Admin login check
        if username_or_email == 'admin' and password == 'admin':
            session['user_role'] = 'admin'
            return redirect(url_for('dashboard_admin'))

        # Regular user login
        user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()  # Check both username and email
        if user and user.check_password(password):
            login_user(user)
            user.last_login_at = db.func.now()  # Update last login time
            db.session.commit()  # Save changes
            session['user_role'] = 'user'
            return redirect(url_for('user.beranda'))
        else:
            flash('Invalid username/email or password!', 'danger')  # Flash message for invalid login

    return render_template('auth/login.html')


@auth_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    username_or_email = data.get('username_or_email')
    new_password = data.get('new_password')

    # Mencari user berdasarkan username atau email
    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

    if user:
        user.set_password(new_password)  # Assuming you have a method to set the password
        db.session.commit()
        return jsonify({"success": True, "message": "Password berhasil direset."})
    else:
        return jsonify({"success": False, "message": "Username atau Email tidak ditemukan."})


@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    session.pop('user_role', None)
    return jsonify({"success": True, "message": "Anda berhasil logout."})
