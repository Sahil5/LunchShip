from app import db
import datetime
import time

from models.ship import Ship
from models.crew import Crew

def create_ship(captain_id, destination, departure_time, crew):
    new_ship = Ship(captain_id, destination, departure_time)
    db.session.add(new_ship)
    db.session.commit()

    crew = [crew_member.strip() for crew_member in crew.split(',')]
    for crew_member in crew:
        new_crew_member = Crew(new_ship.id, crew_member)
        db.session.add(new_crew_member)
    db.session.commit()


def get_all_sailing_ships():
    all_ships = db.session.query(Ship).all()
    sailing_ships = []
    for ship in all_ships:
        if time.mktime(ship.departure_time.timetuple()) >= time.mktime(datetime.datetime.now().timetuple()):
            sailing_ships.append(ship)
    return sailing_ships


def get_all_sailing_crews(ship_map):
    all_crews = db.session.query(Crew).all()
    sailing_crews = []
    for crew in all_crews:
        if crew.ship_id in ship_map:
            sailing_crews.append(crew)
    return sailing_crews
