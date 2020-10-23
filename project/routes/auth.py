from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, set_login_view, current_user
from ..models import User, Transaction, BankAccount, ModelView, Roles, db
from flask_scrypt import generate_random_salt, generate_password_hash, check_password_hash
import requests, json
from project.app import admin
from flask_admin import Admin
from flask_security import Security, SQLAlchemyUserDatastore

set_login_view("auth.signin")

user_datastore = SQLAlchemyUserDatastore(db, User, Roles)


auth = Blueprint('auth', __name__)

#admin.add_view(ModelView(User, db.session))
#admin.add_view(ModelView(Transaction, db.session))
#admin.add_view(ModelView(BankAccount, db.session))



@auth.route('/signin')
def signin():
    sitekey = "6LcME9UZAAAAAFs9gpLPk2cNe6y7KsbltAMyZOIk"
    return render_template('login.html', sitekey = sitekey )

@auth.route('/signin', methods=['POST', 'GET'])
def signin_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    captcha_response = request.form.get('g-recaptcha-response')
    
    if not is_human(captcha_response):
        user = User.query.filter_by(email=email).first()

        
        if not user: 
            flash('Brukeren finnes ikke, trykk på registrer for å opprette en bruker')
            return redirect(url_for('auth.signin')) # Hvis bruker ikke eksisterer eller passord er feil, last inn siden på nytt med flash message

        print("Sjekker innlogging med passord, opp mot hash og salt i databasen")
        print(password)
        print(user.password)
        print(user.salt)
        print("bruker salten til å hashe passordet på nytt")
        p_hash = generate_password_hash(password, user.salt)
        print(p_hash)

        print(user.fornavn)

        # Sjekk om bruker faktisk eksiterer
        # Ta brukeren sitt passord, hash det, og sammenlign det med det hasha passordet i databasen
        if not check_password_hash(password, user.password, user.salt): 
            flash('Passordet er feil')
            return redirect(url_for('auth.signin'))

        # Hvis det over ikke skjer, logg inn og ta til profile siden
        login_user(user, remember=remember, force=True)
        return redirect(url_for('main.profile'))

    flash('Du er ikke menneske!')
    return redirect(url_for('auth.signin'))

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
    kjonn = str(request.form.get('Kjonn'))
    fodselsdato = request.form.get('Fodselsdato')
    password = request.form.get('psw')
    repeatPassword = request.form.get('psw-repeat')
    captcha_response = request.form.get('g-recaptcha-response')
    
    if not is_human(captcha_response):
        salt = generate_random_salt()
        print(salt)

        #if database not exist, create database
    
        user = User.query.filter_by(email=email).first() # Hvis dette retunerer en bruker, da finnes allerede mailen i databasen

        if user: # Hvis brukeren allerede finnes, sendes den tilbake til signup page med flash message. 
            flash('Email adresse allerede finnes.')
            return redirect(url_for('auth.signup'))
            

        if str(password) != str(repeatPassword):
            flash('Ditt passord er ikke lik. Prøv igjen!')
            return redirect(url_for('auth.signup'))


        # lag ny bruker med dataen fra form. Hash passworder så vanlig passord ikke blir lagret.
        p_hash = generate_password_hash(password, salt)
        print()
        print("Registrerer bruker med passord, salt, hash:")
        print(password)
        print(salt)
        print(p_hash)
        print()

        user = User(email=email, 
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
        user_datastore.toggle_active(user)
        # legg til den nye brukeren til databasen
        db.session.add(user)
        db.session.commit()

        print("passordet og salt fra databasen:")
        print(user.password)
        print(user.salt)

        return redirect(url_for('auth.signin'))
    
    flash('Du er ikke Menneske!')
    return redirect(url_for('auth.signup'))


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