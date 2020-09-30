import os
import io
import sys
from flask import send_file
from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify, Response
from flask_bcrypt import Bcrypt
from flask_session import Session
from database import Base, Bruker, Kunder, Konto, KundeLog, Transaksjoner
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime
import xlwt
from fpdf import FPDF

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.urandom(24)

engine = create_engine('sqlite:///database.db',connect_args={'check_same_thread': False},echo=True)
Base.metadata.bind = engine
db = scoped_session(sessionmaker(bind=engine))
    
@app.route('/')
@app.route("/dashboard")
def dashboard():
    return render_template("home.html", home=True)

@app.route("/leggtilkunde" , methods=["GET", "POST"])
def leggtilkunde():
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("dashboard"))
    if session['usert']=="executive":
        if request.method == "POST":
            ssn_kunde_id = int(request.form.get("ssn_kunde_id"))
            name = request.form.get("name")
            adresse = request.form.get("adresse")
            age= int(request.form.get("age"))
            fylke = request.form.get("fylke")
            by = request.form.get("by")
            resultat = db.execute("SELECT * from kunder WHERE ssn_kunde_id = :c", {"c": ssn_kunde_id}).fetchone()
            if resultat is None :
                resultat = db.query(Kunder).count()
                if resultat == 0 :
                    query = Kunder(kunde_id=110110000,ssn_kunde_id=ssn_kunde_id,name=name,adresse=adresse,age=age,fylke=fylke,by=by,status='aktiv')
                else:
                    query = Kunder(ssn_kunde_id=ssn_kunde_id,name=name,adresse=adresse,age=age,fylke=fylke,by=by,status='aktiv')
                db.add(query)
                db.commit()
                if query.kunde_id is None:
                    flash("Data er ikke satt inn! Sjekk om informasjon er riktig", "fare")
                else:
                    temp = KundeLog(kunde_id=query.kunde_id,log_message="Kundelaget")
                    db.add(temp)
                    db.commit()
                    flash(f"Kunde {query.name} er opprettet med kunde-ID: {query.kunde_id}.", "vellykket")
                    return redirect(url_for('se_kunde'))
            flash(f"SSN-ID : {ssn_kunde_id} er allerede i databasen.", "advarsel")
        
    return render_template('leggtilkunde.html', leggtilkunde=True)

@app.route("/se_kunde/<kunde_id>")
@app.route("/se_kunde" , methods=["GET", "POST"])
def se_kunde(kunde_id=None):
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("dashboard"))
    if session['usert']=="executive":
        if request.method == "POST":
            ssn_kunde_id = request.form.get("ssn_kunde_id")
            kunde_id = request.form.get("kunde_id")
            data = db.execute("SELECT * from kunder WHERE kunde_id = :c or ssn_kunde_id = :d", {"c": kunde_id, "d": ssn_kunde_id}).fetchone()
            if data is not None:
                return render_template('se_kunde.html', se_kunde=True, data=data)
            
            flash("Kunden ble ikke funnet! Sjekk om det er riktig.", "fare")
        elif kunde_id is not None:
            data = db.execute("SELECT * from kunder WHERE kunde_id = :c", {"c": kunde_id}).fetchone()
            if data is not None:
                return render_template('se_kunde.html', se_kunde=True, data=data)
            
            flash("Kunden ble ikke funnet! Sjekk om det er riktig.", "fare")
    else:
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("dashboard"))

    return render_template('se_kunde.html', se_kunde=True)

