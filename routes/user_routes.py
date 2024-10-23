from flask import Blueprint, render_template
from flask_login import login_required
from models import db
from models import Label, SongketDataset

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


@user_bp.route('/panduan')
@login_required
def panduan():
    return render_template('users/panduan.html')

@user_bp.route('/informasi')
def display_songket():
    # Join between SongketDataset and Label to get unique songket data with labels
    songkets_with_labels = db.session.query(SongketDataset, Label).\
        join(Label, SongketDataset.fabric_name == Label.fabric_name).\
        distinct(SongketDataset.fabric_name).all()

    # Check if data is available
    if not songkets_with_labels:
        error = "Tidak ada songket yang tersedia saat ini."
        return render_template('users/modul_informasi.html', error=error)

    # Return template with songket and label data
    return render_template('users/modul_informasi.html', songkets_with_labels=songkets_with_labels)