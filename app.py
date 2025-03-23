from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------
# ✅ Define User model
# -----------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# -----------------------
# ✅ Route to display form and users list
# -----------------------
@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

# -----------------------
# ✅ Route to handle form submission
# -----------------------
@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    email = request.form.get('email')

    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400
    
    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('index'))

# -----------------------
# ✅ POST - Create a new user (API)
# -----------------------
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Name and email are required'}), 400
    
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        'message': 'User created successfully',
        'user': {
            'id': new_user.id,
            'name': new_user.name,
            'email': new_user.email
        }
    }), 201

# -----------------------
# ✅ GET - Get all users (API)
# -----------------------
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [
        {'id': user.id, 'name': user.name, 'email': user.email} 
        for user in users
    ]
    return jsonify(result), 200

# -----------------------
# ✅ GET - Get a single user by ID (API)
# -----------------------
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email}), 200

# -----------------------
# ✅ PUT - Update a user by ID (API)
# -----------------------
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if data.get('name'):
        user.name = data['name']
    if data.get('email'):
        user.email = data['email']
    
    db.session.commit()
    
    return jsonify({
        'message': 'User updated successfully',
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
    }), 200

# -----------------------
# ✅ DELETE - Delete a user by ID (API)
# -----------------------
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'}), 200

# -----------------------
# ✅ Start the Flask server
# -----------------------
if __name__ == '__main__':
    app.run(debug=True)
