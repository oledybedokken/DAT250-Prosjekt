import os
import io
import sys
from flask import send_file
from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify, Response
from flask_bcrypt import Bcrypt
from flask_session import Session
from database import Bruker, Kunder, Kundelog, Konto, Transactions
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime
import xlwt

app = Flask(__navn__)
bcrypt = Bcrypt(app)

app.secret_key = os.urandom(4) 
# Bytt til noe høyere når ferdig

# Setter databasen
engine = create_engine("sqlite:///database.db",connect_args={"check_same_thread": False},echo=True)
Base.metadata.bind = engine
db = scoped_session(sessionmaker(bind=engine))
    
# Hovedmeny
@app.route("/")
@app.route("/login")
def login():
    return render_template("Login.html", home=True)

@app.route("/registrer" , methods=["GET", "POST"])
def registrer():
    if "user" not in session:
        return redirect(url_for("login"))
    if session["brukertyp"] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("login"))
    if session["brukertyp"]=="executive":
        if request.method == "POST":
            ssn_kunde_id = int(request.form.get("ssn_kunde_id"))
            navn = request.form.get("navn")
            adresse = request.form.get("adresse")
            fylke = request.form.get("fylke")
            by = request.form.get("by")
            resultat = db.execute("SELECT * from kunder WHERE ssn_kunde_id = :c", {"c": ssn_kunde_id}).fetchone()
            if resultat is None :
                resultat = db.spor(kunder).count()
                if resultat == 0 :
                    spor = kunder(kunde_id=110110000, ssn_kunde_id=ssn_kunde_id, navn=navn, adresse=adresse, fylke=fylke, city=city, status="aktiv")
                else:
                    spor = kunder(ssn_kunde_id=ssn_kunde_id, navn=navn, adresse=adresse, fylke=fylke, by=by, status="aktiv")
                db.add(spor)
                db.commit()
                if spor.kunde_id is None:
                    flash("Data er ikke satt inn! Sjekk innspill.","fare")
                else:
                    temp = kundelog(kunde_id=spor.kunde_id,log_melding="Kundelaget")
                    db.add(temp)
                    db.commit()
                    flash(f"Kunde {spor.navn} er opprettet med kunde-ID: {spor.kunde_id}.", "suksess")
                    return redirect(url_for("se_kunder"))
            flash(f"SSN id : {ssn_kunde_id} is already present in database.", "advarsel")
        
    return render_template("addcustomer.html", addcustomer=True)

@app.route("/se_kunder/<kunde_id>")
@app.route("/se_kunder" , methods=["GET", "POST"])
def se_kunder(kunde_id=None):
    if "user" not in session:
        return redirect(url_for("login"))
    if session["brukertyp"] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("login"))
    if session["brukertyp"]=="executive":
        if request.method == "POST":
            ssn_kunde_id = request.form.get("ssn_kunde_id")
            kunde_id = request.form.get("kunde_id")
            data = db.execute("SELECT * from kunder WHERE kunde_id = :c or ssn_kunde_id = :d", {"c": kunde_id, "d": ssn_kunde_id}).fetchone()
            if data is not None:
                return render_template("se_kunder.html", se_kunder=True, data=data)
            
            flash("Kunden ble ikke funnet! Vennligst sjekk innspill.", "fare")
        elif kunde_id is not None:
            data = db.execute("SELECT * from kunder WHERE kunde_id = :c", {"c": kunde_id}).fetchone()
            if data is not None:
                return render_template("se_kunder.html", se_kunder=True, data=data)
            
            flash("Kunden ble ikke funnet! Vennligst sjekk innspill.", "fare")
    else:
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("login"))

    return render_template("se_kunder.html", se_kunder=True)

