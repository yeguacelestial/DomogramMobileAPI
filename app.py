import os
import json
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from dotenv import load_dotenv

from flask import Flask, request, Response, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_mail import Mail, Message


# --- SETTINGS ---
# Load env variables
load_dotenv()

# Initialize Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

# Flask Mail config
app.config.from_pyfile('config.cfg')
mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])


# --- DB MODELS ---
# Table: User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(15), unique=False)
    verified = db.Column(db.Boolean, unique=False)


# --- API ENDPOINTS ---
# Endpoint: SignIn
class SignIn(Resource):
    def get(self):
        return {'test': 'this is a test for signin endpoint'}, 201

    def post(self):
        # Filter request data
        user_json = request.get_json()

        # Validate if user is registered
        user = User.query.filter_by(email=user_json['email']).first()

        if user:
            response = handle_signin(user_json, user)

        else:
            response = Response(
                response=json.dumps(
                    {'error': 'El usuario no existe. Asegúrate de haberte registrado en Domogram.'}),
                status=201,
                mimetype='application/json')

        return response


# Endpoint: SignUp
class SignUp(Resource):
    def get(self):
        return {'test': 'this is a test for signup endpoint'}, 201

    def post(self):
        # JSON object from POST request
        new_user_json = request.get_json()
        new_user_email = new_user_json['email']
        new_user_password = new_user_json['password']
        new_user_verified = False

        # Validate if user email exists
        new_user_exists = User.query.filter_by(
            email=new_user_json['email']).first()

        if new_user_exists:
            response = Response(
                response=json.dumps(
                    {'error': 'El usuario ya existe. Por favor, introduce un correo distinto.'}),
                status=201,
                mimetype='application/json')

        # Else, if user doesn't exists...
        else:
            # Create User row with json data
            new_user = User(
                email=new_user_email, password=new_user_password, verified=False)

            # Handle confirm email
            handle_confirm_email(new_user_email)

            # Add new_user to db
            db.session.add(new_user)
            db.session.commit()

            # Create response
            response = Response(
                response=json.dumps(
                    {'success': 'Usuario creado. Tienes 5 minutos para confirmar tu registro en Domogram.'}),
                status=201,
                mimetype='application/json')

        return response


# --- API SERVER ROUTES ---
# Route: Confirm email
@app.route('/api/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=60)

        # Get user row on db and set verified to true
        user_row = User.query.filter_by(email=email).first()
        user_row.verified = True
        db.session.commit()

    except SignatureExpired:
        return '<h1>El link de confirmación ha expirado.</h1>'

    except BadTimeSignature:
        return '<h1>Whoops! No deberías estar aquí.</h1>'

    return """<h1>¡Tu cuenta ha sido confirmada! </h1> 
        <p>Accede a la plataforma de Domogram con tus datos de registro.</p>"""


# --- FUNCTIONS ---
# Handle user exists actions
def handle_signin(user_json, user):
    # Check if password matches
    if user.password == user_json['password'] and user.verified == False:
        response = Response(
            response=json.dumps(
                {'error': 'Estás registrado en Domogram, pero no has activado tu cuenta. ¡Revisa el correo de confirmación!'}),
            status=201,
            mimetype='application/json')

    # Check if password matches
    elif user.password == user_json['password'] and user.verified:
        response = Response(
            response=json.dumps(
                {'success': 'Has iniciado sesión.'}),
            status=201,
            mimetype='application/json')

    # Else if password doesn't matches
    else:
        response = Response(
            response=json.dumps(
                {'error': 'Usuario y/o contraseña no coinciden.'}),
            status=201,
            mimetype='application/json')

    return response


# Handle confirmation of a given email
def handle_confirm_email(email):
    token = s.dumps(email, salt='email-confirm')

    msg = Message('Confirma tu registro en Domogram',
                  sender='domogrambot@gmail.com',
                  recipients=[email])

    link = url_for('confirm_email', token=token, _external=True)

    msg.body = f"""¡Bienvenido a Domogram! Para confirmar tu cuenta, entra al siguiente link de confirmación:\n{link}"""

    mail.send(msg)


# Create API Endpoints
# api.add_resource(SignUp, '/signup')
# api.add_resource(SignIn, '/signin')
