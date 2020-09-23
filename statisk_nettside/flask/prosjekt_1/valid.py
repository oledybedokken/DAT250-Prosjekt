from .. import alle_moduler as am

# Innlogging
def innlogging():
    data = am.request.get_json()
    if not data:
        return am.jsonify({"msg": "OBS! Ingen data"})

    try:
        email = data["email"]
        passord = data["passord"]
    except KeyError:
        return am.jsonify({"msg": "OBS! Sjekk om stavefeil"})

    if not isinstance(email, str) or not isinstance(passord, str):
        return am.jsonify({"msg": "Feil input"})

    bruker = am.bruker.find_one({"email": email})

    if not bruker:
        return am.jsonify({"msg": "Feil email/passord"})

    finnes = am.bcrypt.check_password_hash(bruker["passord"].decode("UTF-8"),
                                          passord)
    if not finnes:
        return am.jsonify({"msg": "Feil email/passord"})

# Bytt passord
def bytt_passord():
    data = am.request.get_json()
    if not data:
        return am.jsonify({"msg": "OBS! Ingen data"})
    try:
        email = data["email"]
        auth_kode = data["auth_kode"]
        ny_pass = data["passord"]
    except KeyError:
        return am.jsonify({"msg": "OBS! Sjekk om stavefeil"})

    bruker = am.bruker.find_one({"$og": [{"email": email}]})
    if not bruker:
        return am.jsonify({"msg": "Invalid information"})

    ny_hash = am.bcrypt.generate_password_hash(newpw.encode("UTF-8"))
    resultat = am.bruker.update_one({"email": email},
                                   {"$set": {"passord": ny_hash}})
    if not result.modified_count:
        return am.jsonify({"msg": "Failed to update"})

    return am.jsonify({"msg": "passord changed successful"})

# Avlogging
def avlogging():
    # Skriv her!
    return am.jsonify({"msg": "Du har avlogget!"})
