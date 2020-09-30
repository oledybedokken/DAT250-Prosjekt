import os
import io
import sys
from flask import send_file
from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify, Response
from flask_bcrypt import Bcrypt
from flask_session import Session
from database import Base, Konto, Bruker, Kunder, KundeLog, Transaksjoner
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime
import xlwt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.urandom(4) # Bytt til noe høyere når ferdig

# Setter databasen.
engine = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False}, echo=True)
Base.metadata.bind = engine
db = scoped_session(sessionmaker(bind=engine))
    
# Hovedmeny
@app.route("/")
@app.route("/hovedmeny")
def hovedmeny():
    return render_template("login.html", login=True)

@app.route("/lagkunde" , methods=["GET", "POST"])
def lagkunde():
    if "user" not in session:
        return redirect(url_for("innlogging"))
    if session["usert"] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("hovedmeny"))
    if session["usert"]=="executive":
        if request.method == "POST":
            ssn_kunde_id = int(request.form.get("ssn_kunde_id"))
            navn = request.form.get("navn")
            adresse = request.form.get("adresse")
            fylke = request.form.get("fylke")
            by = request.form.get("by")
            resultat = db.execute("SELECT * from kunder WHERE ssn_kunde_id = :c", {"c": ssn_kunde_id}).fetchone()
            if resultat is None :
                resultat = db.spor(Kunder).count()
                if resultat == 0 :
                    spor = Kunder(kunde_id=110110000, ssn_kunde_id=ssn_kunde_id, navn=navn, adresse=adresse, fylke=fylke, by=by, status="activate")
                else:
                    spor = Kunder(ssn_kunde_id=ssn_kunde_id, navn=navn, adresse=adresse, fylke=fylke, by=by, status="activate")
                db.add(spor)
                db.commit()
                if spor.kunde_id is None:
                    flash("Data er ikke satt inn! Sjekk om det er riktig.","fare")
                else:
                    temp = KundeLog(kunde_id=spor.kunde_id, melding_log="Kundelaget")
                    db.add(temp)
                    db.commit()
                    flash(f"Kunde {spor.navn} er opprettet med kunde-ID: {spor.kunde_id}.", "vellykket")
                    return redirect(url_for("se_kunder"))
            flash(f"SSN-ID : {ssn_kunde_id} er allerede i databasen.", "advarsel")
        
    return render_template("lagkunde.html", lagkunde=True)

@app.route("/se_kunder/<kunde_id>")
@app.route("/se_kunder" , methods=["GET", "POST"])
def se_kunder(kunde_id=None):
    if "user" not in session:
        return redirect(url_for("innlogging"))
    if session["usert"] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("hovedmeny"))
    if session["usert"]=="executive":
        if request.method == "POST":
            ssn_kunde_id = request.form.get("ssn_kunde_id")
            kunde_id = request.form.get("kunde_id")
            data = db.execute("SELECT * from kunder WHERE kunde_id = :c or ssn_kunde_id = :d", {"c": kunde_id, "d": ssn_kunde_id}).fetchone()
            if data is not None:
                return render_template("se_kunder.html", se_kunder=True, data=data)
            
            flash("Kunden ble ikke funnet! Sjekk om det er riktig.", "fare")
        elif kunde_id is not None:
            data = db.execute("SELECT * from kunder WHERE kunde_id = :c", {"c": kunde_id}).fetchone()
            if data is not None:
                return render_template("se_kunder.html", se_kunder=True, data=data)
            
            flash("Kunden ble ikke funnet! Sjekk om det er riktig.", "fare")
    else:
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("hovedmeny"))

    return render_template("se_kunder.html", se_kunder=True)

@app.route("/redigerkunde")
@app.route("/redigerkunde/<kunde_id>", methods=["GET", "POST"])
def redigerkunde(kunde_id=None):
    if "user" not in session:
        return redirect(url_for("innlogging"))
    if session["usert"] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("hovedmeny"))
    if session["usert"]=="executive":
        if kunde_id is not None:
            if request.method != "POST":
                kunde_id = int(kunde_id)
                data = db.execute("SELECT * from kunder WHERE kunde_id = :c", {"c": kunde_id}).fetchone()
                if data is not None and data.status != "deactivate":
                    return render_template("redigerkunde.html", redigerkunde=True, data=data)
                else:
                    flash("Kunden er ikke aktiv eller ikke til stede i databasen.","advarsel")
            else:
                kunde_id = int(kunde_id)
                navn = request.form.get("navn")
                adresse = request.form.get("adresse")
                resultat = db.execute("SELECT * from kunder WHERE kunde_id = :c and status = 'activate'", {"c": kunde_id}).fetchone()
                if resultat is not None :
                    resultat = db.execute("UPDATE kunder SET navn = :n , adresse = :add , WHERE kunde_id = :a", {"n": navn, "add": adresse, "a": kunde_id})
                    db.commit()
                    temp = KundeLog(kunde_id=kunde_id, melding_log="Kundedata er oppdatert")
                    db.add(temp)
                    db.commit()
                    flash(f"Kundedata er oppdatert.", "vellykket")
                else:
                    flash("Ugyldig kunde-ID. Vennligst sjekk kunde-ID.", "advarsel")

    return redirect(url_for("se_kunder"))

