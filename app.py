# Import models
from models import User, db, app

# Flask
from flask import Flask, request
from flask_restful import Resource, Api


# Initializing Flask API
api = Api(app)


# Handling HTTP requests of class 'Hello world'
class SignIn(Resource):
    def get(self):
        return {'test': 'this is a test for signin endpoint'}

    def post(self):
        # Filter request data
        json = request.get_json()

        # Validate if user is registered
        user = User.query.filter_by(email=json['email']).first()

        if user:
            # Check if password matches
            if user.password == json['password']:
                return {'aviso': 'Usuario autenticado con exito'}, 201

        return {'error': 'Usuario o contraseña no coinciden.'}, 201


# SignUp Endpoint
class SignUp(Resource):
    def get(self):
        return {'test': 'this is a test for signup endpoint'}, 201

    def post(self):
        # JSON object from POST request
        json = request.get_json()

        # Create User row with json data
        new_user = User(email=json['email'], password=json['password'])

        # Add new_user to db
        db.session.add(new_user)
        db.session.commit()

        return {'aviso': 'nuevo usuario creado'}, 201


# Create endpoints, and associate them with created classes
api.add_resource(SignUp, '/signup')
api.add_resource(SignIn, '/signin')


if __name__ == '__main__':
    app.run(debug=True)
