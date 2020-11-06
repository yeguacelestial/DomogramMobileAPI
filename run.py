from flask_restful import Api
from app import app, SignUp, SignIn

# Microservices
from registro_dispositivos import DispositivosList, Dispositivo


api = Api(app)

api.add_resource(SignUp, '/signup')
api.add_resource(SignIn, '/signin')
api.add_resource(DispositivosList, '/dispositivos')
api.add_resource(Dispositivo, '/dispositivo/<string:identificador>')


app.run(debug=True)
