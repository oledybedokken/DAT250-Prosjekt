from .. import alle_moduler as am
from .views import uttak
import re

uttak_bp = am.Blueprint("uttak", __name__)

# Fortsett!

def uttak_til():
    data = am.request.get_json()

    if not data:
        return am.make_response("OBS! Ingen data")
    try:
        sum_mengde = data["sum_mengde"]
        konto_nummer = str(data["konto_nummer"])
    except KeyError:
        return am.make_response("OBS! Sjekk om stavefeil")

    if (not isinstance(sum_mengde, float) and not isinstance(sum_mengde, int)) or not \
            isinstance(konto_nummer, str):
        return am.jsonify({"msg": "uvanlig inpit"})

    if not am.finnes(konto_nummer) or not konto_nummer:
        return am.jsonify({"msg": "tomt konto felt"})

    nav_bruker = am.get_jwt_identity()["email"]
    melding = "<melding>" if konto_nummer[0] == "4" else "uttak"
    oppdater_bruker = deposit(nav_bruker, konto_nummer, sum_mengde, melding)

    if not oppdater_bruker:
        return am.jsonify({"msg": "brukeren eier ikke konto"})
    for_konto = next(acc for acc in oppdater_bruker[
        "accounts"] if acc["konto_nummer"] == str(konto_nummer))
    slutt_mengde = for_konto["balance"]
    return am.jsonify({"email": nav_bruker, "sum_mengde": sum_mengde,
                       "slutt_mengde": float(slutt_mengde.to_decimal()),
                       "konto_nummer": konto_nummer})