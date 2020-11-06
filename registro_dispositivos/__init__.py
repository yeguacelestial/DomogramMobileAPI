import os
import time
import shelve

import markdown
import serial

from flask import Flask, g
from flask_restful import Resource, Api, reqparse

from app import app

from .handle_serial import send_serial


puerto = '/dev/ttyACM0'
board = serial.Serial(puerto, 115200)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("devices.db", writeback=True)
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
        parser.add_argument('parametros', type=dict, required=True)

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

        # Sensor - Temperatura y humedad
        if identificador == 'temp-y-humedad':

            print("TEMPERATURA Y HUMEDAD => ")

        return {'message': 'Dispositivo encontrado', 'data': shelf[identificador]}, 200

    def put(self, identificador):
        shelf = get_db()

        # If the key doesn't exist in the data store, return 404
        if not (identificador in shelf):
            return {'message': 'Dispositivo no encontrado'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('identificador', required=False)
        parser.add_argument('nombre', required=False)
        parser.add_argument('tipo_dispositivo', required=False)
        parser.add_argument('pin_dispositivo', required=False)
        parser.add_argument('parametros', type=dict, required=False)

        # Parse the arguments into an object
        args = parser.parse_args()
        new_args = dict(shelf[identificador])  # Copy of current shelf

        if 'dato_serial' in args['parametros']:
            dato_serial = args['parametros']['dato_serial'].encode()
            send_serial(board, args, shelf, identificador, dato_serial)

        for k, v in args.items():
            if v != None:
                new_args[k] = v
                shelf[identificador][k] = new_args[k]

        return {'message': 'Dispositivo actualizado', 'data': shelf[identificador]}, 200

    def delete(self, identificador):
        shelf = get_db()

        # If the key doesn't exist in the data store, return 404
        if not (identificador in shelf):
            return {'message': 'Dispositivo no encontrado'}, 404

        del shelf[identificador]
        return {'message': f'Dispositivo eliminado: {identificador}'}, 204
