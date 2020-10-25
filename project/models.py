from flask_security import RoleMixin, UserMixin
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import expression
from flask_admin.contrib.sqla import ModelView
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour", "5 per minute"])
db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(300),nullable=False)
    fornavn = db.Column(db.String(50),nullable=True)
    etternavn = db.Column(db.String(50),nullable=True)
    postAddresse = db.Column(db.String(50),nullable=True)
    postKode = db.Column(db.String(50),nullable=True)
    fylke = db.Column(db.String(50),nullable=True)
    kjonn = db.Column(db.String(50),nullable=True)
    fodselsdato = db.Column(db.String(50),nullable=True)
    salt = db.Column(db.String(300))
    active = db.Column(db.Boolean())


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