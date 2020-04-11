from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

conn_string = os.environ.get('SQLALCHEMY_CONNECTION')

if conn_string is None:
    raise Exception(
        'Please set the "SQLALCHEMY_CONNECTION" environment variable before starting the application')

app.config['SQLALCHEMY_DATABASE_URI'] = conn_string
db = SQLAlchemy(app)


@app.route("/")
def home():
    return "Hello World"


@app.route("/movies", methods=['GET', 'POST', 'PUT'])
def list_movies():
    return "no movies yet"


@app.route("/movies/<movie_id>")
def get_movie(movie_id):
    return f"no movie found with id {movie_id}"


if __name__ == "__main__":
    app.run()
