#imports
from os import name
from flask import Flask, abort, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField, IntegerField
from datetime import date

app = Flask(__name__)

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'Mrenj98r5fckl'

Bootstrap(app)

# db name + config
db_name = 'evaccenter.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

#table from models.py
class Evacuee(db.Model):
    EvacueeId = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(150))
    dob = db.Column(db.String(10))
    age = db.Column(db.Integer)
    phone_number = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200), unique=True)

    def __init__(self, name, dob, age, phone_number, email):
        self.name = name
        self.dob = dob
        self.age = age
        self.phone_number = phone_number
        self.email = email

class AddRecord(FlaskForm):
    # id used only by update/edit
    id_field = HiddenField()
    name = StringField('Evacuee name')
    dob = StringField('DOB')
    age = IntegerField('Age')
    phone_number = StringField('Phone Number')
    email = StringField('Email')
    # updated + submission
    updated = HiddenField()
    submit = SubmitField('Add/Update Record')


#routes for site navigation
@app.route('/')
def index():
    return render_template('index.html')

#selects an evacuee for querying
@app.route('/select_evacuee')
def select_evacuee():
    names = Evacuee.query.with_entities(Evacuee.name).distinct()
    return render_template('select_evacuee.html', names=names)

#adds evacuee to database
@app.route('/form', methods=['GET', 'POST'])
def form():
    form = AddRecord()
    if form.validate_on_submit():
        name = request.form['name']
        dob = request.form['dob']
        age = request.form['age']
        phone_number = request.form['phone_number']
        email = request.form['email']
        # the data to be inserted
        record = Evacuee(name, dob, age, phone_number, email)
        # Add record
        db.session.add(record)
        db.session.commit()
        return render_template('form.html', form=form)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form, field).label.text,
                    error
                ), 'error')
        return render_template('form.html', form=form)

#runs query for all evacuee names
@app.route('/inventory/<name>')
def inventory(name):
    try:
        evacuees = Evacuee.query.filter_by(name=name).order_by(Evacuee.EvacueeId).all()
        return render_template('list.html', evacuees=evacuees, name=name)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something went wrong.</h1>'
        return hed + error_text
   
#run app
if __name__ == '__main__':
    app.run(debug=True)