@app.route("/slettkunde")
@app.route("/slettkunde/<kunde_id>")
def slettkunde(kunde_id=None):
    if "user" not in session:
        return redirect(url_for("innlogging"))
    if session["usert"] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("hovedmeny"))
    if session["usert"]=="executive":
        if kunde_id is not None:
            kunde_id = int(kunde_id)
            resultat = db.execute("SELECT * from kunder WHERE kunde_id = :a and status = 'activate'", {"a": kunde_id}).fetchone()
            if resultat is not None :
                spor = db.execute("UPDATE kunder SET status='deactivate' WHERE kunde_id = :a", {"a": kunde_id})
                db.commit()
                temp = KundeLog(kunde_id=kunde_id,melding_log="Kundedeaktiv")
                db.add(temp)
                db.commit()
                flash(f"Kunde er ikke aktiv.", "vellykket")
                return redirect(url_for("hovedmeny"))
            else:
                flash(f"Kunde med ID: {kunde_id} er allerede deaktivert eller ikke til stede i databasen.", "fare")
    return redirect(url_for("se_kunder"))

@app.route("/aktiverkunde")
@app.route("/aktiverkunde/<kunde_id>")
def aktiverkunde(kunde_id=None):
    if "user" not in session:
        return redirect(url_for("innlogging"))
    if session["usert"] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("hovedmeny"))
    if session["usert"]=="executive":
        if kunde_id is not None:
            kunde_id = int(kunde_id)
            resultat = db.execute("SELECT * from kunder WHERE kunde_id = :a and status = 'deactivate'", {"a": kunde_id}).fetchone()
            if resultat is not None :
                spor = db.execute("UPDATE kunder SET status='activate' WHERE kunde_id = :a", {"a": kunde_id})
                db.commit()
                temp = KundeLog(kunde_id=kunde_id,melding_log="Kunden er aktiv.")
                db.add(temp)
                db.commit()
                flash(f"Kunden er aktiv.", "vellykket")
                return redirect(url_for("hovedmeny"))
            flash(f"Kunde med id: {kunde_id} er allerede aktiv eller ikke til stede i databasen.", "advarsel")
    return redirect(url_for("se_kunder"))

@app.route("/aktiverkonto")
@app.route("/aktiverkonto/<bruker_id>")
def aktiverkonto(bruker_id=None):
    if "user" not in session:
        return redirect(url_for("innlogging"))
    if session["usert"] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("hovedmeny"))
    if session["usert"]=="executive":
        if bruker_id is not None:
            bruker_id = int(bruker_id)
            resultat = db.execute("SELECT * from konto WHERE bruker_id = :a and status = 'deactivate'", {"a": bruker_id}).fetchone()
            if resultat is not None :
                date = datetime.datetime.now()
                spor = db.execute("UPDATE konto SET status='active', melding='Konto aktiv igjen', last_update = :d WHERE bruker_id = :a", {"d":date,"a": bruker_id})
                db.commit()
                flash(f"Kunden er aktiv.", "vellykket")
                return redirect(url_for("hovedmeny"))
            flash(f"Konto med id : {bruker_id} er allerede aktiv eller ikke til stede i databasen.", "advarsel")
    return redirect(url_for("se_kunder"))

@app.route("/kundestatus")
def kundestatus():
    if "user" not in session:
        return redirect(url_for("innlogging"))
    if session["usert"] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("hovedmeny"))
    if session["usert"]=="executive":
        data = db.execute("SELECT kunder.kunde_id as id, kunder.ssn_kunde_id as ssn_id, kundelog.melding_log as melding, kundelog.time_stamp as date from (SELECT kunde_id,melding_log,time_stamp from kundelog group by kunde_id ORDER by time_stamp desc) as kundelog JOIN kunder ON kunder.kunde_id = kundelog.kunde_id group by kundelog.kunde_id order by kundelog.time_stamp desc").fetchall()
        if data:
            return render_template("kontostatus.html", kundestatus=True , data=data)
        else:
            flash("Ingen data er funnet.", "fare")
    return redirect(url_for("hovedmeny"))

