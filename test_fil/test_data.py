import sys
import csv
import os
from database import Base, Bruker, Kunder, Konto, KundeLog, Transaksjoner
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bcrypt import Bcrypt
from flask import Flask

app = Flask(__name__)
engine = create_engine("sqlite:///database.db",connect_args={"check_same_thread": False},echo=True)
Base.metadata.bind = engine
db = scoped_session(sessionmaker(bind=engine))
bcrypt = Bcrypt(app)


def brukere():
    email = "sjoko@gmail.com"
    name = "Pervaz"
    usert = "executive" # Admin
    passwd = "Admin123!12"
    passord_hash = bcrypt.generate_password_hash(passwd).decode("utf-8")
    db.execute("INSERT INTO bruker (id,name, bruker_type, password) VALUES (:u,:n,:t,:p)", {"u": email,"n":name,"t":usert ,"p": passord_hash})
    db.commit()
    print("Konto er skapt ............................................ ")

if __name__ == "__main__":
    brukere()