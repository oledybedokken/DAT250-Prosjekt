import sys
import csv
import os
from database import Base, Konto, Bruker, Kunder, KundeLog, Transaksjoner
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bcrypt import Bcrypt
from flask import Flask

app = Flask(__name__)
engine = create_engine("sqlite:///database.db",connect_args={"check_same_thread": False},echo=True)
Base.metadata.bind = engine
db = scoped_session(sessionmaker(bind=engine))
bcrypt = Bcrypt(app)

def kontoer():
    email = "sjokomannen@gmail.com"
    navn = "Harald"
    usert = "executive"
    passord = "Harmon2"
    passord_hash = bcrypt.generate_password_hash(passord).decode("utf-8")
    db.execute("INSERT INTO bruker (id,navn,bruker_type,passord) VALUES (:u,:n,:t,:p)", {"u": email,"n":navn,"t":usert ,"p": passord_hash})
    db.commit()
    print("Konto skapes ............................................ ")
    email = "sjamokn@gmail.com"
    navn = "Watermalaon"
    usert = "cashier"
    passord = "Fritok123"
    passord_hash = bcrypt.generate_password_hash(passord).decode("utf-8")
    db.execute("INSERT INTO bruker (id,navn,bruker_type,passord) VALUES (:u,:n,:t,:p)", {"u": email,"n":navn,"t":usert ,"p": passord_hash})
    db.commit()
    print("Konto skapes ............................................ ")
    email = "koimnbn@gmail.com"
    navn = "Lakim"
    usert = "teller"
    passord = "Lakim123"
    passord_hash = bcrypt.generate_password_hash(passord).decode("utf-8")
    db.execute("INSERT INTO bruker (id,navn,bruker_type,passord) VALUES (:u,:n,:t,:p)", {"u": email,"n":navn,"t":usert ,"p": passord_hash})
    db.commit()
    print("Konto skapes ............................................ ")
    email = "test123"
    navn = "Yogurt"
    usert = "teller"
    passord = "admin"
    passord_hash = bcrypt.generate_password_hash(passord).decode("utf-8")
    db.execute("INSERT INTO bruker (id,navn,bruker_type,passord) VALUES (:u,:n,:t,:p)", {"u": email,"n":navn,"t":usert ,"p": passord_hash})
    db.commit()
    print("Konto skapes ............................................ ")

if __name__ == "__main__":
    kontoer()