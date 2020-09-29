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
from datetime import datetime
import random

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

    def finn_konto(self, konto_id):
        for konto in self.kontoer:
            if konto.id == konto_id:
                return konto

class BankAccount:
    def __init__(self, name, kontotype, user_id, saldo):
        self.name = name
        self.kontotype = kontotype
        self.user_id = user_id
        self.saldo = int(saldo)
        self.id = int(random.randint(1e15, 1e16))
        self.transactions = []

    def utfor_transaksjon(self, mottaker_konto, transaksjonstype, pengesum):
        self.mottaker_konto = mottaker_konto
        self.transaksjonstype = transaksjonstype
        self.pengesum = int(pengesum)
        self.dato = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.ny_saldo = self.saldo - self.pengesum
        self.ny_mottaker_saldo = mottaker_konto.saldo + self.pengesum

        self.saldo -= pengesum
        mottaker_konto.saldo += pengesum

        self.transactions.append(Transaction(mottaker_konto.id, self.transaksjonstype, -self.pengesum, self.dato, self.ny_saldo))
        mottaker_konto.transactions.append(Transaction(self.id, self.transaksjonstype, "+"+str(self.pengesum), self.dato, self.ny_mottaker_saldo))

    def ingen_transaksjoner(self):
        if len(self.transactions) == 0:
            return True
        return False

class Loan:
    def __init__(self, name, user_id, saldo):
        self.name = name
        self.user_id = user_id
        self.saldo = int(saldo)


class Transaction:
    def __init__(self, konto2, transaksjonstype, pengesum, dato, ny_saldo):
        self.konto2 = konto2
        self.transaksjonstype = transaksjonstype
        self.pengesum = pengesum
        self.dato = dato
        self.ny_saldo = int(ny_saldo)


users = []
users.append(User(id = 1, username= "Ole", password ="password", saldo = 2, dato =dt.date(2002, 5, 6) ))
users.append(User(id = 2, username= "Pervaz", password ="password2", saldo=500,dato =dt.date(2002, 5, 6) ))
users.append(User(id = 3, username= "Espen", password ="69420123", saldo=1000, dato =dt.date(2002, 5, 6)))
users.append(User(id = 4, username= "Jørgen", password ="password3", saldo=600 , dato =dt.date(2002, 5, 6)))

for user in users:
    user.kontoer.append(BankAccount(name = "Brukskonto", kontotype ="bruk", user_id = user.id, saldo = 1300))
    user.kontoer.append(BankAccount(name = "Regninger", kontotype = "bruk", user_id = user.id, saldo = 7200))
    user.kontoer.append(BankAccount(name = "Sparekonto", kontotype = "spar", user_id = user.id, saldo = 4))
    user.laan.append(Loan(name = "Lån type hus", user_id = user.id, saldo = 2345928))
    user.laan.append(Loan(name = "Lån type bil", user_id = user.id, saldo = 356281))
    print()
    print(f"Kontonummer for bruker: {user.username}")
    print(f"{user.kontoer[0].name}: {user.kontoer[0].id}")
    print(f"{user.kontoer[1].name}: {user.kontoer[1].id}")
    print(f"{user.kontoer[2].name}: {user.kontoer[2].id}")
    print()

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

    if request.method == 'POST' and request.form["btn"] == "overfør":
        fra_konto_id = request.form["fra_konto"]
        til_konto_id = request.form["til_konto"]
        pengesum = int(request.form["pengesum"])
        fra_konto = g.user.finn_konto(int(fra_konto_id))
        til_konto = g.user.finn_konto(int(til_konto_id))

        if fra_konto == til_konto or fra_konto.saldo < pengesum:
            print("Kontoene er like")
            return redirect(url_for('transaction'))
        
        fra_konto.utfor_transaksjon(til_konto, "overføring", pengesum)
        return redirect(url_for('overview'))

    if request.method == 'POST' and request.form["btn"] == "betal":
        fra_konto_id = request.form["fra_konto_bet"]
        til_konto_id = request.form["til_konto_bet"]
        pengesum = int(request.form["pengesum2"])
        fra_konto = g.user.finn_konto(int(fra_konto_id))
        for user in users:
            for konto in user.kontoer:
                if konto.id == int(til_konto_id):
                    til_konto = user.finn_konto(int(til_konto_id))
                    break

        if fra_konto == til_konto or fra_konto.saldo < pengesum:
            print("Kontoene er like")
            return redirect(url_for('transaction'))
        
        fra_konto.utfor_transaksjon(til_konto, "overføring", pengesum)
        return redirect(url_for('overview'))

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
            g.user.kontoer.append(BankAccount(name = kontonavn, kontotype = "bruk", user_id = user.id, saldo = 0))
        else:
            g.user.kontoer.append(BankAccount(name = kontonavn, kontotype = "spar", user_id = user.id, saldo = 0))
        return redirect(url_for('overview'))

    return render_template('create_bank_account.html')

@app.route('/account<int:account_id>', methods=['GET'])
def account(account_id):
    if not g.user:
        return redirect(url_for('login'))

    kontoen = g.user.finn_konto(int(account_id))
    if kontoen in g.user.kontoer:
        return render_template('account.html', konto=kontoen)

    return redirect(url_for('account'))