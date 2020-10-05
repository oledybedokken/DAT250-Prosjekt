from flask import Flask,g, redirect, render_template, request,session, url_for, flash, Blueprint
from flask_login import login_required, current_user
from .models import db, User, Transaction, Loan, BankAccount
import random
from sqlalchemy import desc, or_

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    kontoer=BankAccount.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', fornavn=current_user.fornavn, email =current_user.email, etternavn = current_user.etternavn, addresse = current_user.postAddresse, postkode = current_user.postKode, fylke = current_user.fylke, kjonn = current_user.kjonn, fodselsdato = current_user.fodselsdato, password = current_user.password, kontoer=kontoer )

@main.route('/profile', methods=['POST'])
@login_required
def profile_post():
    kontoer=BankAccount.query.filter_by(user_id=current_user.id).all()
    #Oppdatere data inne i profil
    #skal kunne hente data fra db, og sjekke opp mot data i Profil. 
    #Om data er annerledes, oppdater data
    fornavn = request.form.get('fornavn')
    etternavn = request.form.get('etternavn')
    email = request.form.get('email')
    postAddresse = request.form.get('postAddresse')
    postKode = request.form.get('postKode')
    fylke = request.form.get('fylke')
    kjonn = request.form.get('kjonn')
    fodselsdato = request.form.get('fodselsdato')
    
    user = User.query.filter_by(id=current_user.id).first()

    #Burde ikke kunne sette lik mail som allerede er i databasen
    #user.email = email
    user.fornavn = fornavn
    user.etternavn = etternavn
    user.postAddresse = postAddresse
    user.postKode = postKode
    user.fylke = fylke
    user.kjonn = kjonn
    user.fodselsdato = fodselsdato

    db.session.commit()


    return render_template('profile.html', fornavn=current_user.fornavn, email =current_user.email, etternavn = current_user.etternavn, addresse = current_user.postAddresse, postkode = current_user.postKode, fylke = current_user.fylke, kjonn = current_user.kjonn, fodselsdato = current_user.fodselsdato, password = current_user.password, kontoer=kontoer)

@main.route('/overview')
@login_required
def overview():
    kontoer=BankAccount.query.filter_by(user_id=current_user.id).all()
    laan=Loan.query.filter_by(user_id=current_user.id).all()
    return render_template('overview.html', kontoer=kontoer, laan=laan)

@main.route('/overview', methods=['POST'])
@login_required
def overview_post():
    kontoer=BankAccount.query.filter_by(user_id=current_user.id).all()
    laan=Loan.query.filter_by(user_id=current_user.id).all()
    return render_template('overview.html', kontoer=kontoer, laan=laan)

@main.route('/account<int:kontonr>')
@login_required
def account(kontonr):
    kontoen = BankAccount.query.filter_by(kontonr=int(kontonr)).first()
    print(kontonr)
    transaksjoner = Transaction.query.filter(or_(Transaction.avsender==kontonr, Transaction.mottaker==kontonr)).all()

    return render_template('account.html', konto=kontoen, transaksjoner=transaksjoner)

@main.route('/create_bank_account')
@login_required
def create_bank_account():
    return render_template('create_bank_account.html')

@main.route('/create_bank_account', methods=['POST'])
def create_bank_account_post():
    kontotype = request.form['kontotype']
    kontonavn = request.form['kontonavn']
    kontonummer = int(random.randint(1e15, 1e16))
    while BankAccount.query.filter_by(kontonr=kontonummer).first():
        kontonummer = int(random.randint(1e15, 1e16))

    new_account = BankAccount(kontonr = kontonummer, navn = kontonavn, kontotype = kontotype, saldo=int(10000), user_id = current_user.id)
    db.session.add(new_account)
    db.session.commit()
    return redirect(url_for('main.overview'))

# Sletting av bank konto, dette er template for viedere development - ikke ferdig
@main.route('/delete_bank_account<int:kontonr>')
@login_required
def delete_bank_account(kontonr):
    kontoen = BankAccount.query.filter_by(kontonr=int(kontonr)).first()
    if BankAccount is None: # Om bankkonto er tom
        print('Du har ikke bruker å slette.')
    if BankAccount is not None: # Om bakkonto ikke er tom
        if kontoen.saldo == 0: # om saldo er null, den slettes.
            db.session.delete(kontoen)
            db.session.commit()
            print('Konto er slettet.')
        else:
            print('Konto må være tom for sletting.') # Om den ikke er tom, feilmelding
    return redirect(url_for('main.overview'))

