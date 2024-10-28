from flask import Flask, jsonify, request, flash, redirect, url_for, render_template, session, send_from_directory, current_app, send_file
from flask_login import LoginManager  # Import LoginManager
from config import Config
from models import db, User, SongketDataset, Label, SearchHistory
from sqlalchemy import or_
import io
import os
from sqlalchemy import func
import csv
import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Menetapkan Secret Key
app.secret_key = os.urandom(24)

# Initialize the database with the Flask app
db.init_app(app)

# Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)  # Attach the login manager to the app
login_manager.login_view = 'auth.login'  # Set the login route if user is not authenticated

# Set up the UPLOAD_FOLDER
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, 'uploads')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Define the user loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/get_datasets', methods=['GET'])
def get_datasets():
    datasets = SongketDataset.query.all()
    return jsonify([{
        'id': dataset.id,
        'region': dataset.region,
        'fabric_name': dataset.fabric_name,
        'image_filename': dataset.image_filename,
        'query_image': dataset.query_image 
    } for dataset in datasets])

@app.route('/edit_dataset', methods=['POST'])
def edit_dataset():
    data = request.json
    dataset = SongketDataset.query.get(data['id'])
    if dataset:
        dataset.fabric_name = data['fabric_name']
        dataset.region = data['region']
        db.session.commit()
        return jsonify({'success': True}), 200
    return jsonify({'success': False, 'message': 'Dataset not found'}), 404

@app.route('/delete_dataset', methods=['POST'])
def delete_dataset():
    data = request.json
    dataset = SongketDataset.query.get(data['id'])
    if dataset:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], dataset.image_filename))
        db.session.delete(dataset)
        db.session.commit()
        return jsonify({'success': True}), 200
    return jsonify({'success': False, 'message': 'Dataset not found'}), 404

@app.route('/delete_multiple_datasets', methods=['POST'])
def delete_multiple_datasets():
    ids = request.json.get('ids', [])
    success = True
    
    for id in ids:
        dataset = SongketDataset.query.get(id)
        if dataset:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], dataset.image_filename))
            db.session.delete(dataset)
        else:
            success = False
    
    db.session.commit()
    return jsonify({'success': success})

@app.route('/add_label', methods=['POST'])
def add_label():
    data = request.get_json()
    new_label = Label(fabric_name=data['fabric_name'], region=data['region'], description=data['description']) 
    db.session.add(new_label)
    db.session.commit()
    return jsonify(success=True)

@app.route('/edit_label/<int:id>', methods=['PUT'])
def edit_label(id):
    label = Label.query.get_or_404(id)
    data = request.get_json()
    label.fabric_name = data['fabric_name'] 
    label.region = data['region']
    label.description = data['description']
    db.session.commit()
    return jsonify(success=True)

@app.route('/get_labels', methods=['GET'])
def get_labels():
    labels = Label.query.all()
    return jsonify([{
        'id': label.id,
        'fabric_name': label.fabric_name,  
        'region': label.region,
        'description': label.description,
        'created_at': label.created_at.strftime("%Y-%m-%d %H:%M:%S")
    } for label in labels])

@app.route('/delete_label/<int:id>', methods=['DELETE'])
def delete_label(id):
    label = Label.query.get_or_404(id)
    db.session.delete(label)
    db.session.commit()
    return jsonify(success=True)

@app.route('/delete_multiple_labels', methods=['POST'])
def delete_multiple_labels():
    ids = request.json.get('ids', [])
    labels_to_delete = Label.query.filter(Label.id.in_(ids)).all()
    for label in labels_to_delete:
        db.session.delete(label)
    db.session.commit()
    return jsonify(success=True)

@app.route('/dashboard_admin', methods=['GET', 'POST'])
def dashboard_admin():
    if session.get('user_role') != 'admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        return render_template('admin/dashboard_admin.html')

    # Handle POST request
    dataset_info = db.session.query(
        SongketDataset.fabric_name,
        func.count(SongketDataset.id).label('count')
    ).group_by(SongketDataset.fabric_name).all()

    result = [{'fabric_name': item[0], 'count': item[1]} for item in dataset_info]

    label_info = db.session.query(
        Label.fabric_name,
        func.count(Label.id).label('count')
    ).group_by(Label.fabric_name).all()

    # Prepare the label results in JSON format
    label_result = [{'fabric_name': item[0]} for item in label_info]

    combined_result = {
        'label_info': label_result,
        'dataset_info': result
    }

    return jsonify(combined_result)

@app.route('/get_region/<fabric_name>', methods=['GET'])
def get_region(fabric_name):
    region = db.session.query(Label.region).filter(Label.fabric_name == fabric_name).first()
    if region:
        return region[0]
    return '', 204

@app.route('/api/search-history')
def get_search_history():
    page, per_page = request.args.get('page', 1, int), request.args.get('per_page', 10, int)
    search_query = request.args.get('search', '')
    query = SearchHistory.query.join(User).filter(
        or_(User.username.ilike(f'%{search_query}%'), SearchHistory.query_image.ilike(f'%{search_query}%'))
    ).order_by(SearchHistory.search_timestamp.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'data': [{
            'no': (page - 1) * per_page + idx + 1,
            'id': h.id, 'username': h.user.username, 'query_image': h.query_image,
            'timestamp': h.search_timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for idx, h in enumerate(pagination.items)],
        'total': pagination.total, 'pages': pagination.pages, 'current_page': page, 'per_page': per_page
    })

# Delete search history
@app.route('/api/search-history/<int:history_id>', methods=['DELETE'])
def delete_search_history(history_id):
    history = SearchHistory.query.get(history_id)
    if history:
        db.session.delete(history)
        db.session.commit()
        return jsonify(message='History deleted successfully')
    return jsonify(error='History not found'), 404

@app.route('/api/search-history', methods=['DELETE'])
def delete_all_search_history():
    deleted_count = SearchHistory.query.filter_by(deleted=0).update({'deleted': 1})
    db.session.commit()
    return jsonify(message=f'Successfully deleted {deleted_count} history records')
    
# Import and register blueprints
from routes.admin_routes import admin_bp
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