@app.route('/')
@app.route('/redigkunde/<kunde_id>', methods=["GET", "POST"])
def redigkunde(kunde_id=None):
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("dashboard"))
    if session['usert']=="executive":
        if kunde_id is not None:
            if request.method != "POST":
                kunde_id = int(kunde_id)
                data = db.execute("SELECT * from kunder WHERE kunde_id = :c", {"c": kunde_id}).fetchone()
                if data is not None and data.status != 'ikke aktiv':
                    return render_template('redigkunde.html', redigkunde=True, data=data)
                else:
                    flash("Kunden er ikke aktiv eller ikke til stede i databasen.","advarsel")
            else:
                kunde_id = int(kunde_id)
                name = request.form.get("name")
                adresse = request.form.get("adresse")
                age = int(request.form.get("age"))
                resultat = db.execute("SELECT * from kunder WHERE kunde_id = :c and status = 'aktiv'", {"c": kunde_id}).fetchone()
                if resultat is not None :
                    resultat = db.execute("UPDATE kunder SET name = :n , adresse = :add , age = :ag WHERE kunde_id = :a", {"n": name,"add": adresse,"ag": age,"a": kunde_id})
                    db.commit()
                    temp = KundeLog(kunde_id=kunde_id,log_message="Kundedata er oppdatert")
                    db.add(temp)
                    db.commit()
                    flash(f"Kundedata er oppdatert.", "vellykket")
                else:
                    flash("Ugyldig kunde-ID. Vennligst sjekk kunde-ID.", "advarsel")

    return redirect(url_for('se_kunde'))

@app.route('/slettkunde')
@app.route('/slettkunde/<kunde_id>')
def slettkunde(kunde_id=None):
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("dashboard"))
    if session['usert']=="executive":
        if kunde_id is not None:
            kunde_id = int(kunde_id)
            resultat = db.execute("SELECT * from kunder WHERE kunde_id = :a and status = 'aktiv'", {"a": kunde_id}).fetchone()
            if resultat is not None :
                query = db.execute("UPDATE kunder SET status='ikke aktiv' WHERE kunde_id = :a", {"a": kunde_id})
                db.commit()
                temp = KundeLog(kunde_id=kunde_id,log_message="Kunde deaktivert")
                db.add(temp)
                db.commit()
                flash(f"Kunde er slettet.", "vellyket")
                return redirect(url_for("dashboard"))
            else:
                flash(f"Kunde med ID: {kunde_id} er allerede aktiv eller ikke til stede i databasen.", "advarsel")
    return redirect(url_for('se_kunde'))

@app.route('/aktiverkunde')
@app.route('/aktiverkunde/<kunde_id>')
def aktiverkunde(kunde_id=None):
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("dashboard"))
    if session['usert']=="executive":
        if kunde_id is not None:
            kunde_id = int(kunde_id)
            resultat = db.execute("SELECT * from kunder WHERE kunde_id = :a and status = 'ikke aktiv'", {"a": kunde_id}).fetchone()
            if resultat is not None :
                query = db.execute("UPDATE kunder SET status='aktiv' WHERE kunde_id = :a", {"a": kunde_id})
                db.commit()
                temp = KundeLog(kunde_id=kunde_id,log_message="Kunden er aktiv.")
                db.add(temp)
                db.commit()
                flash(f"Kunden er aktiv.", "vellykket")
                return redirect(url_for("dashboard"))
            flash(f"Kunde med ID : {kunde_id} er allerede aktiv eller ikke til stede i databasen.", "advarsel")
    return redirect(url_for('se_kunde'))

@app.route('/aktiverkonto')
@app.route('/aktiverkonto/<konto_id>')
def aktiverkonto(konto_id=None):
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("dashboard"))
    if session['usert']=="executive":
        if konto_id is not None:
            konto_id = int(konto_id)
            resultat = db.execute("SELECT * from konto WHERE konto_id = :a and status = 'ikke aktiv'", {"a": konto_id}).fetchone()
            if resultat is not None :
                date = datetime.datetime.now()
                query = db.execute("UPDATE konto SET status='aktiv', message='Konto aktiv igjen', last_update = :d WHERE konto_id = :a", {"d":date,"a": konto_id})
                db.commit()
                flash(f"Kunden er aktiv.", "vellykket")
                return redirect(url_for("dashboard"))
            flash(f"Konto med ID : {konto_id} er allerede aktiv eller ikke til stede i databasen.", "advarsel")
    return redirect(url_for('se_konto'))

