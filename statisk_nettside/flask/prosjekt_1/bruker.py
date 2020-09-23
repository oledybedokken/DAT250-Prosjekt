from .. import alle_moduler as am
from .views import log_transaksjon
from bcrypt import hashpw

slettet = 0

# Skriv metode for å lage konto
# Skriv metode for å slette konto

def skape_konto():
    pass

# Fortsett med denne!

def slett_konto():
    data = am.request.get_json()
    if not data:
        return am.jsonify({"msg": "OBS! Ingen data"})
    try:
        email1 = data["email"]
        passord = data["passord"]
        auth_kode = data["auth_kode"]
    except KeyError:
        return am.jsonify({"msg": "OBS! Sjekk om stavefeil"})

    bruker = am.bruker.find_one({"email": email})
    if not bruker:
        return am.jsonify({"msg": "Feil email/passord"})

    finnes = am.bcrypt.check_password_hash(bruker["passord"].decode("UTF-8"),
                                          passord)

    if not finnes or email != bruker["email"]:
        return am.jsonify({"msg": "Feil email/passord eller autorisering kode"})

    result = am.bruker.slett_konto({"email": email})
    if result.slettet:
        return am.jsonify({"msg": f"e-mailen <{email}> er slettet!"})
    return am.jsonify({"msg": f"e-mailen <{email}> ikke finnes!"})