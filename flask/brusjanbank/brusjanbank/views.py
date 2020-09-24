import datetime
from brusjanbank import app
from flask import render_template

articles = [{'id': 1, 'navn': 'Ole', 'saldo': '1.000.000','konto': datetime.date(1999, 4, 12)}, 
            {'id': 2, 'navn': 'Pervaz', 'saldo': '999.999','konto': datetime.date(2122, 9, 2)},
            {'id': 3, 'navn': 'Jørgen', 'saldo': '888.888','konto': datetime.date(2014, 8, 7)},
            {'id': 4, 'navn': 'Vebee', 'saldo': '258.795','konto': datetime.date(2003, 4, 7)},
            {'id': 5, 'navn': 'Espen', 'saldo': 'Broke','konto': datetime.date(2002, 5, 6)}]
@app.route('/')
def index():
    return render_template('index.html', articles=articles)

@app.route('/article/<int:article_id>')
def article(article_id):
    return render_template('article.html', article=articles[article_id - 1])