@app.route('/kundestatus')
def kundestatus():
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("dashboard"))
    if session['usert']=="executive":
        data = db.execute("SELECT kunder.kunde_id as id, kunder.ssn_kunde_id as ssn_id, kundelog.log_message as message, kundelog.time_stamp as date from (select kunde_id,log_message,time_stamp from kundelog group by kunde_id ORDER by time_stamp desc) as kundelog JOIN kunder ON kunder.kunde_id = kundelog.kunde_id group by kundelog.kunde_id order by kundelog.time_stamp desc").fetchall()
        if data:
            return render_template('kundestatus.html',kundestatus=True , data=data)
        else:
            flash("Ingen data er funnet.", "fare")
    return redirect(url_for("dashboard"))

@app.route("/leggtilkonto" , methods=["GET", "POST"])
def leggtilkonto():
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("dashboard"))
    if session['usert']=="executive":
        if request.method == "POST":
            kunde_id = int(request.form.get("kunde_id"))
            konto_type = request.form.get("konto_type")
            belop= float(request.form.get("belop"))
            message = "Bruker skapelse er vellykket"
            resultat = db.execute("SELECT * from kunder WHERE kunde_id = :c", {"c": kunde_id}).fetchone()
            if resultat is not None :
                resultat = db.execute("SELECT * from konto WHERE kunde_id = :c and konto_type = :at", {"c": kunde_id, "at": konto_type}).fetchone()
                if resultat is None:
                    resultat = db.query(Konto).count()
                    if resultat == 0 :
                        query = Konto(konto_id=360110000,konto_type=konto_type,saldo=belop,kunde_id=kunde_id,status='aktiv',message=message,last_update=datetime.datetime.now())
                    else:
                        query = Konto(konto_type=konto_type,saldo=belop,kunde_id=kunde_id,status='aktiv',message=message,last_update=datetime.datetime.now())
                    db.add(query)
                    db.commit()
                    if query.konto_id is None:
                        flash("Data er ikke satt inn! Sjekk om informasjon er riktig", "fare")
                    else:
                        flash(f"{query.konto_type} konto er skapt med konto-ID : {query.konto_id}.", "vellykket")
                        return redirect(url_for("dashboard"))
                else:
                    flash(f"Kunde med ID : {kunde_id} har allerede {konto_type} konto.", "advarsel")
            else:
                flash(f"Kunde med ID : {kunde_id} er ikke til stede i databasen.", "advarsel")

    return render_template('leggtilkonto.html', leggtilkonto=True)

@app.route("/se_konto" , methods=["GET", "POST"])
def se_konto():
    if 'user' not in session:
        return redirect(url_for('login'))        
    if session['usert']=="executive" or session['usert']=="teller" or session['usert']=="cashier":
        if request.method == "POST":
            konto_id = request.form.get("konto_id")
            kunde_id = request.form.get("kunde_id")
            data = db.execute("SELECT * from konto WHERE kunde_id = :c or konto_id = :d", {"c": kunde_id, "d": konto_id}).fetchall()
            if data:
                return render_template('se_konto.html', se_konto=True, data=data)
            
            flash("Konto ikke funnet! Vennligst sjekk om informasjon er riktig", "fare")
    else:
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("dashboard"))
    return render_template('se_konto.html', se_konto=True)


@app.route("/se_kontostatus" , methods=["GET", "POST"])
def se_kontostatus():
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] != "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("dashboard"))
    if session['usert']=="executive":
        data = db.execute("SELECT * from konto").fetchall()
        if data:
            return render_template('se_kontostatus.html', se_kontostatus=True, data=data)
        else:
            flash("konto ikke funnet!", "fare")
    return render_template('se_kontostatus.html', se_kontostatus=True)

