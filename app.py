from email.policy import default
from django.forms import Select
from flask import Flask, render_template, redirect
from graphviz import render
from flask_wtf import FlaskForm, Form
from jsonschema import Validator
from wtforms import DateField, TimeField, IntegerField, SelectField, StringField, FormField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Length
from flask_wtf.csrf import CSRFProtect
import pandas as pd
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import date, time, datetime

script_directory = os.path.dirname(os.path.abspath(__file__))
schedule_data = os.path.join(script_directory, "P:\AA-OCS-Orefield-Schedule\AA-OCSII-MITCHELL Schedule\OCSII MITCHELL-I-0 SCHEDULE JUNE 2022.xlsm")
done_data = os.path.join(script_directory, "../done/Schedule1.xlsx")

df = pd.read_excel(schedule_data, sheet_name="DropDownFields")
df = df.dropna(subset=['Carrier List'])
c = df['Carrier List'].tolist()
def convert(set):
    return sorted(set)

CARRIER_LIST = convert(c)

app = Flask(__name__)
app.config.update(
    SECRET_KEY="secret_sauce"
)

db_name = 'rework.db'

app.config.update(
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_name,
    SQLALCHEMY_TRACK_MODIFICATIONS = True
)

csrf = CSRFProtect(app)
csrf.init_app(app)

db = SQLAlchemy(app)

SHIPPING_NAMES = ["Carolina Dairy", "Duboise", "Fort Worth", "Minster", 
            "MWDC", "Schreiber", "West Jordan"]

STATUS_CHOICES = ["Live", "Drop"]

class Load_Orders(Form):
    id_field = HiddenField()
    DateShipped = DateField("Date Shipped", [ InputRequired() ], format='%m/%d/%Y')
    shipping = SelectField("Shipping Location", choices=SHIPPING_NAMES)
    carrier = SelectField("Carrier Name", choices=CARRIER_LIST)
    status = SelectField("Status", choices=STATUS_CHOICES)
    load = StringField("Load Number", [ InputRequired() , Length(min=10, max=15, message="Invalid Range")])
    trailer = StringField("Trailer Number")
    appointmentDate = DateField("Appointment Date", format='%m/%d/%Y')
    appointmentTime = TimeField("Appointment Time", format="hh:mm")
    cases = IntegerField("Cases Reworked", default=0)
    pallets = IntegerField("Pallets Reworked", default=0)


class MyForm(FlaskForm):
    carrier = FormField(Load_Orders)


@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/form", methods=('GET', 'POST'))
def input_form():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template("form.html", form=form)

@app.route("/success", methods=["GET", "POST"])
def success():
    form = MyForm()
    if form.validate_on_submit():
        return f'<h1> Welcome {form.carrier.data} </h1>'
    return render_template('form.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)