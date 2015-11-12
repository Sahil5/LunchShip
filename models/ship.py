from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Ship(db.Model):
    id = db.Column(db.Integer(11), primary_key=True)
    captain_id = db.Column(db.String(128))
    destination = db.Column(db.String(64))
    time_created = db.Column(db.DateTime)
    departure_time = db.Column(db.DateTime)

    def __init__(self, captain_id, destination):
        self.captain_id = captain_id
        self.destination = destination

    def __repr__(self):
        return '<Ship(id=%d, destination=%s)>' % (self.id, self.destination)