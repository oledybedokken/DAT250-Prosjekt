from .. import alle_moduler as am
from .views import uttak

# Overforing
def transfer():
    data = am.request.get_json()

    if not data:
        return am.make_response("OBS! Ingen data")
    try:
        konto_fra = data["konto_fra"]
        konto_til = data["konto_til"]
        sum_mengde = data["sum_mengde"]
    except KeyError:
        return am.jsonify({"msg": "OBS! Sjekk om stavefeil"})

    if not isinstance(sum_mengde, float) and not isinstance(sum_mengde, int):
        return am.jsonify({"msg": "uvanlig input"})

    sum_mengde = round(sum_mengde, 3) # test

    konto_fra = str(konto_fra)
    konto_til = str(konto_til)
    sum_mengde = abs(sum_mengde)

    if str(konto_fra) == str(konto_til):
        return am.jsonify({"msg": "kan ikke være samme konto"})

    if not am.clients.find_one({"bruker.konto_nummer": konto_fra}) or \
            not \
            am.clients.find_one({"bruker.konto_nummer": konto_til}):
        return am.jsonify({"msg": "konto ikke finnes"})

    nav_bruker = am.get_jwt_identity()["email"]

    melding_fra = f"Overført til {konto_til[-4:]}"
    bruker_fra = withdraw(nav_bruker, konto_fra, sum_mengde,
                        melding_fra)
    if not bruker_fra:
        return am.jsonify({"msg": "kunne ikke overføre til konto"})

    melding_til = f"Overført fra {konto_fra[-4:]}"
    if konto_til[0] == "4":
        melding_til = melding_til
    til_konto = deposit({"$exists": True}, konto_til, sum_mengde, melding_til)

    return am.jsonify(
        {"fra": konto_fra, "til": konto_til, "sum_mengde": sum_mengde})