@app.route("/profilredigering")
@app.route("/profilredigering/<kunde_id>", methods=["GET", "POST"])
def profilredigering(kunde_id=None):
    if "user" not in session:
        return redirect(url_for("login"))
    if session["brukertyp"] != "executive":
        flash("Du har ikke tilgang til denne siden","advarsel")
        return redirect(url_for("login"))
    if session["brukertyp"]=="executive":
        if kunde_id is not None:
            if request.method != "POST":
                kunde_id = int(kunde_id)
                data = db.execute("SELECT * from kunder WHERE kunde_id = :c", {"c": kunde_id}).fetchone()
                if data is not None and data.status != "deaktivert":
                    return render_template("profilredigering.html", profilredigering=True, data=data)
                else:
                    flash("Kunden er deaktivert eller ikke til stede i databasen.","advarsel")
            else:
                kunde_id = int(kunde_id)
                navn = request.form.get("navn")
                adresse = request.form.get("adresse")
                resultat = db.execute("SELECT * from kunder WHERE kunde_id = :c and status = "aktiv"", {"c": kunde_id}).fetchone()
                if resultat is not None :
                    resultat = db.execute("UPDATE kunder SET navn = :n , adresse = :add , WHERE kunde_id = :a", {"n": navn,"add": adresse,"a": kunde_id})
                    db.commit()
                    temp = kundelog(kunde_id=kunde_id, log_melding="Kundedata er oppdatert")
                    db.add(temp)
                    db.commit()
                    flash(f"Kundedata er oppdatert.", "suksess")
                else:
                    flash("Ugyldig kunde-ID. Vennligst sjekk kunde-ID.", "advarsel")

    return redirect(url_for("se_kunder"))

@app.route("/slettkunde")
@app.route("/slettkunde/<kunde_id>")
def slettkunde(kunde_id=None):
    if "user" not in session:
        return redirect(url_for("login"))
    if session["brukertyp"] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("login"))
    if session["brukertyp"]=="executive":
        if kunde_id is not None:
            kunde_id = int(kunde_id)
            resultat = db.execute("SELECT * from kunder WHERE kunde_id = :a and status = "aktiv"", {"a": kunde_id}).fetchone()
            if resultat is not None :
                # delete from konto WHERE bruker_id = :a and konto_type=:at", {"a": bruker_id,"at":konto_type}
                spor = db.execute("UPDATE kunder SET status="deaktiv" WHERE kunde_id = :a", {"a": kunde_id})
                db.commit()
                temp = kundelog(kunde_id=kunde_id,log_melding="Kundedeaktiv")
                db.add(temp)
                db.commit()
                flash(f"Kune er deaktiv.", "suksess")
                return redirect(url_for("login"))
            else:
                flash(f"Kunde med id: {kunde_id} er allerede deaktivert eller ikke til stede i databasen.", "fare")
    return redirect(url_for("se_kunder"))

@app.route("/aktivkunde")
@app.route("/aktivkunde/<kunde_id>")
def aktivkunde(kunde_id=None):
    if "user" not in session:
        return redirect(url_for("login"))
    if session["brukertyp"] != "executive":
        flash("Du har ikke tilgang til denne siden","advarsel")
        return redirect(url_for("login"))
    if session["brukertyp"]=="executive":
        if kunde_id is not None:
            kunde_id = int(kunde_id)
            resultat = db.execute("SELECT * from kunder WHERE kunde_id = :a and status = "deaktiv"", {"a": kunde_id}).fetchone()
            if resultat is not None :
                spor = db.execute("UPDATE kunder SET status="aktiv" WHERE kunde_id = :a", {"a": kunde_id})
                db.commit()
                temp = kundelog(kunde_id=kunde_id,log_melding="Kunden er aktiv.")
                db.add(temp)
                db.commit()
                flash(f"Kunden er aktiv.", "suksess")
                return redirect(url_for("login"))
            flash(f"Kunde med id: {kunde_id} er allerede aktiv eller ikke til stede i databasen.", "advarsel")
    return redirect(url_for("se_kunder"))

