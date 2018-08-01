from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
import os
from data import Rules
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, IntegerField, PasswordField, SelectField, validators
from flask_bcrypt import Bcrypt
from functools import wraps
import requests
import json
import geocoder
import time
from datetime import datetime, timedelta
import math

app = Flask(__name__)
app.debug = False
app.config['SECRET_KEY'] = '12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mrmeteo2.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#add Database Views
class Posts(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    create_date = db.Column(db.DateTime, nullable=False)

class Rules(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(50), nullable=False)
    advice = db.Column(db.Text, nullable=False)
    weather = db.Column(db.String(50), nullable=False)
    weather_condition = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime, nullable=False)

class Users(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False)



#Index
@app.route('/', methods=['GET', 'POST'])
def index():
    g = geocoder.ip('me')
    lat = str(g.lat)
    lon = str(g.lng)
    url = 'https://api.openweathermap.org/data/2.5/forecast?lat=12.3657&lon=-1.5339&units=metric&appid=454d3e3138f204980589ae958b2a9728'
    # url = 'https://api.openweathermap.org/data/2.5/forecast?lat=' + lat + '&lon=' + lon + '&units=metric&appid=454d3e3138f204980589ae958b2a9728'
    result = requests.get(url).json()
    all_data = result['list']

    weather = {}
    weather[0] = result['city']
    for data in all_data:
        dayUnix = data['dt']
        round = data['main']['temp']
        data['main']['temp'] = math.ceil(round)
        date = datetime.fromtimestamp(dayUnix)
        s = datetime.now() + timedelta(days=1)
        x = datetime.now() + timedelta(days=2)
        y = datetime.now() + timedelta(days=3)
        z = datetime.now() + timedelta(days=4)
        if s > date < x:
            ts = time.gmtime(dayUnix)
            day_of_week = time.strftime("%A", ts)
            data['dt'] = day_of_week
            weather[1] = data
        if  s < date < x:
            ts = time.gmtime(dayUnix)
            day_of_week = time.strftime("%A", ts)
            data['dt'] = day_of_week
            weather[2] = data
        if  s < date < y:
            ts = time.gmtime(dayUnix)
            day_of_week = time.strftime("%A", ts)
            data['dt'] = day_of_week
            weather[3] = data
        if  s < date < z:
            ts = time.gmtime(dayUnix)
            day_of_week = time.strftime("%A", ts)
            data['dt'] = day_of_week
            weather[4] = data


    rules = Rules.query.all()
    crop = request.form.get("selected_crop")

    context = {
            'weather': weather,
            'rules': rules,
            'crop': crop,
            }

    return render_template('home.html', context=context)

#VoiceEnglish
@app.route('/voice', methods=['GET', 'POST'])
def voice():
    url = 'https://api.openweathermap.org/data/2.5/forecast?lat=12.3657&lon=-1.5339&units=metric&appid=454d3e3138f204980589ae958b2a9728'
    result = requests.get(url).json()
    all_data = result['list']

    weather = {}
    weather[0] = result['city']
    for data in all_data:
        dayUnix = data['dt']
        round = data['main']['temp']
        data['main']['temp'] = math.ceil(round)
        date = datetime.fromtimestamp(dayUnix)
        s = datetime.now() + timedelta(days=1)
        x = datetime.now() + timedelta(days=2)
        y = datetime.now() + timedelta(days=3)
        z = datetime.now() + timedelta(days=4)
        if s > date < x:
            ts = time.gmtime(dayUnix)
            day_of_week = time.strftime("%A", ts)
            data['dt'] = day_of_week
            weather[1] = data
        if  s < date < x:
            ts = time.gmtime(dayUnix)
            day_of_week = time.strftime("%A", ts)
            data['dt'] = day_of_week
            weather[2] = data
        if  s < date < y:
            ts = time.gmtime(dayUnix)
            day_of_week = time.strftime("%A", ts)
            data['dt'] = day_of_week
            weather[3] = data
        if  s < date < z:
            ts = time.gmtime(dayUnix)
            day_of_week = time.strftime("%A", ts)
            data['dt'] = day_of_week
            weather[4] = data


    rules = Rules.query.all()
    posts = Posts.query.all()

    context = {
            'weather': weather,
            'rules': rules,
            'posts': posts,
            }
    return render_template('voice.xml', context=context)

#VoiceFrench
@app.route('/voice_french')
def voice_french():
    return render_template('voice_french.xml')

#About
@app.route('/about')
def about():
    return render_template('about.html')

#Posts Page
@app.route('/posts')
def posts():
        #get posts
        posts = Posts.query.all()

        if len(posts) > 0:
            return render_template('posts.html', posts=posts)
        else:
            msg = 'No Posts Found'
            return render_template('posts.html', msg=msg)


#Single post
@app.route('/post/<string:id>/')
def post(id):

    #get post
    post = Posts.query.filter_by(id=id).one()

    return render_template('post.html', post=post)