@app.route("/lagkonto" , methods=["GET", "POST"])
def lagkonto():
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for('hovedmeny'))
    if session['usert']=="executive":
        if request.method == "POST":
            kunde_id = int(request.form.get("kunde_id"))
            bruker_type = request.form.get("bruker_type")
            belop= float(request.form.get("belop"))
            melding = "Bruker skapelse er vellykket"
            resultat = db.execute("SELECT * from kunder WHERE kunde_id = :c", {"c": kunde_id}).fetchone()
            if resultat is not None :
                resultat = db.execute("SELECT * from konto WHERE kunde_id = :c and bruker_type = :at", {"c": kunde_id, "at": bruker_type}).fetchone()
                if resultat is None:
                    resultat = db.spor(Konto).count()
                    if resultat == 0 :
                        spor = Konto(bruker_id=360110000, bruker_type=bruker_type, saldo=belop, kunde_id=kunde_id, status='active', melding=melding, last_update=datetime.datetime.now())
                    else:
                        spor = Konto(bruker_type=bruker_type,saldo=belop,kunde_id=kunde_id,status='active',melding=melding,last_update=datetime.datetime.now())
                    db.add(spor)
                    db.commit()
                    if spor.bruker_id is None:
                        flash("Data er ikke satt inn! Sjekk om informasjon er riktig", "fare")
                    else:
                        flash(f"{spor.bruker_type} konto er skapt med konto-ID : {spor.bruker_id}.", "vellykket")
                        return redirect(url_for('hovedmeny'))
                else:
                    flash(f"Kunde med ID : {kunde_id} har allerede {bruker_type} konto.", "advarsel")
            else:
                flash(f"Kunde med id: {kunde_id} er ikke til stede i databasen.", "advarsel")

    return render_template('lagkonto.html', lagkonto=True)


@app.route("/slettkonto" , methods=["GET", "POST"])
def slettkonto():
    if "user" not in session:
        return redirect(url_for("innlogging"))
    if session["usert"] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("hovedmeny"))
    if session["usert"]=="executive":
        if request.method == "POST":
            bruker_id = int(request.form.get("bruker_id"))
            resultat = db.execute("SELECT * from konto WHERE bruker_id = :a and status='active'", {"a": bruker_id}).fetchone()
            if resultat is not None :
                melding = "Konto er deaktivert"
                date = datetime.datetime.now()
                spor = db.execute("UPDATE konto SET status='deactive', melding= :m, last_update = :d WHERE bruker_id = :a;", {"m":melding, "d":date, "a": bruker_id})
                db.commit()
                flash(f"Kunde er deaktivert.", "vellykket")
                return redirect(url_for("hovedmeny"))
            flash(f"Bruker med ID : {bruker_id} er allerede deaktiv eller ikke funnet.", "advarsel")
    return render_template("slettkonto.html", slettkonto=True)

@app.route("/sekunder" , methods=["GET", "POST"])
def sekunder():
    if "user" not in session:
        return redirect(url_for("innlogging"))        
    if session["usert"]=="executive" or session["usert"]=="teller" or session["usert"]=="cashier":
        if request.method == "POST":
            bruker_id = request.form.get("bruker_id")
            kunde_id = request.form.get("kunde_id")
            data = db.execute("SELECT * from konto WHERE kunde_id = :c or bruker_id = :d", {"c": kunde_id, "d": bruker_id}).fetchall()
            if data:
                return render_template("se_kunder.html", sekunder=True, data=data)
            
            flash("Konto ikke funnet! Vennligst sjekk om informasjon er riktig", "fare")
    else:
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("hovedmeny"))
    return render_template("se_kunder.html", sekunder=True)


@app.route("/kontostatus" , methods=["GET", "POST"])
def kontostatus():
    if "user" not in session:
        return redirect(url_for("innlogging"))
    if session["usert"] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("hovedmeny"))
    if session["usert"]=="executive":   
        data = db.execute("SELECT * from konto").fetchall()
        if data:
            return render_template("kontostatus.html", kontostatus=True, data=data)
        else:
            flash("konto ikke funnet!", "fare")
    return render_template("kontostatus.html", kontostatus=True)