@app.route("/aktivkunde")
@app.route("/aktivkunde/<bruker_id>")
def aktivkunde(bruker_id=None):
    if "user" not in session:
        return redirect(url_for("login"))
    if session["brukertyp"] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("login"))
    if session["brukertyp"]=="executive":
        if bruker_id is not None:
            bruker_id = int(bruker_id)
            resultat = db.execute("SELECT * from konto WHERE bruker_id = :a and status = "deactive"", {"a": bruker_id}).fetchone()
            if resultat is not None :
                date = datetime.datetime.now()
                spor = db.execute("UPDATE konto SET status="active", melding="Konto aktiv igjen", last_update = :d WHERE bruker_id = :a", {"d":date,"a": bruker_id})
                db.commit()
                flash(f"Kunden er aktiv.", "suksess")
                return redirect(url_for("login"))
            flash(f"Konto med id : {bruker_id} er allerede aktiv eller ikke til stede i databasen.", "advarsel")
    return redirect(url_for("se_kunder"))

@app.route("/kundestatus")
def kundestatus():
    if "user" not in session:
        return redirect(url_for("login"))
    if session["brukertyp"] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("login"))
    if session["brukertyp"]=="executive":
        # join spor to get one log melding per customer id
        data = db.execute("SELECT kunder.kunde_id as id, kunder.ssn_kunde_id as ssn_id, kundelog.log_melding as melding, kundelog.time_stamp as date from (select kunde_id,log_melding,time_stamp from kundelog group by kunde_id ORDER by time_stamp desc) as kundelog JOIN kunder ON kunder.kunde_id = kundelog.kunde_id group by kundelog.kunde_id order by kundelog.time_stamp desc").fetchall()
        if data:
            return render_template("kundestatus.html", kundestatus=True , data=data)
        else:
            flash("Ingen data funnet.", "fare")
    return redirect(url_for("login"))

@app.route("/settinkonto" , methods=["GET", "POST"])
def settinkonto():
    if "user" not in session:
        return redirect(url_for("login"))
    if session["brukertyp"] != "executive":
        flash("Du har ikke tilgang til denne siden","advarsel")
        return redirect(url_for("login"))
    if session["brukertyp"]=="executive":
        if request.method == "POST":
            kunde_id = int(request.form.get("kunde_id"))
            konto_type = request.form.get("konto_type")
            belop= float(request.form.get("belop"))
            melding = "Account vellykket created"
            resultat = db.execute("SELECT * from kunder WHERE kunde_id = :c", {"c": kunde_id}).fetchone()
            if resultat is not None :
                resultat = db.execute("SELECT * from konto WHERE kunde_id = :c and konto_type = :at", {"c": kunde_id, "at": konto_type}).fetchone()
                if resultat is None:
                    resultat = db.spor(konto).count()
                    if resultat == 0 :
                        spor = konto(bruker_id=360110000, konto_type=konto_type, balance=belop, kunde_id=kunde_id, status="active", melding=melding, last_update=datetime.datetime.now())
                    else:
                        spor = konto(konto_type=konto_type, balance=belop,kunde_id=kunde_id, status="active", melding=melding, last_update=datetime.datetime.now())
                    db.add(spor)
                    db.commit()
                    if spor.bruker_id is None:
                        flash("Data er ikke satt inn! Sjekk innspillene dine.", "fare")
                    else:
                        flash(f"{spor.konto_type} kontoen opprettes med kunde-ID : {spor.bruker_id}.", "suksess")
                        return redirect(url_for("login"))
                else:
                    flash(f"Kunde med id: {kunde_id} har allerede {konto_type} konto.", "advarsel")
            else:
                flash(f"Kunde med id: {kunde_id} er ikke til stede i databasen.", "advarsel")

    return render_template("settinkonto.html", settinkonto=True)