@main.route('/delete_bank_account',  methods=['POST'])
def delete_bank_account_post():
    kontoen = BankAccount.query.filter_by(user_id=current_user.id).first()
    if BankAccount is None: # Om bankkonto er tom
        print('Du har ikke bruker å slette.')
    if BankAccount is not None: # Om bakkonto ikke er tom
        if kontoen.saldo == 0: # om saldo er null, den slettes.
            db.session.delete()
            db.session.commit()
            print('Konto er slettet.')
        else:
            print('Konto må være tom for sletting.') # Om den ikke er tom, feilmelding
    return redirect(url_for('main.overview'))

# om bruker ikke finnes, gi feilmelding
# om bruker finnes i database, ikke ha penger
# om bruker finnes og ikke har penger, slett. 

@main.route('/create_loan')
@login_required
def create_loan():
    kontoen = BankAccount.query.filter_by(user_id=current_user.id).first()
    if not kontoen:
        print("Finner ikke en gyldig konto")
        flash('Du må opprette en konto først!') #FÅ DENNE TIL Å VISES
        return redirect(url_for('main.overview'))

    return render_template('create_loan.html')

@main.route('/create_loan', methods=['POST'])
def create_loan_post():
    laan_type = request.form['kontotype']
    verdi = int(request.form['laan_verdi'])
    new_loan = Loan(laan_type=laan_type, verdi=verdi, user_id = current_user.id)
    db.session.add(new_loan)

    kontoen = BankAccount.query.filter_by(user_id=current_user.id).first()
    kontoen.saldo += verdi

    transaksjon = Transaction(trans_type=laan_type, verdi=verdi, avsender="", mottaker=kontoen.kontonr)
    db.session.add(transaksjon)
    db.session.commit()

    return redirect(url_for('main.overview'))

@main.route('/transaction')
@login_required
def transaction():
    bruker_kontoer = BankAccount.query.filter_by(user_id=current_user.id).all()
    alle_kontoer = BankAccount.query.all()
    andre_kontoer = {}
    for konto in alle_kontoer:
        if konto not in bruker_kontoer:
            bruker = User.query.filter_by(id=konto.user_id).first()
            andre_kontoer[konto] = bruker.fornavn + " " + bruker.etternavn

    return render_template('transaction.html', bruker_kontoer=bruker_kontoer, andre_kontoer=andre_kontoer)

@main.route('/transaction', methods=['POST'])
def transaction_post():
    if request.form["btn"] == "overfør":
        avsender_kontonr = request.form["fra_konto"]
        mottaker_kontonr = request.form["til_konto"]
        pengesum = int(request.form["pengesum"])
        trans_type = "Overføring"
        
    if request.form["btn"] == "betal":
        avsender_kontonr = request.form["avsender_konto"]
        mottaker_kontonr = request.form["mottaker_konto"]
        pengesum = int(request.form["pengesum"])
        trans_type = "Betaling"

    avsender_konto = BankAccount.query.filter_by(kontonr=int(avsender_kontonr)).first()
    mottaker_konto = BankAccount.query.filter_by(kontonr=int(mottaker_kontonr)).first()

    if not BankAccount.query.filter_by(kontonr=int(mottaker_kontonr)).all():
        print("Ugyldig konto")
        return redirect(url_for('main.transaction'))

    if avsender_konto == mottaker_konto:
        print("Kontoene er like")
        return redirect(url_for('main.transaction'))

    if avsender_konto.saldo < pengesum:
        print("Du har ikke nok penger")
        return redirect(url_for('main.transaction'))

    # Oppdater databsen
    avsender_konto.saldo -= pengesum
    mottaker_konto.saldo += pengesum
    transaksjon = Transaction(trans_type=trans_type, verdi=pengesum, avsender=avsender_kontonr, mottaker=mottaker_kontonr)
    db.session.add(transaksjon)
    db.session.commit()
    return redirect(url_for('main.overview'))