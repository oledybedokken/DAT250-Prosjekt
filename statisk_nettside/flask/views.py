from flask import Flask, request, session, redirect, url_for, render_template, flash, jsonify
from database_SQLAlchemy import Bruker, db, Konto
from forms import Pameldingsskjema, Registreringsskjema, Brukerskjema, legg_til_kontoskjema

@app.route("/logg_ut")
def avlogging():
    session.clear()

if __name__ == '__main__':
    database_SQLAlchemy.run()


