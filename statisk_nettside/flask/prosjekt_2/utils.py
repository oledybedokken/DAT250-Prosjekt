import all_module as mp
from pymongo import ReturnDocument
import pymongo

def record_transaction(username, account_num, amount, description=None):
    time = am.datetime.now().strftime('%c')
    transaction = {
        'time': time,
        'amount': amount
    } if not description else {
        'description': description,
        'time': time,
        'amount': amount
    }

    am.clients.update_one(
        {'username': username, 'accounts.account_number': str(account_num)},
        {'$push': {
            'accounts.$.transactions': {
                '$each': [transaction],
                '$position': 0}
        }}
    )

def deposit(user, account_number, deposit_amount, description=None):
    amount = float(deposit_amount)
    if am.verify(str(account_number)) and str(account_number)[0] == '4':
        neg_d128_amount = to_d128(abs(amount) * -1)
        d128_amount = to_d128(abs(amount))
        client = am.clients.find_one_and_update({
            'username': user,
            'accounts.account_number': str(account_number)},
            {'$inc': {'accounts.$.balance': neg_d128_amount,
                      'accounts.$.available_credit': d128_amount}},
            return_document=ReturnDocument.AFTER)
    else:
        d128_amount = to_d128(abs(amount))
        client = am.clients.find_one_and_update(
            {'username': user, 'accounts.account_number': str(account_number)},
            {'$inc': {'accounts.$.balance': d128_amount}},
            return_document=ReturnDocument.AFTER)
    if client:
        record_transaction(user, account_number, d128_amount, description)
    return client