from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/rexcolt/GitHub/DomogramApp/DomogramMobileAPI/database.db'
db = SQLAlchemy(app)


# --- DB Table - User ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(15), unique=True)


if __name__ == '__main__':
    app.run(debug=True)
