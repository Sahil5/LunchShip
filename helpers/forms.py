from flask_wtf import Form
from wtforms import StringField
from wtforms import Form, DateTimeField, PasswordField, TextField, validators

class CreateLunchShip(Form):
    departure_time = DateTimeField('Departure Time')
    destination = TextField('Destination', [validators.input_required()])
    crew = TextField('Crew')

class LoginForm(Form):
	username = TextField('Username', [validators.input_required()])
	password = PasswordField('Password', [validators.input_required()])
