from collections import namedtuple

LunchShip = namedtuple('LunchShip', [
	'time_created',
	'departure_time',
	'destination',
	'crew'
])

dummy_time = [
	{
		'time_created': "2015-11-12 01:10:05",
		'departure_time': "2015-11-12 02:01:05",
		'destination': "McDonalds",
		'crew': "Stella, Ben, Nathan",
	},
	{
		'time_created': "2015-11-12 01:01:05",
		'departure_time': "2015-11-12 03:01:05",
		'destination': "Senior Sisig",
		'crew': "Stella, Nathan",
	},
	{
		'time_created': "2015-11-12 01:01:05",
		'departure_time': "2015-11-12 06:01:05",
		'destination': "McDonalds",
		'crew': "Stella, Ben, Nathan, Matt, Sahil",
	},
]

def get_all_lunch_ship_presenters():
	lunch_ship_presenters = []

	for lunch_ship in dummy_time:
		lunch_ship_presenters.append(LunchShip(
				time_created=lunch_ship['time_created'],
				departure_time=lunch_ship['departure_time'],
				destination=lunch_ship['destination'],
				crew=lunch_ship['crew']
			)
		)
	return lunch_ship_presenters
