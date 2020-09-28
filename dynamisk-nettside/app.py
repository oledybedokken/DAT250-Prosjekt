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

        # Liste med kontoer og lån
        self.kontoer = []
        self.laan = []

    def __repr__(self):
        return f'<User: {self.username}>'


class BankAccount:
    def __init__(self, name, kontotype, user_id, saldo):
        self.name = name
        self.kontotype = kontotype
        self.user_id = user_id
        self.saldo = int(saldo)

    def withdraw(self, sum):
        self.saldo -= sum
        return self.saldo

    def deposit(self, sum):
        self.saldo += sum
        return self.saldo


class Loan:
    def __init__(self, name, user_id, saldo):
        self.name = name
        self.user_id = user_id
        self.saldo = int(saldo)

users = []
users.append(User(id = 1, username= "Ole", password ="password", saldo = 2, dato =dt.date(2002, 5, 6) ))
users.append(User(id = 2, username= "Pervaz", password ="password2", saldo=500,dato =dt.date(2002, 5, 6) ))
users.append(User(id = 3, username= "Espen", password ="69420123", saldo=1000, dato =dt.date(2002, 5, 6)))
users.append(User(id = 4, username= "Jørgen", password ="password3", saldo=600 , dato =dt.date(2002, 5, 6)))

for user in users:
    user.kontoer.append(BankAccount(name = "Brukskonto", kontotype ="bruk", user_id = 4, saldo = 1300))
    user.kontoer.append(BankAccount(name = "Regninger", kontotype = "bruk", user_id = 4, saldo = 7200))
    user.kontoer.append(BankAccount(name = "Sparekonto", kontotype = "spar", user_id = 4, saldo = 4))
    user.laan.append(Loan(name = "Lån type hus", user_id = 4, saldo = 2345928))
    user.laan.append(Loan(name = "Lån type bil", user_id = 4, saldo = 356281))

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

@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        fra_konto = request.form["fra_konto"]
        til_konto = request.form["til_konto"]
        pengesum = int(request.form["pengesum"])
        print(fra_konto)
        print(til_konto)
        print(pengesum)

        #if fra_konto == til_konto:
        #    print("Kontoene er like")
        #    return redirect(url_for('transaction'))
        
        #fra_konto.withdraw(pengesum)
        #til_konto.deposit(pengesum)
        #return redirect(url_for('overview'))

    return render_template('transaction.html')

@app.route('/overview')
def overview():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('overview.html')

@app.route('/create_bank_account', methods=['GET', 'POST'])
def create_bank_account():
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        kontotype = request.form['kontotype']
        kontonavn = request.form['kontonavn']
        if kontotype == "bruk":
            user.kontoer.append(BankAccount(name = kontonavn, kontotype = "bruk", user_id = user.id, saldo = 0))
        else:
            user.kontoer.append(BankAccount(name = kontonavn, kontotype = "spar", user_id = user.id, saldo = 0))
        return redirect(url_for('overview'))

    return render_template('create_bank_account.html')

@app.route('/account')
def account():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('account.html')