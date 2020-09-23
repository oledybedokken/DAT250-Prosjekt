import os
from datetime import datetime
from forms import  OpprettForm, InnloggingForm, DREP___MEGG, InnskuddForm, OverforingForm, SlettForm
from flask import Flask, session, render_template, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config["SECRET_KEY"] = "admin"
db = SQLAlchemy(app)

class Bruker(db.Model):

    __tablename__ = "bruker"
    id = db.Column(db.Integer, primary_key = True)
    navn = db.Column(db.String(64), unique=True)
    passord = db.Column(db.Text)
    belop = db.Column(db.Float)
    aktiv = db.Column(db.Boolean, default=True)

    def innskudd_uttak(self, type, belop):
        if type == "uttak":
            belop *= -1
        if self.saldo + belop < 0:
            return False
        else:
            self.saldo += belop
            return True

    def __init__(self, navn, passord, saldo=0):
        self.navn = navn
        self.passord = generate_password_hash(passord)
        self.saldo = saldo

    def __repr__(self):
        return f"Kontonavn er {self.navn} med kontonummer {self.id}"

class Transaksjon(db.Model):

    __tablename__ = "transaksjon"
    id = db.Column(db.Integer, primary_key = True)
    transaksjon_type = db.Column(db.Text) # Gave/Lønn/Betaling
    beskrivelse = db.Column(db.Text)
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    bruker_id = db.Column(db.Integer,db.ForeignKey("bruker_id"), nullable=False)
    konto = db.relationship("Konto", backref=db.backref("transaksjon", lazy=True))

    def __init__(self,transaksjon_type, beskrivelse, bruker_id, amount=0):
        self.transaksjon_type = transaksjon_type
        self.beskrivelse = beskrivelse
        self.bruker_id = bruker_id
        self.amount = amount

    def __repr__(self):
        return f"Transaksjon {self.id}: {self.transaksjon_type} on {self.date}"


@app.route("/")
def konto():
    return render_template("Konto.html")

@app.errorhandler(404)
def feilmelding(e):
    return render_template("404.html"), 404

@app.route("/skap_brukskonto", methods=["GET", "POST"])
def skap_brukskonto():
    form = OpprettForm()

    if form.validate_on_submit():
        navn = form.navn.data
        passord = form.password.data
        if form.saldo.data > 0:
            saldo = form.saldo.data
        else:
            saldo = 0

        # Add new bank account to database
        ny_bankkonto = Account(passord, saldo)
        db.session.add(ny_bankkonto)
        db.session.commit()
        ny_transaksjon = Transaksjon("innskudd", "kontoapning", ny_bankkonto.id, saldo)
        db.session.add(ny_transaksjon)
        db.session.commit()

        return redirect(url_for("Konto"))

    return render_template("skap_brukskonto.html", form=form)

@app.route("/innlogging", methods=["GET", "POST"])
def innlogging():
    form = InnloggingForm()

    if form.validate_on_submit():
        id = form.id.data
        passord = form.passord.data
        konto = Account.query.get(id)
        if check_password_hash(konto.passord, passord):
            return redirect(url_for("Konto"))
        else:
            return "<h1>Ugyldig kontonummer & passord</h1>"

    return render_template("Login.html", form=form)

@app.route("/avlogging", methods=["GET"])
def avlogging():
    session["email"] = None
    return redirect(url_for("Login"))
