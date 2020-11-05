import markdown
import os
import shelve

from flask import Flask, g
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)

# Initializing Flask API
api = Api(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("devices.db")
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    """ Present some documentation """

    # Open README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Read file content
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)


class DispositivosList(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        devices = [shelf[key] for key in keys]

        return {'message': 'Success', 'data': devices}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('identificador', required=True)
        parser.add_argument('nombre', required=True)
        parser.add_argument('tipo_dispositivo', required=True)
        parser.add_argument('pin_dispositivo', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        shelf = get_db()
        shelf[args['identificador']] = args

        return {'message': 'Dispositivo registrado', 'data': args}, 201


class Dispositivo(Resource):
    def get(self, identificador):
        shelf = get_db()

        # If the key doesn't exist in the data store, return 404
        if not (identificador in shelf):
            return {'message': 'Dispositivo no encontrado'}, 404

        return {'message': 'Dispositivo encontrado', 'data': shelf[identificador]}, 200

    def delete(self, identificador):
        shelf = get_db()

        # If the key doesn't exist in the data store, return 404
        if not (identificador in shelf):
            return {'message': 'Dispositivo no encontrado'}, 404

        del shelf[identificador]
        return '', 204


api.add_resource(DispositivosList, '/dispositivos')
api.add_resource(Dispositivo, '/dispositivo/<string:identificador>')
