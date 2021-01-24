#!/usr/bin/python3.9

from flask import Flask, request, render_template, redirect, session, url_for
from database_functions import addUser, checkUser, addPlace, getPlace, updatePlace, getAllPlaces
app = Flask(__name__)

#a randomly generated key to encrypt the session cookies, will change later
app.secret_key = b'\xfe\x14\x07-#\x1a\x7f\xbe#PG\xd0\x8eo\x1ea'

#default page
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/map')
def map():
    if session.get('lat') and session.get('lng'):
        lat = session['lat']
        lng = session['lng']
    else:
        lat = 41.8268
        lng = -71.4025
    return render_template('map.html', data=getAllPlaces(), lat=lat, lng=lng)

#signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        
        addUser(username, password)
        session['username'] = username
        return redirect(url_for('map'))
        # else:
        #    return render_template('signup.html') 
    elif request.method=='GET':
        return redirect(url_for('signup'))


    elif request.method=='GET':
        return render_template('login.html')
#login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        
        if checkUser(username, password):
            session['username'] = username
            return redirect(url_for('map'))
        else:
           return redirect(url_for('login'))


    elif request.method=='GET':
        return render_template('login.html')

#home page, where you can submit the ratings?
@app.route('/rate')
def rate():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    name = request.args.get('name')

    session['lat'] = lat
    session['lng'] = lng
    session['placeName'] = name
    print(session['lat'], session['lng'], session['placeName'])

    return render_template('covid-rater.html')

#place where ratings will post request to
@app.route('/addPlaceForm', methods=['POST'])
def addPlaceForm():
    masksRating = int(request.form.get('masks-star'))
    distancingRating = int(request.form.get('distancing-star'))
    outdoorRating = int(request.form.get('outdoor-star'))
    capacityRating = int(request.form.get('contactless-star'))
    contactRating = int(request.form.get('capacity-star'))
    tempRating = int(request.form.get('temp-star'))

    name = session['placeName']
    lat = session['lat']
    lng = session['lng']

    print(masksRating, distancingRating, outdoorRating, capacityRating, contactRating, tempRating, name, lat, lng)

    if getPlace(name) == None:
        addPlace(name, masksRating, distancingRating, outdoorRating, capacityRating, contactRating, lat, lng)
    else:
        updatePlace(name, masksRating, distancingRating, outdoorRating, capacityRating, contactRating, lat, lng)
    return redirect('map')
    
@app.route('/newPlace')
def newPlace():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    session['lat'] = lat
    session['lng'] = lng

    print(session['lat'])
    print(session['lng'])

    return render_template('newPlace.html')

@app.route('/newPlaceName', methods=['POST'])
def newPlaceName():
    if request.method=='POST':
        name = request.form['placeName']
        lat = session['lat']
        lng = session['lng']

        return redirect('rate?name=' + name + "&lat=" + lat + "&lng=" + lng)
        #return redirect(url_for('rate', placeName=name, lat=lat, lng=lng, **request.args))