@app.route('/inskudd',methods=['GET','POST'])
@app.route('/inskudd/<konto_id>',methods=['GET','POST'])
def inskudd(konto_id=None):
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] == "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("dashboard"))
    if session['usert']=="teller" or session['usert']=="cashier":
        if konto_id is None:
            return redirect(url_for('se_konto'))
        else:
            if request.method == "POST":
                belop = request.form.get("belop")
                data = db.execute("SELECT * from konto where konto_id = :a and status='aktiv'",{"a":konto_id}).fetchone()
                if data is not None:
                    saldo = int(belop) + int(data.saldo)
                    query = db.execute("UPDATE konto SET saldo= :b WHERE konto_id = :a", {"b":saldo,"a": data.konto_id})
                    db.commit()
                    flash(f"{belop} beløp deponert på konto: {data.konto_id}.", "vellykket")
                    temp = Transaksjoner(konto_id=data.konto_id,trans_melding="Beløp satt inn",belop=belop)
                    db.add(temp)
                    db.commit()
                else:
                    flash(f"Kontoen ble ikke funnet eller er inaktiv.", "fare")
            else:
                data = db.execute("SELECT * from konto where konto_id = :a",{"a":konto_id}).fetchone()
                if data is not None:
                    return render_template('inskudd.html', inskudd=True, data=data)
                else:
                    flash(f"Kontoen ble ikke funnet eller er inaktiv.", "fare")

    return redirect(url_for("dashboard"))

@app.route('/overfor',methods=['GET','POST'])
@app.route('/overfor/<kunde_id>',methods=['GET','POST'])
def overfor(kunde_id=None):
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] == "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("dashboard"))
    if session['usert']=="teller" or session['usert']=="cashier":
        if kunde_id is None:
            return redirect(url_for('se_konto'))
        else:
            if request.method == 'POST':
                src_type = request.form.get("src_type")
                trg_type = request.form.get("trg_type")
                belop = int(request.form.get("belop"))
                if src_type != trg_type:
                    src_data  = db.execute("SELECT * from konto where kunde_id = :a and konto_type = :t and status='aktiv'",{"a":kunde_id,"t":src_type}).fetchone()
                    trg_data  = db.execute("SELECT * from konto where kunde_id = :a and konto_type = :t and status='aktiv'",{"a":kunde_id,"t":trg_type}).fetchone()
                    if src_data is not None and trg_data is not None:
                        if src_data.saldo > belop:
                            src_saldo = src_data.saldo - belop
                            trg_saldo = trg_data.saldo + belop
                            
                            test = db.execute("UPDATE konto set saldo = :b where kunde_id = :a and konto_type = :t",{"b":src_saldo,"a":kunde_id,"t":src_type})
                            db.commit()
                            temp = Transaksjoner(konto_id=src_data.konto_id,trans_melding="belop overført til "+str(trg_data.konto_id),belop=belop)
                            db.add(temp)
                            db.commit()

                            db.execute("UPDATE konto set saldo = :b where kunde_id = :a and konto_type = :t",{"b":trg_saldo,"a":kunde_id,"t":trg_type})
                            db.commit()
                            temp = Transaksjoner(konto_id=trg_data.konto_id,trans_melding="belop mottatt fra "+str(src_data.konto_id),belop=belop)
                            db.add(temp)
                            db.commit()

                            flash(f"beløp overført til {trg_data.konto_id} fra {src_data.konto_id}", "vellykket")
                        else:
                            flash("Umulig beløp å overføre", "fare")
                            
                    else:
                        flash("konto ikke funnet", "fare")

                else:
                    flash("Kan ikke overføre til samme konto", "advarsel")

            else:
                data = db.execute("SELECT * from konto where kunde_id = :a",{"a":kunde_id}).fetchall()
                if data and len(data) == 2:
                    return render_template('overfor.html', inskudd=True, kunde_id=kunde_id)
                else:
                    flash("Data ikke funnet eller ugyldig kunde-ID", "fare")
                    return redirect(url_for('se_konto'))

    return redirect(url_for("dashboard"))

