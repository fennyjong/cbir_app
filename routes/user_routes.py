from flask import Blueprint, render_template
from flask_login import login_required

user_bp = Blueprint('user', __name__) 

@user_bp.route('/beranda')
@login_required
def beranda():
    return render_template('users/beranda.html')

@user_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    return render_template('users/modul_upload.html')

@user_bp.route('/hasil', methods=['GET', 'POST'])
@login_required
def hasil():
    return render_template('users/modul_hasil.html')

@user_bp.route('/informasi')
@login_required
def informasi():
    return render_template('users/modul_informasi.html')
