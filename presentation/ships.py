from collections import namedtuple
import datetime
import time
from app import db

from models.ship import Ship
from models.crew import Crew

LunchShip = namedtuple('LunchShip', [
	'captain_id',
	'time_created',
	'departure_time',
	'destination',
	'crew'
])

def get_all_lunch_ship_presenters():
	ships = db.session.query(Ship
		).all()

	ship_map = {}
	for ship in ships:
		ship_map[ship.id] = LunchShip(
								captain_id=ship.captain_id,
								time_created=ship.time_created,
								departure_time=ship.departure_time,
								destination=ship.destination,
								crew=[],
							)

	crews = db.session.query(Crew
		).filter(Crew.ship_id in ship_map
		).all()

	for crew in crews:
		presenter = ship_map[crew.ship_id]
		presenter.crew.append(crew.sailor_id)

	return [ship_map[ship_id] for ship_id in ship_map.keys()]