@app.route("/slettkonto" , methods=["GET", "POST"])
def slettkonto():
    if "user" not in session:
        return redirect(url_for("login"))
    if session["brukertyp"] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("login"))
    if session["brukertyp"]=="executive":
        if request.method == "POST":
            bruker_id = int(request.form.get("bruker_id"))
            resultat = db.execute("SELECT * from konto WHERE bruker_id = :a and status="active"", {"a": bruker_id}).fetchone()
            if resultat is not None :
                # delete from konto WHERE bruker_id = :a and konto_type=:at", {"a": bruker_id,"at":konto_type}
                melding = "Konto deaktivert"
                dato = datetime.datetime.now()
                spor = db.execute("UPDATE konto SET status="deactive", melding= :m, last_update = :d WHERE bruker_id = :a;", {"m":melding,"d":dato,"a": bruker_id})
                db.commit()
                flash(f"Customer account is Deaktivd vellykket.","suksess")
                return redirect(url_for("login"))
            flash(f"Account with id : {bruker_id} is already deaktiv or account not found.", "advarsel")
    return render_template("slettkonto.html", slettkonto=True)

@app.route("/se_kunder" , methods=["GET", "POST"])
def se_kunder():
    if "user" not in session:
        return redirect(url_for("login"))        
    if session["brukertyp"]=="executive" or session["brukertyp"]=="teller" or session["brukertyp"]=="cashier":
        if request.method == "POST":
            bruker_id = request.form.get("bruker_id")
            kunde_id = request.form.get("kunde_id")
            data = db.execute("SELECT * from konto WHERE kunde_id = :c or bruker_id = :d", {"c": kunde_id, "d": bruker_id}).fetchall()
            if data:
                return render_template("se_kunder.html", se_kunder=True, data=data)
            
            flash("Konto ikke funnet! Vennligst sjekk innspillene dine.", "fare")
    else:
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("login"))
    return render_template("se_kunder.html", se_kunder=True)


@app.route("/se_kontostatus" , methods=["GET", "POST"])
def se_kontostatus():
    if "user" not in session:
        return redirect(url_for("login"))
    if session["brukertyp"] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("login"))
    if session["brukertyp"]=="executive":
        data = db.execute("select * from konto").fetchall()
        if data:
            return render_template("se_kontostatus.html", se_kontostatus=True, data=data)
        else:
            flash("konto ikke funnet!", "fare")
    return render_template("se_kontostatus.html", se_kontostatus=True)

# Code for inskudd belop 
@app.route("/inskudd", methods=["GET","POST"])
@app.route("/inskudd/<bruker_id>", methods=["GET","POST"])
def inskudd(bruker_id=None):
    if "user" not in session:
        return redirect(url_for("login"))
    if session["brukertyp"] == "executive":
        flash("Du har ikke tilgang til denne siden","advarsel")
        return redirect(url_for("login"))
    if session["brukertyp"]=="teller" or session["brukertyp"]=="cashier":
        if bruker_id is None:
            return redirect(url_for("se_kunder"))
        else:
            if request.method == "POST":
                belop = request.form.get("belop")
                data = db.execute("select * from konto where bruker_id = :a and status="active"",{"a":bruker_id}).fetchone()
                if data is not None:
                    balance = int(belop) + int(data.balance)
                    spor = db.execute("UPDATE konto SET balance= :b WHERE bruker_id = :a", {"b":balance,"a": data.bruker_id})
                    db.commit()
                    flash(f"{belop} beløp deponert på konto: {data.bruker_id} vellykket.","suksess")
                    temp = transaksjoner(bruker_id=data.bruker_id,trans_melding="Beløp innskudd", belop=belop)
                    db.add(temp)
                    db.commit()
                else:
                    flash(f"Kontoen ble ikke funnet eller inaktiv.", "fare")
            else:
                data = db.execute("select * from konto where bruker_id = :a",{"a":bruker_id}).fetchone()
                if data is not None:
                    return render_template("Betaling.html", betaling=True, data=data)
                else:
                    flash(f"Kontoen ble ikke funnet eller inaktiv.", "fare")

    return redirect(url_for("login"))

