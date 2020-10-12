from flask_login import UserMixin, current_user
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import expression
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50),nullable=False)
    fornavn = db.Column(db.String(50),nullable=False)
    etternavn = db.Column(db.String(50),nullable=False)
    postAddresse = db.Column(db.String(50),nullable=False)
    postKode = db.Column(db.String(50),nullable=False)
    fylke = db.Column(db.String(50),nullable=False)
    kjonn = db.Column(db.String(50),nullable=False)
    fodselsdato = db.Column(db.String(50),nullable=False)
    salt = db.Column(db.String(50))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trans_type = db.Column(db.String(50), nullable=False)
    verdi = db.Column(db.Integer, nullable = False)
    avsender = db.Column(db.Integer, nullable = False)
    mottaker = db.Column(db.Integer, nullable = False)
    tidspunkt = db.Column(db.DateTime, nullable = False, default=datetime.now().replace(microsecond=0))

    def __str__(self):
        resultat = format(self.verdi, ",")
        return resultat.replace(",", " ")

class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kontonr = db.Column(db.Integer, unique=True)
    navn = db.Column(db.String(50), nullable=False)
    kontotype = db.Column(db.String(50), nullable=False)
    saldo = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, nullable = False)

    def __str__(self):
        resultat = format(self.saldo, ",")
        return resultat.replace(",", " ")