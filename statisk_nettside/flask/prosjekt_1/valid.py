from .. import alle_moduler as am

# Innlogging
def innlogging():
    data = am.request.get_json()
    if not data:
        return am.jsonify({"msg": "OBS! Ingen data"}), 400

    try:
        email = data["email"]
        passord = data["passord"]
    except KeyError:
        return am.jsonify({"msg": "OBS! Sjekk om stavefeil"}), 400

    if not isinstance(email, str) or not isinstance(passord, str):
        return am.jsonify({"msg": "Feil input"}), 400

    bruker = am.bruker.find_one({"email": email})

    if not bruker:
        return am.jsonify({"msg": "Feil email/passord"}), 409

    finnes = am.bcrypt.check_password_hash(bruker["passord"].decode("UTF-8"),
                                          passord)
    if not finnes:
        return am.jsonify({"msg": "Feil email/passord"}), 409

# Bytt passord
def bytt_passord():
    data = am.request.get_json()
    if not data:
        return am.jsonify({"msg": "OBS! Ingen data"}), 400
    try:
        email = data["email"]
        auth_kode = data["auth_kode"]
        newpw = data["passord"]
    except KeyError:
        return am.jsonify({"msg": "OBS! Sjekk om stavefeil"}), 400

    bruker = am.bruker.find_one({"$og": [{"email": email}]})
    if not bruker:
        return am.jsonify({"msg": "Invalid information"}), 409

    ny_hash = am.bcrypt.generate_password_hash(newpw.encode("UTF-8"))
    resultat = am.bruker.update_one({"email": email},
                                   {"$set": {"passord": new_hash}})
    if not result.modified_count:
        return am.jsonify({"msg": "Failed to update"}), 503

    return am.jsonify({"msg": "passord changed successful"}), 200

# Avlogging
def avlogging():
    # Skriv her!
    return am.jsonify({"msg": "Du har avlogget!"}), 200