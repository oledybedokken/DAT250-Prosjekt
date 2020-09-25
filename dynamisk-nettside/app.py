from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
import datetime as dt

class User:
    def __init__(self, id, username, password,saldo, dato):
        self.id = id
        self.username = username
        self.password = password
        self.saldo = int(saldo)
        self.dato = dato

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id = 1, username= "Ole", password ="password", saldo = 2, dato =dt.date(2002, 5, 6) ))
users.append(User(id = 2, username= "Pervaz", password ="password2", saldo=500,dato =dt.date(2002, 5, 6) ))
users.append(User(id = 3, username= "Espen", password ="123", saldo=1000, dato =dt.date(2002, 5, 6)))
users.append(User(id = 4, username= "Jørgen", password ="password3", saldo=600 , dato =dt.date(2002, 5, 6)))


app = Flask(__name__)
app.secret_key = 'brusjanbank'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        print("riktig")
        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')