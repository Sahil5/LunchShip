from collections import namedtuple

LunchShip = namedtuple('LunchShip', [
	'captain_id',
	'time_created',
	'departure_time',
	'destination',
	'crew'
])

dummy_time = [
	{
		'captain_id': 'stella',
		'time_created': "2015-11-12 01:10:05",
		'departure_time': "2015-11-12 02:01:05",
		'destination': "McDonalds",
		'crew': ['Stella', 'Ben', 'Nathan']
	},
	{
		'captain_id': 'stella',
		'time_created': "2015-11-12 01:01:05",
		'departure_time': "2015-11-12 03:01:05",
		'destination': "Senior Sisig",
		'crew': ['Stella', 'Nathan']
	},
	{
		'captain_id': 'ssaini',
		'time_created': "2015-11-12 01:01:05",
		'departure_time': "2015-11-12 06:01:05",
		'destination': "McDonalds",
		'crew': ['Stella', 'Ben', 'Nathan', 'Matt', 'Sahil'],
	},
]

def get_all_lunch_ship_presenters():
	lunch_ship_presenters = []

	for lunch_ship in dummy_time:
		lunch_ship_presenters.append(LunchShip(
				captain_id=lunch_ship['captain_id'],
				time_created=lunch_ship['time_created'],
				departure_time=lunch_ship['departure_time'],
				destination=lunch_ship['destination'],
				crew=lunch_ship['crew']
			)
		)
	return lunch_ship_presenters
