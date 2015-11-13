from flask_wtf import Form
from wtforms import StringField
from wtforms import Form, PasswordField, TextField, validators

from helpers.fields import LunchTimeField


class AddShip(Form):
    captain = TextField('Captain', [validators.optional()])
    departure_time = LunchTimeField('Departure Time')
    destination = TextField('Destination', [validators.input_required()])


class LoginForm(Form):
    username = TextField('Username', [validators.input_required()])
    password = PasswordField('Password', [validators.input_required()])
