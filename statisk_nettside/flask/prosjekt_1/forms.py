from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField, PasswordField
from wtforms.validators import InputRequired, EqualTo

class OpprettForm(FlaskForm):

    navn = StringField("Kontonavn: ", [InputRequired()])
    saldo = FloatField("Inngående egenkapital: ")
    passord = PasswordField("Passord: ", [InputRequired(), EqualTo("pass_konf", message="Passordene må være like")])
    pass_konf = PasswordField("Bekreft passord for kontoen: ")
    bekreft = SubmitField("Opprett konto")

class InnloggingForm(FlaskForm):

    email = TextField("Email: ",[validators.Required("Vennligst skriv inn E-postadressen din"), validators.email("Vennligst skriv inn E-postadressen din")])
    passord = PasswordField("Passord: ", [InputRequired()])
    bekreft = SubmitField("Login")

class OverforingForm(FlaskForm):

    konto_nummer = IntegerField("Mottakerens kontonummer: ", [InputRequired()])
    belop = FloatField("Overfør beløp: ", [InputRequired()])
    passord = PasswordField("Passord: ", [InputRequired()])
    overfor = SubmitField("Overfør beløp")

class InnskuddForm(FlaskForm):

    belop = FloatField("Innskuddsbeløp: ", [InputRequired()])
    bekreft = SubmitField("Innskuddsbeløp")

class SlettForm(FlaskForm):

    bruker_id = IntegerField("Kontonummer som skal slettes: ", [InputRequired()])
    passord = PasswordField("Passord: ", [InputRequired(), EqualTo("pass_konf", message="Passordene må være like")])
    pass_konf = PasswordField("Bekreft passord for kontoen: ")
    bekreft = SubmitField("Slett konto")