@app.route("/statement" , methods=["GET", "POST"])
def statement():
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] == "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("dashboard"))       
    if session['usert']=="teller" or session['usert']=="cashier":
        if request.method == "POST":
            konto_id = request.form.get("konto_id")
            number = request.form.get("number")
            flag = request.form.get("Radio")
            start_date = request.form.get("start_date")
            end_date = request.form.get("end_date")
            if flag=="red":
                data = db.execute("SELECT * FROM (SELECT * FROM transaksjoner where konto_id=:d ORDER BY trans_id DESC LIMIT :l)Var1 ORDER BY trans_id ASC;", {"d": konto_id,"l":number}).fetchall()
            else:
                data = db.execute("SELECT * FROM transaksjoner WHERE konto_id=:a between DATE(time_stamp) >= :s AND DATE(time_stamp) <= :e;",{"a":konto_id,"s":start_date,"e":end_date}).fetchall()
            if data:
                return render_template('statement.html', statement=True, data=data, konto_id=konto_id)
            else:
                flash("Ingen transaksjoner", "fare")
                return redirect(url_for("dashboard"))
    else:
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("dashboard"))
    return render_template('statement.html', statement=True)

@app.route('/pdf_xl_statement/<konto_id>')
@app.route('/pdf_xl_statement/<konto_id>/<ftype>')
def pdf_xl_statement(konto_id=None,ftype=None):
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['usert'] == "executive":
        flash("Du har ikke tilgang til denne siden", "advarsel")
        return redirect(url_for("dashboard"))       
    if session['usert']=="teller" or session['usert']=="cashier":
        if konto_id is not None:
            data = db.execute("SELECT * FROM transaksjoner WHERE konto_id=:a order by time_stamp limit 20;",{"a":konto_id}).fetchall()
            column_names = ['TransaksjonID', 'Beskrivelse', 'Dato', 'Beløp']
            if data:
                if ftype is None: 
                    pdf = FPDF()
                    pdf.add_page()
                    
                    page_width = pdf.w - 2 * pdf.l_margin
                    
                    pdf.set_font('Times','B',16.0) 
                    pdf.cell(page_width, 0.0, "Retail Banking", align='C')
                    pdf.ln(10)

                    msg='Account Statment : '+str(konto_id)
                    pdf.set_font('Times','',12.0) 
                    pdf.cell(page_width, 0.0, msg, align='C')
                    pdf.ln(10)

                    pdf.set_font('Times', 'B', 11)
                    pdf.ln(1)
                    
                    th = pdf.font_size
                    
                    pdf.cell(page_width/5, th, 'Transaksjon ID')
                    pdf.cell(page_width/3, th, 'Beskrivelse')
                    pdf.cell(page_width/3, th, 'Dato')
                    pdf.cell(page_width/7, th, 'Beløp')
                    pdf.ln(th)

                    pdf.set_font('Times', '', 11)

                    for row in data:
                        pdf.cell(page_width/5, th, str(row.trans_id))
                        pdf.cell(page_width/3, th, row.trans_melding)
                        pdf.cell(page_width/3, th, str(row.time_stamp))
                        pdf.cell(page_width/7, th, str(row.belop))
                        pdf.ln(th)
                    
                    pdf.ln(10)

                    bal = db.execute("SELECT saldo FROM konto WHERE konto_id=:a;",{"a":konto_id}).fetchone()
                    
                    pdf.set_font('Times','',10.0) 
                    msg='Nåværende saldo : '+str(bal.saldo)
                    pdf.cell(page_width, 0.0, msg, align='C')
                    pdf.ln(5)

                    pdf.cell(page_width, 0.0, '-- End of statement --', align='C')
                    
                    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'inline;filename=statement.pdf'})
                
                elif ftype == 'xl':

                    output = io.BytesIO()
                    workbook = xlwt.Workbook()
                    sh = workbook.add_sheet('Kontoutskrift')

                    sh.write(0, 0, 'Transaksjon ID')
                    sh.write(0, 1, 'Beskrivelse')
                    sh.write(0, 2, 'Dato')
                    sh.write(0, 3, 'Beløp')

                    idx = 0
                    for row in data:
                        sh.write(idx+1, 0, str(row.trans_id))
                        sh.write(idx+1, 1, row.trans_melding)
                        sh.write(idx+1, 2, str(row.time_stamp))
                        sh.write(idx+1, 3, str(row.belop))
                        idx += 1

                    workbook.save(output)
                    output.seek(0)

                    response = Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=statment.xls"})
                    return response
            else:
                flash("Ugyldig konto-ID", 'fare')
        else:
            flash("Vennligst, skriv inn Konto ID", "advarsel")
    return redirect(url_for("dashboard"))

