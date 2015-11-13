from app import db

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