# Code for overforing belop 
@app.route("/overforing",methods=["GET","POST"])
@app.route("/overforing/<kunde_id>",methods=["GET","POST"])
def overforing(kunde_id=None):
    if "user" not in session:
        return redirect(url_for("login"))
    if session["brukertyp"] == "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("login"))
    if session["brukertyp"]=="teller" or session["brukertyp"]=="cashier":
        if kunde_id is None:
            return redirect(url_for("se_kunder"))
        else:
            if request.method == "POST":
                src_type = request.form.get("src_type")
                trg_type = request.form.get("trg_type")
                belop = int(request.form.get("belop"))
                if src_type != trg_type:
                    src_data  = db.execute("select * from konto where kunde_id = :a and konto_type = :t and status="active"",{"a":kunde_id,"t":src_type}).fetchone()
                    til_data  = db.execute("select * from konto where kunde_id = :a and konto_type = :t and status="active"",{"a":kunde_id,"t":trg_type}).fetchone()
                    if src_data is not None and til_data is not None:
                        if src_data.balance > belop:
                            src_balance = src_data.balance - belop
                            trg_balance = til_data.balance + belop
                            
                            test = db.execute("update konto set balance = :b where kunde_id = :a and konto_type = :t",{"b":src_balance,"a":kunde_id,"t":src_type})
                            db.commit()
                            temp = transaksjoner(bruker_id=src_data.bruker_id,trans_melding="belop overført til "+ str(til_data.bruker_id),belop=belop)
                            db.add(temp)
                            db.commit()

                            db.execute("update konto set balance = :b where kunde_id = :a and konto_type = :t",{"b":trg_balance,"a":kunde_id,"t":trg_type})
                            db.commit()
                            temp = transaksjoner(bruker_id=til_data.bruker_id,trans_melding="belop mottatt fra "+ str(src_data.bruker_id), belop=belop)
                            db.add(temp)
                            db.commit()

                            flash(f"belop overført til {til_data.bruker_id} fra {src_data.bruker_id} vellykket", "suksess")
                        else:
                            flash("Utilstrekkelig beløp å overføre", "fare")
                            
                    else:
                        flash("konto ikke funnet", "fare")

                else:
                    flash("Kan ikke overføre til samme konto", "advarsel")

            else:
                data = db.execute("select * from konto where kunde_id = :a",{"a":kunde_id}).fetchall()
                if data and len(data) == 2:
                    return render_template("Betaling.html", betaling=True, kunde_id=kunde_id)
                else:
                    flash("Data ikke funnet eller ugyldig kunde-ID", "fare")
                    return redirect(url_for("se_kunder"))

    return redirect(url_for("login"))

# code for view account statment based on the account id
# Using nummer of last transaction
# or 
# Using Specified date duration
@app.route("/betaling" , methods=["GET", "POST"])
def betaling():
    if "user" not in session:
        return redirect(url_for("login"))
    if session["brukertyp"] == "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("login"))       
    if session["brukertyp"]=="teller" or session["brukertyp"]=="cashier":
        if request.method == "POST":
            bruker_id = request.form.get("bruker_id")
            nummer = request.form.get("nummer")
            flag = request.form.get("Radio")
            start_date = request.form.get("start_date")
            end_date = request.form.get("end_date")
            if flag=="red":
                data = db.execute("SELECT * FROM (SELECT * FROM transaksjoner where bruker_id=:d ORDER BY trans_id DESC LIMIT :l)Var1 ORDER BY trans_id ASC;", {"d": bruker_id,"l":nummer}).fetchall()
            else:
                data = db.execute("SELECT * FROM transaksjoner WHERE bruker_id=:a between DATE(time_stamp) >= :s AND DATE(time_stamp) <= :e;",{"a":bruker_id,"s":start_date,"e":end_date}).fetchall()
            if data:
                return render_template("Betaling.html", betaling=True, data=data, bruker_id=bruker_id)
            else:
                flash("Ingen transaksjoner", "fare")
                return redirect(url_for("login"))
    else:
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("login"))
    return render_template("Betaling.html", betaling=True)

# route for 404 error
@app.errorhandler(404)
def not_found(e):
  return render_template("404.html") 

