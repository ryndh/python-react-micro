from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = ''

@app.route('/')
def home():
    return '<h1>Hello</h1>'

if __name__ == '__main__':
    app.debug = True
    app.run()

