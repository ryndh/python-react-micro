from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku
from bs4 import BeautifulSoup as BS
import requests
import regex as RE


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kgiwkefesonugp:57e3f0bab3cb23d1f88375c351616ddd83e70b34c721785cc380c150a0ad16be@ec2-184-72-239-186.compute-1.amazonaws.com:5432/dfasnfr84q1b8j'

db = SQLAlchemy(app)

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    year = db.Column(db.Integer)

    def __init__(self, title, year):
        self.year = year
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
        user_title_input = post_data.get('title')
        site = requests.get(f"https://www.imdb.com/find?ref_=nv_sr_fn&q={user_title_input.replace(' ', '+')}&s=all")
        soup = BS(site.content, 'html.parser')
        movie = soup.find_all('td', class_='result_text')[0]
        movie_name = movie.find('a').get_text()
        movie_year_initial = movie.get_text().replace(movie_name, '')
        movie_year_parsed = RE.findall('\d+', movie_year_initial)
        if len(movie_year_parsed) > 0:
            verified_movie_year = movie_year_parsed[0]
        else:
            verified_movie_year = 0
        reg = Movie(movie_name, verified_movie_year)
        db.session.add(reg)
        db.session.commit()
        return jsonify('data posted')
    return jsonify('')

@app.route('/movies_delete', methods=['DELETE'])
def movies_remove():
    if request.content_type == 'application/json':
        post_data = request.get_json()
        movietitle = post_data.get('title')
        obj=Movie.query.filter_by(title=movietitle).first()
        db.session.delete(obj)
        db.session.commit()
        return jsonify('data deleted')
    return jsonify('')

@app.route('/return_movies', methods=['GET'])
def movies_return():
    if request.method == 'GET':
        all_movies = db.session.query(Movie.title, Movie.year).all()
        return jsonify(all_movies)

if __name__ == '__main__':
    app.debug = True
    app.run()

