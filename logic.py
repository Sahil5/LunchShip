from app import db
import datetime

from models.ship import Ship
from models.crew import Crew
from sqlalchemy.orm import joinedload
from sqlalchemy import func


def create_ship(captain_id, destination, departure_time):
    new_ship = Ship(captain_id, destination, departure_time)
    db.session.add(new_ship)
    db.session.commit()

    db.session.add(Crew(new_ship.id, captain_id))
    db.session.commit()


def join_lunch_ship(ship_id, sailor_id):
    new_crew_member = Crew(ship_id, sailor_id)
    db.session.add(new_crew_member)
    db.session.commit()


def abandon_lunch_ship(ship_id, sailor_id):
    Crew.query.filter_by(ship_id=ship_id, sailor_id=sailor_id).delete()
    db.session.commit()


def get_all_sailing_ships():
    return db.session.query(
        Ship
    ).options(
        joinedload('crew')
    ).filter(
        Ship.departure_time > datetime.datetime.now()
    ).order_by(
        Ship.departure_time.asc()
    ).all()


def get_ships_captained():
    count = func.count(Ship.captain_id)
    return db.session.query(
        count,
        Ship.captain_id,
    ).group_by(
        Ship.captain_id,
    ).order_by(
        count.desc(),
    ).limit(10).all()


def get_ships_crewed():
    count = func.count(Crew.sailor_id)
    return db.session.query(
        Crew.sailor_id,
        count,
    ).group_by(
        Crew.sailor_id,
    ).order_by(
        count.desc(),
    ).limit(10).all()


def get_ship_by_id(ship_id):
    return db.session.query(
        Ship
    ).options(
        joinedload('crew')
    ).filter(
        Ship.id == ship_id
    ).one()


def edit_ship_by_id(ship_id, departure_time, destination):
    db.session.query(
        Ship
    ).filter(
        Ship.id == ship_id
    ).update({
        Ship.departure_time: departure_time,
        Ship.destination: destination,
    })

    db.session.commit()
