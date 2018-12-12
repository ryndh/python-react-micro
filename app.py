from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kgiwkefesonugp:57e3f0bab3cb23d1f88375c351616ddd83e70b34c721785cc380c150a0ad16be@ec2-184-72-239-186.compute-1.amazonaws.com:5432/dfasnfr84q1b8j'

db=SQLAlchemy(app)

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    rating = db.Column(db.Integer)

    def __init__(self, title, rating):
        self.rating = rating
        self.title = title
    
    def __repr__(self):
        return '<Title %r>' % self.title

@app.route('/')
def home():
    return '<h1>Hello</h1>'

@app.route('/movies_input', methods=['POST'])
def movies_input():
    if request.content_type == 'application/json':
        post_data = request.get_json()
        title = post_data.get('title')
        rating = post_data.get('rating')
        reg = Movie(title, rating)
        db.session.add(reg)
        db.session.commit()
        return jsonify('data posted')
    return jsonify('')

@app.route('/return_movies', methods=['GET'])
def movies_return():
    if request.method == 'GET':
        all_movies = db.session.query(Movie.title, Movie.rating).all()
        return jsonify(all_movies)


if __name__ == '__main__':
    app.debug = True
    app.run()

