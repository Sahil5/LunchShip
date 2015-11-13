from app import db
import datetime

from models.ship import Ship
from models.crew import Crew
from sqlalchemy.orm import joinedload


def create_ship(captain_id, destination, departure_time):
    new_ship = Ship(captain_id, destination, departure_time)
    db.session.add(new_ship)
    db.session.commit()

    db.session.add(Crew(new_ship.id, captain_id))
    db.session.commit()


def get_all_sailing_ships():
    return db.session.query(
        Ship
    ).options(
        joinedload('crew')
    ).filter(
        Ship.departure_time > datetime.datetime.now()
    ).order_by(
        Ship.departure_time.desc()
    ).all()
