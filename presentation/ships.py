from collections import namedtuple
from flask import session
from logic import get_all_sailing_ships
from logic import get_all_sailing_crews

from models.ship import Ship
from models.crew import Crew

LunchShip = namedtuple('LunchShip', [
	'is_captain',
	'captain_id',
	'time_created',
	'departure_time',
	'destination',
	'crew'
])

def get_all_lunch_ship_presenters():
	ships = get_all_sailing_ships()

	ship_map = {}
	for ship in ships:
		ship_map[ship.id] = LunchShip(
								is_captain=session["username"] == ship.captain_id,
								captain_id=ship.captain_id,
								time_created=ship.time_created,
								departure_time=ship.departure_time,
								destination=ship.destination,
								crew=[],
							)

	crews = get_all_sailing_crews(ship_map)

	for crew in crews:
		presenter = ship_map[crew.ship_id]
		presenter.crew.append(crew.sailor_id)

	return [ship_map[ship_id] for ship_id in ship_map.keys()]
