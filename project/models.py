from flask_login import UserMixin
from datetime import datetime, timedelta
from . import db

#class User(UserMixin, db.Model):
#    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
#    email = db.Column(db.String(100), unique=True)
#    password = db.Column(db.String(100))
#    name = db.Column(db.String(1000))

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

class Withdraw(db.Model):
    amount = db.Column(db.Integer(50), nullable = False)

class Deposit(db.Model):
    amount = db.Column(db.Integer(50), nullable = False)

class Transaksjoner(db.Model):
    __tablename__ = 'transaksjoner'
    id = db.Column(db.Integer, primary_key=True)
    tidspunkt = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    beskrivelse = db.Column(db.Text)
    verdi = db.Column(db.Integer)
    KID = db.Column(db.String(15))#KIDnr skal være 15 lange ifølge ole
    konto = db.Column(db.Integer)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
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