#Registration form class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
        ])
    confirm = PasswordField('Confirm Password')

#User Register
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        #execute commands
        user = Users(name=name, email=email, username=username, password=hashed_password, create_date=datetime.now())
        db.session.add(user)
        db.session.commit()

        flash('You are now registered and can log in', 'success')

        redirect(url_for('index'))
    return render_template('add_user.html', form=form)

#User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user.id > 0:
            #compare passwords
            if user and bcrypt.check_password_hash(user.password, password_candidate):
             #Passed
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('index'))
            else:
                error = 'Wrong Password. Please Try Again'
                return render_template('login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

#Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unathorized! Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

#Manage Posts
@app.route('/manage_posts')
@is_logged_in
def manage_posts():
    #get posts
    posts = Posts.query.all()

    if len(posts) > 0:
        return render_template('manage_posts.html', posts=posts)
    else:
        msg = 'No Posts Found'
        return render_template('manage_posts.html', msg=msg)

#Manage user
@app.route('/users')
@is_logged_in
def users():

    #get users
    users = Users.query.all()

    if len(users) > 0:
        return render_template('users.html', users=users)
    else:
        msg = 'No Users Found'
        return render_template('users.html', msg=msg)


#Add new Post form
class PostForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])

#Add Post
@app.route('/add_post', methods=['POST', 'GET'])
@is_logged_in
def add_post():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        post = Posts(title=title, body=body, create_date=datetime.now())
        db.session.add(post)
        db.session.commit()
        flash('New Post Created', 'success')

        return redirect(url_for('posts'))

    return render_template('add_post.html', form=form)

#Add new Rule
class RuleForm(Form):
    variable = IntegerField('Input the value', [validators.NumberRange(min=1)])
    advice = TextAreaField('Give an Advice or Information', [validators.Length(min=20)])
    crop = SelectField('Select a Crop', choices=[(' ', ' '), ('sorghum', 'Sorghum'), ('maize', 'Maize')], validators=[validators.DataRequired()] )
    weather = SelectField('Select a weather condition', choices=[(' ', ' '), ('wind', 'Wind'), ('temperature', 'Temperature')], validators=[validators.DataRequired()] )
    weather_condition = SelectField('Select value as greater-than, less-than or equals-to', choices=[(' ', ' '), ('less than', 'less than'), ('greater than', 'greater than'), ('equals to', 'equals to')], validators=[validators.DataRequired()] )

#Add Rule
@app.route('/add_rule', methods=['POST', 'GET'])
@is_logged_in
def add_rule():
    form = RuleForm(request.form)
    if request.method == 'POST' and form.validate():
        crop = form.crop.data
        advice = form.advice.data
        weather = form.weather.data
        weather_condition = form.weather_condition.data
        value = form.variable.data

        #add rule to DB
        rule = Rules(crop=crop, advice=advice, weather=weather, weather_condition=weather_condition, value=value, create_date=datetime.now())
        db.session.add(rule)
        db.session.commit()

        flash('New Rule Added', 'success')

        return redirect(url_for('index'))

    return render_template('new_rule.html', form=form)

#Manage Rules
@app.route('/manage_rules')
@is_logged_in
def manage_rules():

    #get rules
    rules = Rules.query.all()

    if len(rules) > 0:
        return render_template('manage_rules.html', rules=rules)
    else:
        msg = 'No Rules Found'
        return render_template('manage_rules.html', msg=msg)


# #Edit post
@app.route('/edit_post/<string:id>', methods=['POST', 'GET'])
@is_logged_in
def edit_post(id):

        post = Posts.query.filter_by(id=id).one()

        #get form
        form = PostForm(request.form)

        #ppulate post form fields
        form.title.data = post.title
        form.body.data = post.body

        if request.method == 'POST' and form.validate():
            post.title = request.form['title']
            post.body = request.form['body']

            db.session.commit()

            flash('Post Updated', 'success')

            return redirect(url_for('posts'))

        return render_template('edit_post.html', form=form)


# #Edit Rule
@app.route('/edit_rule/<string:id>', methods=['POST', 'GET'])
@is_logged_in
def edit_rule(id):

        rule = Rules.query.filter_by(id=id).one()

        #get form
        form = RuleForm(request.form)


        if request.method == 'POST' and form.validate():
            rule.crop = request.form['crop']
            rule.advice = request.form['advice']
            rule.weather = request.form['weather']
            rule.weather_condition = request.form['weather_condition']
            rule.value = request.form['variable']

            db.session.commit()

            flash('Rule Updated', 'success')

            return redirect(url_for('manage_rules'))

        return render_template('edit_rule.html', form=form)



#LogOut
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out!', 'success')
    return redirect(url_for('login'))




if __name__ == '__main__':
    	port = int(os.environ.get('PORT', 5000))
    	app.run(host='0.0.0.0', port=port)
