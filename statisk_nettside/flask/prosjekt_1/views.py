from flask import alle_moduler as am
from pymongo import ReturnDocument


def make_serializable(bruker_log): # Fjern - skrevet bedre versjon som er ikke dum (14.09.2020)
    """
    Convert all decimal128 to float
    """
    for key in bruker_log:
        if type(bruker_log[key]) is am.Decimal128:
            bruker_log[key] = float(bruker_log[key].to_decimal())
        if type(bruker_log[key]) is dict:
            make_serializable(bruker_log[key])
        if type(bruker_log[key]) is list:
            for item in bruker_log[key]:
                make_serializable(item)
                # Stackoverflow

def log_transaksjon(email, konto_nummer, formue):
    tid = am.datetime.now().strftime('%c')
    transaksjon = {
        'tid': tid,
        'formue': formue
    }

    am.bruker.update_one(
        {'email': email, 'bruker.konto_nummer': str(konto_nummer)},
        {'$push': {
            'bruker.$.transaksjoner': {
                '$each': [transaksjon],
                '$position': 0}
        }}
    )


def uttak(email, konto_nummer, uttak_formue): # Fjern - skrevet bedre versjon som er ikke dum (14.09.2020)
    formue = float(uttak_formue)
    if am.verify(str(konto_nummer)) and str(konto_nummer)[0] == '4':
        neg_d128_formue = to_d128(abs(formue) * -1)
        d128_formue = to_d128(abs(formue))
        bruker = am.bruker.find_one_and_update({
            'email': email,
            'bruker.konto_nummer': str(konto_nummer)},
            {'$inc': {'bruker.$.sum': neg_d128_formue,
                      'bruker.$.available_credit': d128_formue}},
            return_document=ReturnDocument.AFTER)
    else:
        d128_formue = to_d128(abs(formue))
        bruker = am.bruker.find_one_and_update(
            {'email': email, 'bruker.konto_nummer': str(konto_nummer)},
            {'$inc': {'bruker.$.sum': d128_formue}},
            return_document=ReturnDocument.AFTER)
    if bruker:
        log_transaksjon(email, konto_nummer, d128_formue)
    return bruker