# Code for innskudd belop 
@app.route("/innskudd", methods=["GET","POST"])
@app.route("/innskudd/<bruker_id>", methods=["GET","POST"])
def innskudd(bruker_id=None):
    if "user" not in session:
        return redirect(url_for("innlogging"))
    if session["usert"] == "executive":
        flash("Du har ikke tilgang til denne siden","advarsel")
        return redirect(url_for("hovedmeny"))
    if session["usert"]=="teller" or session["usert"]=="cashier":
        if bruker_id is None:
            return redirect(url_for("se_kunder"))
        else:
            if request.method == "POST":
                belop = request.form.get("belop")
                data = db.execute("SELECT * from konto where bruker_id = :a and status='active'", {"a":bruker_id}).fetchone()
                if data is not None:
                    saldo = int(belop) + int(data.saldo)
                    spor = db.execute("UPDATE konto SET saldo = :b WHERE bruker_id = :a", {"b":saldo,"a": data.bruker_id})
                    db.commit()
                    flash(f"{belop} beløp deponert på konto: {data.bruker_id} vellykket.","vellykket")
                    temp = Transaksjoner(bruker_id=data.bruker_id, trans_melding="Beløp innskudd", belop=belop)
                    db.add(temp)
                    db.commit()
                else:
                    flash(f"Kontoen ble ikke funnet eller er inaktiv.", "fare")
            else:
                data = db.execute("SELECT * from konto where bruker_id = :a", {"a":bruker_id}).fetchone()
                if data is not None:
                    return render_template("Betaling.html", betaling=True, data=data)
                else:
                    flash(f"Kontoen ble ikke funnet eller er inaktiv.", "fare")

    return redirect(url_for("hovedmeny"))

# Code for overforing belop 
@app.route("/overforing",methods=["GET","POST"])
@app.route("/overforing/<kunde_id>",methods=["GET","POST"])
def overforing(kunde_id=None):
    if "user" not in session:
        return redirect(url_for("innlogging"))
    if session["usert"] == "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("hovedmeny"))
    if session["usert"]=="teller" or session["usert"]=="cashier":
        if kunde_id is None:
            return redirect(url_for("se_kunder"))
        else:
            if request.method == "POST":
                src_type = request.form.get("src_type")
                trg_type = request.form.get("trg_type")
                belop = int(request.form.get("belop"))
                if src_type != trg_type:
                    src_data  = db.execute("SELECT * from konto where kunde_id = :a and konto_type = :t and status='active'", {"a":kunde_id,"t":src_type}).fetchone()
                    til_data  = db.execute("SELECT * from konto where kunde_id = :a and konto_type = :t and status='active'", {"a":kunde_id,"t":trg_type}).fetchone()
                    if src_data is not None and til_data is not None:
                        if src_data.saldo > belop:
                            src_saldo = src_data.saldo - belop
                            trg_saldo = til_data.saldo + belop
                            
                            test = db.execute("UPDATE konto set saldo = :b where kunde_id = :a and konto_type = :t", {"b":src_saldo, "a":kunde_id, "t":src_type})
                            db.commit()
                            temp = Transaksjoner(bruker_id=src_data.bruker_id,trans_melding="belop overført til "+ str(til_data.bruker_id),belop=belop)
                            db.add(temp)
                            db.commit()

                            db.execute("UPDATE konto set saldo = :b where kunde_id = :a and konto_type = :t", {"b":trg_saldo, "a":kunde_id, "t":trg_type})
                            db.commit()
                            temp = Transaksjoner(bruker_id=til_data.bruker_id,trans_melding="belop mottatt fra "+ str(src_data.bruker_id), belop=belop)
                            db.add(temp)
                            db.commit()

                            flash(f"beløp overført til {til_data.bruker_id} fra {src_data.bruker_id}", "vellykket")
                        else:
                            flash("Utilstrekkelig beløp å overføre", "fare")
                            
                    else:
                        flash("konto ikke funnet", "fare")

                else:
                    flash("Kan ikke overføre til samme konto", "advarsel")

            else:
                data = db.execute("SELECT * from konto where kunde_id = :a", {"a":kunde_id}).fetchall()
                if data and len(data) == 2:
                    return render_template("overforing.html", innskudd=True, kunde_id=kunde_id)
                else:
                    flash("Data ikke funnet eller ugyldig kunde-ID", "fare")
                    return redirect(url_for("se_kunder"))

    return redirect(url_for("hovedmeny"))

