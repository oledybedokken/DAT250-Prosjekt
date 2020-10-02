# models.py

from flask_login import UserMixin
import datetime as dt
from datetime import datetime, timedelta

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


class Transaksjoner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tidspunkt = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    verdi = db.Column(db.Integer)
    KID = db.Column(db.String(15))#KIDnr skal være 15 lange ifølge ole
    konto = db.Column(db.Integer)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    verdi = db.Column(db.Integer,nullable = False)
    rente = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(50),nullable=False)
    kontotype = db.Column(db.String(50),nullable=False)
    saldo = db.Column(db.Integer,nullable = False)
    user_id = db.Column(db.Integer, nullable = False)