from app import db

from models.ship import Ship
from models.crew import Crew


def create_ship(captain_id, destination, departure_time):
    new_ship = Ship(captain_id, destination, departure_time)
    db.session.add(new_ship)
    db.session.commit()