@app.route("/uttalelse" , methods=["GET", "POST"])
def uttalelse():
    if "user" not in session:
        return redirect(url_for("innlogging"))
    if session["usert"] == "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("hovedmeny"))       
    if session["usert"]=="teller" or session["usert"]=="cashier":
        if request.method == "POST":
            bruker_id = request.form.get("bruker_id")
            nummer = request.form.get("nummer")
            flag = request.form.get("Radio")
            start_date = request.form.get("start_date")
            end_date = request.form.get("end_date")
            if flag=="red":
                data = db.execute("SELECT * FROM (SELECT  * FROM transaksjoner where bruker_id=:d ORDER BY trans_id DESC LIMIT :l)Var1 ORDER BY trans_id ASC;", {"d": bruker_id,"l":nummer}).fetchall()
            else:
                data = db.execute("SELECT * FROM transaksjoner WHERE bruker_id=:a between DATE(time_stamp) >= :s AND DATE(time_stamp) <= :e;", {"a":bruker_id, "s":start_date,"e":end_date}).fetchall()
            if data:
                return render_template("uttalelse.html", uttalelse=True, data=data, bruker_id=bruker_id)
            else:
                flash("Ingen transaksjoner", "fare")
                return redirect(url_for("hovedmeny"))
    else:
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("hovedmeny"))
    return render_template("uttalelse.html", uttalelse=True)

# route for 404 error
@app.errorhandler(404)
def not_found(e):
  return render_template("404.html") 

# avlogging 
@app.route("/avlogging")
def avlogging():
    session.pop("user", None)
    return redirect(url_for("innlogging"))

# innlogging
@app.route("/innlogging", methods=["GET", "POST"])
def innlogging():
    if "user" in session:
        return redirect(url_for("hovedmeny"))
    
    if request.method == "POST":
        email = request.form.get("email").lower()
        passord = request.form.get("passord").encode("utf-8")
        resultat = db.execute("SELECT * FROM bruker WHERE id = :u", {"u": email}).fetchone()
        if resultat is not None:
            if bcrypt.check_password_hash(resultat["passord"], passord) is True:
                print("riktig passord")
                session["email"] = email
                session["navn"] = resultat.navn
                session["usert"] = resultat.bruker_type
                flash(f"{resultat.navn.capitalize()}, du er innlogget!", "vellykket")
                return render_template("overforing.html")
        flash("Beklager, email eller password er feil.", "fare")
    return render_template("overforing.html", login=True)

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

@app.route("/KundeLog", methods=["GET", "POST"])
@app.route("/api/v1/KundeLog", methods=["GET", "POST"])
def KundeLog():
    if "user" not in session:
        flash("Vennligst logg inn", "advarsel")
        return redirect(url_for("innlogging"))
    if session["usert"] != "executive":
        flash("Du har ikke tilgang til denne api", "advarsel")
        return redirect(url_for("hovedmeny"))
    if session["usert"]=="executive":
        if request.method == "POST":
            kunde_id = request.json["kunde_id"]
            data = db.execute("SELECT melding_log,time_stamp from KundeLog where kunde_id= :c ORDER by time_stamp desc", {"c":kunde_id}).fetchone()
            t = {
                    "melding" : data.melding_log,
                    "date" : data.time_stamp
                }
            return jsonify(t)
        else:
            dict_data = []
            data = db.execute("SELECT kunder.kunde_id as id, kunder.ssn_kunde_id as ssn_id, KundeLog.melding_log as melding, KundeLog.time_stamp as date from KundeLog JOIN kunder ON kunder.kunde_id = KundeLog.kunde_id order by KundeLog.time_stamp desc limit 50").fetchall()
            for row in data:
                t = {
                    "id" : row.id,
                    "ssn_id" : row.ssn_id,
                    "melding" : row.melding,
                    "date" : row.date
                }
                dict_data.append(t)
            return jsonify(dict_data)

@app.route("/kontolog", methods=["GET", "POST"])
@app.route("/api/v1/kontolog", methods=["GET", "POST"])
def kontolog():
    if "user" not in session:
        flash("Venligst, logg inn", "advarsel")
        return redirect(url_for("innlogging"))
    if session["usert"] != "executive":
        flash("Du har ikke tilgang til denne api", "advarsel")
        return redirect(url_for("hovedmeny"))
    if session["usert"]=="executive":
        if request.method == "POST":
            bruker_id = request.json["bruker_id"]
            data = db.execute("SELECT status,melding,last_update as time_stamp from konto where bruker_id= :c;", {"c":bruker_id}).fetchone()
            t = {
                    "status" : data.status,
                    "melding" : data.melding,
                    "date" : data.time_stamp
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
                    "date" : row.last_update
                }
                dict_data.append(t)
            return jsonify(dict_data)
    

# Bytt på secret key. 
if __name__ == "__main__":
    app.secret_key = "admin123"
    app.debug = True
    app.run(host="127.0.0.1", port=5000)