from flask_wtf import Form
from wtforms import StringField
from wtforms import Form, TextField, validators

class CreateLunchShip(Form):
    departure_time = TextField('Departure Time', [validators.Length(min=1, max=8)])
    destination = TextField('Destination', [validators.Length(min=6, max=35)])
    crew = TextField('Crew', [validators.Length(min=5, max=40)])