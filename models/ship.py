from app import db
from sqlalchemy.orm import relationship


class Ship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    captain_id = db.Column(db.String(128))
    destination = db.Column(db.String(64))
    time_created = db.Column(db.DateTime)
    departure_time = db.Column(db.DateTime)

    crew = relationship("Crew", backref="ship")

    def __init__(self, captain_id, destination, departure_time):
        self.captain_id = captain_id
        self.destination = destination
        self.departure_time = departure_time

    def __repr__(self):
        return '<Ship(id=%d, destination=%s)>' % (self.id, self.destination)
