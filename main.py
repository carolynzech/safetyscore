from flask import Flask, request, render_template, redirect, session
from database_functions import addUser, addPlace, getPlace
app = Flask(__name__)

#a randomly generated key to encrypt the session cookies, will change later
app.secret_key = b'\xfe\x14\x07-#\x1a\x7f\xbe#PG\xd0\x8eo\x1ea'

#default page
@app.route('/')
def hello_world():
    return 'Hello, World!'

#login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        return render_template('home.html')
    elif request.method=='GET':
        return render_template('login.html')

#home page, where you can submit the ratings?
@app.route('/home')
def home():
    return render_template('home.html')

#place where ratings will post request to
@app.route('/addPlace', methods=['POST'])
def addPlace():
    placeName = request.form['name']
    masksRating = request.form['masks']
    distancingRating = request.form['distancing']
    outdoorRating = request.form['outdoor']
    capacityRating = request.form['capacity']
    contactRating = request.form['contact']

    session['places'] = [
        {'name': placeName, 
        'masksRating': masksRating, 
        'distancingRating': distancingRating, 
        'outdoorRating': outdoorRating,
        'capacityRating': capacityRating,
        'contactRating': contactRating
        }]
    return redirect('/home')