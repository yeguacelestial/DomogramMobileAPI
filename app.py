import json

# Import models
from models import User, db, app

# Flask
from flask import Flask, request, Response, jsonify
from flask_restful import Resource, Api


# Initializing Flask API
api = Api(app)


# SignIn endpoint
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
                        {'success': 'Usuario autenticado con exito.'}),
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


# SignUp endpoint
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


# Create endpoints, and associate them with created classes
api.add_resource(SignUp, '/signup')
api.add_resource(SignIn, '/signin')


if __name__ == '__main__':
    app.run(debug=True)
