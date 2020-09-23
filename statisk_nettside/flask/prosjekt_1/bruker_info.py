from .. import alle_moduler as am
from .views import make_serializable
from datetime import datetime

# Oppdater bruker info - Skriv mer!
# INFO: Jeg skriver email på to måter: når jeg spør bare om email og om når jeg leter om brukeren finnes
# noen funksjoner er kopiert fra tutorial.

def bruker_oppdater():
    data = am.request.get_json()
    if not data:
        return am.jsonify({"msg": "OBS! Ingen data"})

    try:
        fornavn = data["fornavn"].lower()
        etternavn = data["etternavn"].lower()
        email = data["email"].lower()
        nav_passord = data["nav_passord"]
        passord = data.get("passord", None)
    except nError:
        return am.jsonify({"msg": "OBS! Sjekk om stavefeil"})
    nav_bruker = am.get_jwt_identity()["email"]

    bruker = am.bruker.find_one({"email": nav_bruker})
    if not bruker:
        return am.jsonify({"msg": "bruker ikke finnes"})

    finnes = am.bcrypt.check_password_hash(bruker["passord"].decode("UTF-8"),
                                          nav_passord)
    if not finnes:
        return am.jsonify({"msg": "Feil passord"})

    n_liste = {"fornavn": fornavn, "etternavn": etternavn, "email": email,
                "auth": auth_kode}

    for n in n_liste:
        if not n_liste[n]:
            n_liste[n] = bruker[n]

    am.bruker.update_one(
        {"email": nav_bruker},
        {
            "$set": {
                "fornavn": n_liste["fornavn"],
                "etternavn": n_liste["etternavn"],
                "email": n_liste["email"],
                "auth": n_liste["auth"]
            }
        }
    )

    if passord:
        ny_pass = am.bcrypt.generate_password_hash(passord.encode("UTF-8"))
        am.bruker.update_one(
            {"email": nav_bruker},
            {"$set": {"passord": ny_pass}}
        )

    return am.jsonify(
        {"msg": "ifnromasjon oppdatert"})


# formue
def grip_formue():
    bruker = am.bruker.find_one({"email": nav_bruker},
                                 {"konto": True, "konto.balance": True,
                                  "konto.konto_nummer": True})
    bruker.pop("_id")
    make_serializable(bruker)
    return am.jsonify(bruker)
    # idk hva som står over, kopiert fra tutorial

# Transaksjon
def transaksjon(yr, month):
    nav_bruker = am.get_jwt_identity()["email"]
    bruker = am.bruker.find_one({
        "email": nav_bruker},
        {"konto": True,
         "konto.konto_nummer": True,
         "konto.transaksjon": True})
    if not bruker:
        return am.jsonify({"msg": "bruker ikke funnet"})
    for item in bruker["konto"]:
        make_serializable(item)
    for konto in bruker["konto"]:
        kategori = [trans for trans in konto["transaksjon"]
                    if datetime.strptime(trans["time"], "%c").yr == yr
                    and datetime.strptime(trans["time"], "%c").month == month]
        konto["transaksjon"] = kategori
    return am.jsonify({"konto": bruker["konto"]}) # Stackoverflow


# grip transaksjon på konto
def grip_konto_transaksjon(konto, yr, month):
    nav_bruker = am.get_jwt_identity()["email"]
    bruker = am.bruker.find_one({
        "email": nav_bruker,
        "konto.konto_nummer": str(konto)},
        {"konto": {"$elemMatch": {"konto_nummer": str(konto)}},
         "konto.transaksjon": True})
    if not bruker:
        return am.jsonify({"msg": "konto ikke finnes"})
    transaksjon_list = bruker["konto"][0]["transaksjon"]
    # Stackoverflow

    for item in transaksjon_list:
        make_serializable(item)

    if not yr and not month:
        return am.jsonify({"transaksjon": transaksjon_list})

    kategori = [trans for trans in transaksjon_list
                if datetime.strptime(trans["time"], "%c").yr == yr]
    if yr and not month:
        return am.jsonify({"transaksjon": kategori})
    if yr and month:
        resultat = [trans for trans in kategori
                  if datetime.strptime(trans["time"], "%c").month == month]
        return am.jsonify({"transaksjon": resultat})
    return f"{yr}, {month}"


# Mer info!