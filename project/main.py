from flask import Flask,g, redirect, render_template, request,session, url_for, flash, Blueprint
from flask_login import login_required, current_user
from .models import db, User, Transaction, Loan, BankAccount
import random

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.fornavn)

@main.route('/overview')
@login_required
def overview():
    kontoer=BankAccount.query.filter_by(user_id=current_user.id).all()
    return render_template('overview.html', kontoer=kontoer)

@main.route('/account<int:account_id>')
@login_required
def account(account_id):
    kontoen = BankAccount.query.filter_by(id=int(account_id)).first()
    sendt = Transaction.query.filter_by(avsender=account_id).all()
    mottatt = Transaction.query.filter_by(mottaker=account_id).all()
    transaksjoner = sendt + mottatt

    return render_template('account.html', konto=kontoen, transaksjoner=transaksjoner)

@main.route('/create_bank_account')
@login_required
def create_bank_account():
    return render_template('create_bank_account.html')

@main.route('/create_bank_account', methods=['POST'])
def create_bank_account_post():
    kontotype = request.form['kontotype']
    kontonavn = request.form['kontonavn']
    new_account = BankAccount(id = int(random.randint(1e15, 1e16)), navn = kontonavn, kontotype = kontotype, saldo=int(0), user_id = current_user.id)
    db.session.add(new_account)
    db.session.commit()
    return redirect(url_for('main.overview'))

@main.route('/transaction')
@login_required
def transaction():
    kontoer=BankAccount.query.filter_by(user_id=current_user.id).all()
    for konto in kontoer:
        print(f"{konto.navn}: {konto.id}")
    return render_template('transaction.html', kontoer=kontoer)

@main.route('/transaction', methods=['POST'])
def transaction_post():
    if request.form["btn"] == "overfør":
        avsender_konto_id = request.form["fra_konto"]
        mottaker_konto_id = request.form["til_konto"]
        pengesum = int(request.form["pengesum"])
        trans_type = "Overføring"
        
    if request.form["btn"] == "betal":
        avsender_konto_id = request.form["avsender_konto"]
        mottaker_konto_id = request.form["mottaker_konto"]
        pengesum = int(request.form["pengesum"])
        trans_type = "Betaling"

    avsender_konto = BankAccount.query.filter_by(id=avsender_konto_id).first()
    mottaker_konto = BankAccount.query.filter_by(id=mottaker_konto_id).first()

    if not BankAccount.query.filter_by(id=mottaker_konto_id).all():
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
    transaksjon = Transaction(trans_type=trans_type, verdi=pengesum, avsender=avsender_konto_id, mottaker=mottaker_konto_id)

    db.session.add(transaksjon)
    db.session.commit()
    return redirect(url_for('main.overview'))