# avlogging 
@app.route("/avlogging")
def avlogging():
    session.pop("user", None)
    return redirect(url_for("login"))

# innlogging
@app.route("/innlogging", methods=["GET", "POST"])
def innlogging():
    if "user" in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        email = request.form.get("email").upper()
        passord = request.form.get("passord").encode("utf-8")
        resultat = db.execute("SELECT * FROM users WHERE id = :u", {"u": email}).fetchone()
        if resultat is not None:
            if bcrypt.check_password_hash(resultat["passord"], passord) is True:
                session["email"] = email
                session["navn"] = resultat.navn
                session["brukertyp"] = resultat.bruker_type
                flash(f"{resultat.navn.capitalize()}, du er innlogget!", "suksess")
                return redirect(url_for("login"))
        flash("Beklager, email eller password er feil.", "fare")
    return render_template("Login.html", login=True)

# Api
@app.route("/api")
@app.route("/api/v1")
def api():
    return """
    <h2>List of Api</h2>
    <ol>
        <li>
            <a href="/api/v1/kundelog">Kunde Log</a>
            <a href="/api/v1/kontolog">Konto log</a>
        </li>
    </ol>
    """

@app.route("/kundelog", methods=["GET", "POST"])
@app.route("/api/v1/kundelog", methods=["GET", "POST"])
def kundelog():
    if "user" not in session:
        flash("Vennligst logg inn", "advarsel")
        return redirect(url_for("login"))
    if session["brukertyp"] != "executive":
        flash("Du har ikke tilgang til denne api", "advarsel")
        return redirect(url_for("login"))
    if session["brukertyp"]=="executive":
        if request.method == "POST":
            kunde_id = request.json["kunde_id"]
            data = db.execute("select log_melding,time_stamp from kundelog where kunde_id= :c ORDER by time_stamp desc",{"c":kunde_id}).fetchone()
            t = {
                    "melding" : data.log_melding,
                    "dato" : data.time_stamp
                }
            return jsonify(t)
        else:
            dict_data = []
            data = db.execute("SELECT kunder.kunde_id as id, kunder.ssn_kunde_id as ssn_id, kundelog.log_melding as melding, kundelog.time_stamp as date from kundelog JOIN kunder ON kunder.kunde_id = kundelog.kunde_id order by kundelog.time_stamp desc limit 50").fetchall()
            for row in data:
                t = {
                    "id" : row.id,
                    "ssn_id" : row.ssn_id,
                    "melding" : row.melding,
                    "dato" : row.dato
                }
                dict_data.append(t)
            return jsonify(dict_data)

@app.route("/kontolog", methods=["GET", "POST"])
@app.route("/api/v1/kontolog", methods=["GET", "POST"])
def kontolog():
    if "user" not in session:
        flash("Venligst, logg inn", "advarsel")
        return redirect(url_for("login"))
    if session["brukertyp"] != "executive":
        flash("Du har ikke tilgang til denne api", "advarsel")
        return redirect(url_for("login"))
    if session["brukertyp"]=="executive":
        if request.method == "POST":
            bruker_id = request.json["bruker_id"]
            data = db.execute("select status,melding,last_update as time_stamp from konto where bruker_id= :c;",{"c":bruker_id}).fetchone()
            t = {
                    "status" : data.status,
                    "melding" : data.melding,
                    "dato" : data.time_stamp
                }
            return jsonify(t)
        else:
            dict_data = []
            data = db.execute("SELECT kunde_id, bruker_id, konto_type, status, melding, last_update from konto limit 50").fetchall()
            for row in data:
                t = {
                    "kunde_id" : row.kunde_id,
                    "bruker_id" : row.bruker_id,
                    "konto_type" : row.konto_type,
                    "status" : row.status,
                    "melding" : row.melding,
                    "dato" : row.last_update
                }
                dict_data.append(t)
            return jsonify(dict_data)
    

# Bytt på secret key. 
if __navn__ == "__main__":
    app.secret_key = "admin123"
    app.debug = True
    app.run(host="0.0.0.0", port=5000)