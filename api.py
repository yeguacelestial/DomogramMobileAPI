# Import models
from models import User, db, app

# Flask
from flask import Flask, request
from flask_restful import Resource, Api


# Initializing Flask API
api = Api(app)


# Handling HTTP requests of class 'Hello world'
class HelloWorld(Resource):
    def get(self):
        return {'about': 'Hello world'}

    def post(self):
        # Fetch POST request data
        some_json = request.get_json()
        return {'you sent': some_json}, 201


# SignUp Endpoint
class SignUp(Resource):
    def get(self):
        return {'test': 'this is a test'}, 201

    def post(self):
        # JSON object fromm POST request
        json = request.get_json()
        print(json['email'], json['password'])
        # Create User row with json data
        new_user = User(email=json['email'], password=json['password'])

        # Add new_user to db
        db.session.add(new_user)
        db.session.commit()

        return {'aviso': 'nuevo usuario creado'}, 201


# Create endpoints, and associate them with created classes
api.add_resource(HelloWorld, '/')
api.add_resource(SignUp, '/signup')


if __name__ == '__main__':
    app.run(debug=True)
