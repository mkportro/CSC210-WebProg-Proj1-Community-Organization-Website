from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import MetaData
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///community.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# DB Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    events = db.relationship('Event', secondary='user_events', backref='users')


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(500), nullable=False)


class UserEvents(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)


with app.app_context():
    # create db tables
    db.create_all()
        
    # read events from JSON, create Event objs if they don't exist
    with open('events.json', 'r') as f:
        events = json.load(f)

    for event in events:
        if not db.session.query(Event).filter_by(title=event['title']).first():
            new_event = Event(
                title = event['title'],
                location = event['location'],
                description = event['description'],
                date = event['date'],
                time = event['time']
            )
            db.session.add(new_event)
    db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Forms
class SignupForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Login')


# Routes
@app.route('/')
def home():
    events = db.session.query(Event).all()
    return render_template('home.html', events=events)


@app.route('/event/<int:event_id>/delete')
@login_required
def delete_event(event_id):
    event = Event.query.get(event_id)
    if event in current_user.events:
        db.session.add(event) #add event to session
        current_user.events.remove(event)
        db.session.commit()
        flash('Event deleted successfully!', 'success')
    return redirect(url_for('profile'))


@app.route('/event/<int:event_id>/register')
@login_required
def register_event(event_id):
    event = Event.query.get(event_id)
    if event and event not in current_user.events:
        current_user.events.append(event)
        db.session.commit()
        flash('Registered for event successfully!', 'success')
    return redirect(url_for('home', event=event, event_id=event_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please try again.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(username=current_user.username).first()
    # events = user.events.all()
    events = user.events
    return render_template('profile.html', user=user, events=events)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)