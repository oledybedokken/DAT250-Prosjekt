from flask import Flask,g, redirect, render_template, request,session, url_for, flash, Blueprint
import datetime as dt
from datetime import datetime, timedelta
import random
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin,current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "brusjanbank"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.database'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=5)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50),nullable=False)
    name = db.Column(db.String(50),nullable=False)

class Transaksjoner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tidspunkt = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    verdi = db.Column(db.Integer)
    KID = db.Column(db.String(15))#KIDnr skal være 15 lange tror jeg
    konto = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    verdi = db.Column(db.Integer,nullable = False,)
    rente = verdi = db.Column(db.Integer, nullable = False,)

@login_manager.user_loader
def load_user(user_id):
    # Laster inn brukeren
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, email =current_user.email)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # Sjekk om bruker faktisk eksiterer
    # Ta brukeren sitt passord, hash det, og sammenlign det med det hasha passordet i databasen
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) # Hvis bruker ikke eksisterer eller passord er feil, last inn siden på nytt med flash message

    # Hvis det over ikke skjer, logg inn og ta til profile siden
    login_user(user, remember=remember)
    return redirect(url_for('profile'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/brukere')
def brukere():
    return render_template('brukere.html', values=User.query.all())

@app.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # Hvis dette retunerer en bruker, da finnes allerede mailen i databasen

    if user: # Hvis brukeren allerede finnes, sendes den tilbake til signup page med flash message. 
        flash('Email address already exists')
        return redirect(url_for('signup'))

    # lag ny bruker med dataen fra form. Hash passworder så vanlig passord ikke blir lagret.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # legg til den nye brukeren til databasen
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
    
if __name__=="__main__":
    db.create_all()
    app.run(debug=True)


