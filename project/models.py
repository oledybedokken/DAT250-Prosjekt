from flask_login import UserMixin
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import expression


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

"""
class Account:
    number_accounts = 0
    
    def __init__ (self):
        pass

    def create_account(self, name, balance):
        Account.number_accounts += 1
        self.account_no = Account.number_accounts
        self.name = name
        self.balance = balance
        return self.account_No

    def update_interest(self):
        rate = Account.interest_rate[self.account_type]

        if (datetime.datetime.now().year == self.last_updated[1]):
            dif = (datetime.datetime.now().month - self.last_updated[0])
        else:
            if (datetime.datetime.now().month < self.last_updated[0]):
                dif (datetime.datetime.now().year - self.last_updated[1]-1)*12 + 12 - (self.last_updated[0] - datetime.datetime.now().month)
            else:
                dif (datetime.datetime.now().year - self.last_updated[1]-1)*12 + (datetime.datetime.now().month - self.last_updated[0])
    
    def balance_equity(self):
        self.update_interest()
        return self.balance

    def deposit(self):
        self.update_interest()
        dep_amount = input("Hvor mye vil du legge til? ")
        self.balance += dep_amount
        return self.balance
    
    def withdraw(self):
        withdraw_amount = input("Hvor mye vil du ta ut? ")
        if self.balance - withdraw_amount >= 0:
            self.balance -= withdraw_amount
            return self.balance
        print("OBS! Umulig sum å ta ut!")
        return -1

class Savings(Account):
    	def __init__(self):
		self.last_updated = [datetime.datetime.now().month, datetime.datetime.now().year]
		self.account_type = "Savings"

	def withdraw(self):
		withdraw_amount = input("Hvor mye vil du ta ut? ")
		if self.balance - withdraw_amount >= 1000:
			self.balance -= withdraw_amount
			return self.balance

		print("OBS! Umulig sum å ta ut!")
		return -1
"""