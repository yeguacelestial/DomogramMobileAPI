import os
import json
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv

from flask import Flask, request, Response, jsonify
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

# Initializing Flask API
api = Api(app)

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
            # Check if password matches
            if user.password == user_json['password']:
                response = Response(
                    response=json.dumps(
                        {'success': 'Has iniciado sesión.'}),
                    status=201,
                    mimetype='application/json')

                return response

        # Else if password doesn't match
        response = Response(
            response=json.dumps(
                {'error': 'Usuario y/o contraseña no coinciden.'}),
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
            new_user_json = User(
                email=new_user_json['email'], password=new_user_json['password'])

            # Add new_user to db
            db.session.add(new_user_json)
            db.session.commit()

            # Create response
            response = Response(
                response=json.dumps(
                    {'success': 'Usuario creado con éxito.'}),
                status=201,
                mimetype='application/json')

        return response


# --- API SERVER ROUTES ---
# Route: Confirm email
@app.route('/api/confirm_email/<token>')
def confirm_email(token):
    email = s.loads(token, salt='email-confirm', max_age=60)
    return 'Tu registro fue confirmado.'


# --- FUNCTIONS ---
# Generate a token with a given email
def generate_token(email):
    token = s.dumps(email, salt='email-confirm')
    return token


# API Endpoints
api.add_resource(SignUp, '/signup')
api.add_resource(SignIn, '/signin')


if __name__ == '__main__':
    app.run(debug=True)
