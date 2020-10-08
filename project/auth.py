from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Transaction, BankAccount
from . import db
from flask_scrypt import generate_random_salt, generate_password_hash, check_password_hash
import requests, json

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # Sjekk om bruker faktisk eksiterer
    # Ta brukeren sitt passord, hash det, og sammenlign det med det hasha passordet i databasen
    if not check_password_hash(password, user.password, user.salt): 
        flash('Passordet er feil')
        return redirect(url_for('auth.login'))

    if not user: 
        flash('Brukeren finnes ikke, trykk på signup for å registrere')
        return redirect(url_for('auth.login')) # Hvis bruker ikke eksisterer eller passord er feil, last inn siden på nytt med flash message

    # Hvis det over ikke skjer, logg inn og ta til profile siden
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    sitekey = "6LcME9UZAAAAAFs9gpLPk2cNe6y7KsbltAMyZOIk"
    return render_template('signup.html', sitekey = sitekey)

@auth.route('/signup', methods=['POST'])
def signup_post():

    #Henter all informasjonen fra form til variabler
    fornavn = request.form.get('fornavn')
    etternavn = request.form.get('etternavn')
    email = request.form.get('email')
    postAddresse = request.form.get('postAddresse')
    postKode = request.form.get('postKode')
    fylke = request.form.get('fylke')
    kjonn = request.form.get('Kjonn')
    fodselsdato = request.form.get('Fodselsdato')
    password = request.form.get('psw')
    repeatPassword = request.form.get('psw-repeat')
    captcha_response = request.form.get('g-recaptcha-response')
    
    if is_human(captcha_response):
        flash('Du klarte det!')
    else:
        flash('Du er ikke ett menneske!')
        return redirect(url_for('auth.signup'))
    salt = generate_random_salt()

    #if database not exist, create database
    
    user = User.query.filter_by(email=email).first() # Hvis dette retunerer en bruker, da finnes allerede mailen i databasen

    if user: # Hvis brukeren allerede finnes, sendes den tilbake til signup page med flash message. 
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    if str(password) != str(repeatPassword):
        flash('Ditt passord er ikke lik. Prøv igjen!')
        return redirect(url_for('auth.signup'))


    # lag ny bruker med dataen fra form. Hash passworder så vanlig passord ikke blir lagret.
    p_hash = generate_password_hash(password, salt)

    new_user = User(email=email, 
                    fornavn=fornavn, 
                    password=p_hash, 
                    etternavn=etternavn, 
                    postAddresse = postAddresse, 
                    postKode = postKode, 
                    fylke = fylke, 
                    kjonn = kjonn, 
                    fodselsdato = fodselsdato, 
                    salt = salt
                    )

    # legg til den nye brukeren til databasen
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

def is_human(captcha_response):
    """ Validating recaptcha response from google server
        Returns True captcha test passed for submitted form else returns False.
    """
    secret = "6LcME9UZAAAAAN3gmRrcW0RTQoGpA5bRs980Hoco"
    payload = {'response':captcha_response, 'secret':secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))