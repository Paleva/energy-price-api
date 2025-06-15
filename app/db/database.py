from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import re
from dotenv import load_dotenv
from os import getenv, urandom
import uuid
from app import app

#-------EXPLANATION HOW TO USE DATABASE IN TERMINAL:------
# Create a user (Create) -> # curl -X POST http://127.0.0.1:5000/users -H "Content-Type: application/json" -d '{"name": "testas", "email": "testas@jo.com"}'
# Get all users (Read) -> # curl -X GET http://127.0.0.1:5000/users
# Get a user by ID -> # curl -X GET http://127.0.0.1:5000/users/1
# Update a user (Update) -> # curl -X PUT http://127.0.0.1:5000/users/1 -H "Content-Type: application/json" -d '{"name": "newname", "email": "newemail@jo.com"}'
# Delete a user (Delete) -> # curl -X DELETE http://127.0.0.1:5000/users/1

load_dotenv()

# Configuration
app.config['SECRET_KEY'] = urandom(24)  # For using /admin page
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')  # Replace with your PostgreSQL credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# User model
class User(db.Model):
   # id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def validate_password(self, password):        
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r'[0-9]', password):
            raise ValueError("Password must contain at least one number")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("Password must contain at least one special character.")
        
# Custom ModelView with Email Validation for Flask-Admin
class UserModelView(ModelView):
    def validate_email(self, form, field):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', field.data):
            raise ValidationError('Invalid email format. Email must contain "@" and a domain.')

    # Override the on_model_change to validate email
    def on_model_change(self, form, model, is_created):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', model.email):
            raise ValidationError('Invalid email format. Email must contain "@" and a domain.')
        return super(UserModelView, self).on_model_change(form, model, is_created)

# Admin view with custom validation
admin = Admin(app)
admin.add_view(UserModelView(User, db.session))

# Initialize database tables
with app.app_context():
    db.create_all()

# CRUD operations for API usage
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Validate email
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', data['email']):
        return jsonify({"error": "Invalid email format. Email must contain '@' and a domain."}), 400
    
    new_user = User(name=data['name'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully!"}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{"name": user.name, "email": user.email, "uuid": user.uuid} for user in users]
    return jsonify(users_list), 200

@app.route('/users/<uuid:uuid>', methods=['GET'])
def get_user(uuid):
    user = User.query.filter_by(uuid=uuid).first_or_404()
    return jsonify({"name": user.name, "email": user.email, "uuid": user.uuid}), 200

@app.route('/users/<uuid:uuid>', methods=['PUT'])
def update_user(uuid):
    user = User.query.filter_by(uuid=uuid).first_or_404()
    data = request.get_json()
    
    # Validate email before updating
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', data['email']):
        return jsonify({"error": "Invalid email format. Email must contain '@' and a domain."}), 400

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify({"message": "User updated successfully!"}), 200

@app.route('/users/<uuid:uuid>', methods=['DELETE'])
def delete_user(uuid):
    user = User.query.filter_by(uuid=uuid).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), 200

@app.route('/register/', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate input data
    if not data or 'name' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing fields."}), 400
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"error": "User already exists."}), 400
    
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', data['email']):
        return jsonify({"error": "Invalid email format. Email must contain '@' and a domain."}), 400

    # Create new user
    new_user = User(name=data['name'], email=data['email'])
    try:
        new_user.validate_password(data['password'])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    new_user.set_password(data['password'])
    
    db.session.add(new_user) 
    db.session.commit()
    
    return jsonify({"message": "User created successfully!"}), 201

@app.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate input data
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing fields."}), 400

    # Check if user exists
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        return jsonify({"message": "Login successful!", "user_id": user.uuid}), 200
    else:
        return jsonify({"error": "Invalid email or password."}), 401