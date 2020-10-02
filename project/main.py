from flask import Flask,g, redirect, render_template, request,session, url_for, flash, Blueprint
from flask_login import login_required, current_user
from .models import User, Transaksjoner, Loan, BankAccount
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

@main.route('/create_bank_account', methods=['GET', 'POST'])
@login_required
def create_bank_account():
    if request.method == 'POST':
        kontotype = request.form['kontotype']
        kontonavn = request.form['kontonavn']
        new_account = BankAccount(id = int(random.randint(1e15, 1e16)), navn = kontonavn, kontotype = kontotype, saldo=int(0), user_id = current_user.id)
        db.session.add(new_account)
        db.session.commit()
        return redirect(url_for('overview'))

    return render_template('create_bank_account.html')