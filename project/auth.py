from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
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


    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

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

    user = User.query.filter_by(email=email).first() # Hvis dette retunerer en bruker, da finnes allerede mailen i databasen

    if user: # Hvis brukeren allerede finnes, sendes den tilbake til signup page med flash message. 
        flash('Email address already exists')
        return redirect(url_for('signup'))

    if str(password) != str(repeatPassword):
        flash('Ditt passord er ikke lik på gjenta passord. Prøv igjen!')
        return redirect(url_for('signup'))


    # lag ny bruker med dataen fra form. Hash passworder så vanlig passord ikke blir lagret.
    p_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(email=email, fornavn=fornavn, password=p_hash, etternavn=etternavn, postAddresse = postAddresse, postKode = postKode, fylke = fylke, kjonn = kjonn, fodselsdato = fodselsdato)

    # legg til den nye brukeren til databasen
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))