@app.errorhandler(404)
def ikke_funnet(e):
  return render_template("404.html") 

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'user' in session:
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        email = request.form.get("email")
        passw = request.form.get("password").encode('utf-8')
        resultat = db.execute("SELECT * FROM bruker WHERE id = :u", {"u": email}).fetchone()
        if resultat is not None:
            if bcrypt.check_password_hash(resultat['password'], passw) is True:
                session['user'] = email
                session['namet'] = resultat.name
                session['usert'] = resultat.bruker_type
                flash(f"{resultat.name.capitalize()}, du er innlogget!", "vellykket")
                return redirect(url_for("dashboard"))
        flash("Beklager, email eller passord er feil.", "fare")
    return render_template("login.html", login=True)

@app.route('/api')
@app.route('/api/v1')
def api():
    return """
    <h2>List of Api</h2>
    <ol>
        <li>
            <a href="/api/v1/kundelog">Kunde Log</a>
            <a href="/api/v1/kontolog">Account Log</a>
        </li>
    </ol>
    """

@app.route('/kundelog', methods=["GET", "POST"])
@app.route('/api/v1/kundelog', methods=["GET", "POST"])
def kundelog():
    if 'user' not in session:
        flash("Vennligst logg inn", "advarsel")
        return redirect(url_for('login'))
    if session['usert'] != "executive":
        flash("Beklager, email eller password er feil.", "fare")
        return redirect(url_for("dashboard"))
    if session['usert']=="executive":
        if request.method == "POST":
            kunde_id = request.json['kunde_id']
            data = db.execute("SELECT log_message,time_stamp from kundelog where kunde_id= :c ORDER by time_stamp desc",{'c':kunde_id}).fetchone()
            t = {
                    "melding" : data.log_message,
                    "dato" : data.time_stamp
                }
            return jsonify(t)
        else:
            dict_data = []
            data = db.execute("SELECT kunder.kunde_id as id, kunder.ssn_kunde_id as ssn_id, kundelog.log_message as message, kundelog.time_stamp as date from kundelog JOIN kunder ON kunder.kunde_id = kundelog.kunde_id order by kundelog.time_stamp desc limit 50").fetchall()
            for row in data:
                t = {
                    "id" : row.id,
                    "ssn_id" : row.ssn_id,
                    "melding" : row.message,
                    "dato" : row.date
                }
                dict_data.append(t)
            return jsonify(dict_data)

@app.route('/kontolog', methods=["GET", "POST"])
@app.route('/api/v1/kontolog', methods=["GET", "POST"])
def kontolog():
    if 'user' not in session:
        flash("Vennligst logg inn", "advarsel")
        return redirect(url_for('login'))
    if session['usert'] != "executive":
        flash("Beklager, email eller password er feil.", "fare")
        return redirect(url_for("dashboard"))
    if session['usert']=="executive":
        if request.method == "POST":
            konto_id = request.json['konto_id']
            data = db.execute("SELECT status,message,last_update as time_stamp from konto where konto_id= :c;",{'c':konto_id}).fetchone()
            t = {
                    "status" : data.status,
                    "melding" : data.message,
                    "dato" : data.time_stamp
                }
            return jsonify(t)
        else:
            dict_data = []
            data = db.execute("SELECT kunde_id, konto_id, konto_type, status, message, last_update from konto limit 50").fetchall()
            for row in data:
                t = {
                    "kunde_id" : row.kunde_id,
                    "konto_id" : row.konto_id,
                    "konto_type" : row.konto_type,
                    "status" : row.status,
                    "melding" : row.message,
                    "dato" : row.last_update
                }
                dict_data.append(t)
            return jsonify(dict_data)
    
if __name__ == '__main__':
    app.secret_key = 'admin'
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
