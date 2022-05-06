from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.debug = True
 
# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evaccenter.db'
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

class Evaccenter(db.Model):
    evaccenter_id = db.Column(db.Integer, primary_key=True)
    evac_num = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(6))
    # Relationships
    evacuees = db.relationship('Evacuee', backref='evaccenter', lazy=True)
   
    def __repr__(self):
        return f'Evaccenter("{self.name}","{self.city}",{self.state})'

class Evacuee(db.Model):
    EvacueeId = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(150))
    dob = db.Column(db.String(10))
    age = db.Column(db.Integer)
    phone_number = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200), unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #Foreign Keys
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.evaccenter_id'))
    # Relationships
    evacuee_emergency_contacts = db.relationship('EvacueeEmergencyContact', backref='evacuee', lazy=True)
    # One-to-one relationships
    evacuee_address = db.relationship('EvacueeAddress', backref='evacuee', uselist=False)

    def __repr__(self):
        return f'Evacuee("{self.EvacueeId}","{self.name}","{self.dob}","{self.age}","{self.phone_number}",{self.email})'

class EvacueeAddress(db.Model):
    evacuee_address_id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.String(5), nullable=False)
    #Foreign Keys
    EvacueeId = db.Column(db.Integer, db.ForeignKey('evacuee.EvacueeId'))

    def __repr__(self):
        return f'EvacueeAddress("{self.evacuee_address_id}","{self.street}",{self.city})'

class EvacueeEmergencyContact(db.Model):
    evacuee_emergency_contact_id = db.Column(db.Integer, primary_key=True)
    evacuee_emergency_number = db.Column(db.String(10), nullable=False)
    contact_name = db.Column(db.String(150), nullable=False)
    emergency_contact_relation = db.Column(db.String(50))
    # Foreign Keys
    EvacueeId = db.Column(db.Integer, db.ForeignKey('evacuee.EvacueeId'), nullable=False)

    def __repr__(self):
        return f'EvacueeEmergencyContact("{self.evacuee_emergency_contact_id}","{self.evacuee_emergency_number}","{self.contact_name}",{self.emergency_contact_relation})'

if __name__ == '__main__':
    app.run()