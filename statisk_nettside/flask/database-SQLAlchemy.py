from flask.ext.sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()

class Bruker(db.Model):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fornavn = db.Column(db.String(32))
    etternavn = db.Column(db.String(32))
    email = db.Column(db.String(50))
    passord = db.Column(db.String(30))
    email = db.Column(db.String(50), unique=True, index=True)
    dato_registrert = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__ (self, fornavn, etternavn, email, passord):
        self.fornavn = fornavn
        self.etternavn = etternavn
        self.passord = passord
        self.email = email

class Konto(db.Model):
    konto_nummer = db.Column(db.String(), unique=True)
    f_uttak = db.Column(db.String())

    def __init__(self, konto_nummer, f_uttak):
        self.konto_nummer = konto_nummer
        self.f_uttak = f_uttak

db.create_all()


