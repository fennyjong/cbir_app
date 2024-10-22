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
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already registered!', 'danger')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Admin login check
        if username == 'admin' and password == 'admin':
            session['user_role'] = 'admin'
            return redirect(url_for('dashboard_admin'))

        # Regular user login
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            user.last_login_at = db.func.now()  # Update last login time
            db.session.commit()  # Save changes
            session['user_role'] = 'user'
            flash('Login successful!', 'success')  
            return redirect(url_for('user.beranda'))
    return render_template('auth/login.html')


@auth_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    username = data.get('username')
    new_password = data.get('new_password')
    
    user = User.query.filter_by(username=username).first()
    if user:
        user.set_password(new_password)
        db.session.commit()
        return jsonify({"success": True, "message": "Password reset successful."}), 200
    
    return jsonify({"success": False, "message": "Username not found."}), 404

@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    session.pop('user_role', None)
    return jsonify({"success": True, "message": "You have been logged out successfully."})


