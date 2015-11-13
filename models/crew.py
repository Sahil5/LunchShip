from app import db


class Crew(db.Model):
    ship_id = db.Column(db.Integer, db.ForeignKey('ship.id'), primary_key=True)
    sailor_id = db.Column(db.String(128), primary_key=True)

    def __init__(self, ship_id, sailor_id):
        self.ship_id = ship_id
        self.sailor_id = sailor_id

    def __repr__(self):
        return '<Crew(ship_id=%d, sailor_id=%s)>' % (self.ship_id, self.sailor_id)
