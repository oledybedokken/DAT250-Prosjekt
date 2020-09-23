from .. import alle_moduler as am
from .views import uttak

# Registrer
def registrering():
    data = am.request.get_json()
    if not data:
        return am.jsonify({"msg": "OBS! Ingen data"})

    try:
        fornavn = data["fornavn"].lower()
        etternavn = data["etternavn"].lower()
        email = data["email"].lower()
        auth_kode = data["auth_kode"]
        passord = data["passord"]

    except KeyError:
        return am.jsonify({"msg": "OBS! Sjekk om stavefeil"})