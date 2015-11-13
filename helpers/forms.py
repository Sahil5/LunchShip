from flask_wtf import Form
from wtforms import StringField
from wtforms import Form, PasswordField, TextField, validators

from helpers.fields import LunchTimeField


class CreateLunchShip(Form):
    departure_time = LunchTimeField('Departure Time')
    destination = TextField('Destination', [validators.input_required()])
    crew = TextField('Crew')


class AddShip(Form):
    captain = TextField('Captain')
    departure_time = LunchTimeField('Departure Time')
    destination = TextField('Destination', [validators.input_required()])


class LoginForm(Form):
    username = TextField('Username', [validators.input_required()])
    password = PasswordField('Password', [validators.input_required()])
