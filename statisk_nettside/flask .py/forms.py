from flask_wtf import Forms
from wtforms import TextField, TextAreaField, SubmitField, PasswordField, BooleanField, IntegerField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email
import random_auth

def min_lengde(form, field):
    if len(field.data == 0:)
    raise ValueError("Felt skal ikke være tomt")

class Pameldingsskjema(Form):
#    fornavn = TextField("Fornavn", validators=[DataRequired(), min_lengde])
#    etternavn = TextField("Etternavn", validators=[DataRequired(), min_lengde])
    email = TextField("Email", validators=[DataRequired(), Email()])
    passord = PasswordField("Passord", validators=[DataRequired(), Length(min=8)])
#    autoriserings_kode = IntegerField("Autoriserings kode", validators=[DataRequired(), Length(min=5, max=5)])
    husk_meg = BooleanField("Hold meg innlogget")
    bekreft = SubmitField("Påmelding")

class Registreringsskjema(Form):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    passord = PasswordField("Passord", validators=[DataRequired(), Length(min=8, max=30)])
    fylke = TextField("Fylke", validators=[DataRequired(), min_lengde])
    by = TextField("By", validators=[DataRequired(), min_lengde])
    kjonn = SelectField("Kjønn", choices=[("Tørkel", "Tørkel"), ("Mann", "Mann")], validators=[DataRequired()], coerce="str"])
    husk_meg = BooleanField("Hold meg innlogget")
    bekreft = SubmitField("Logg in")

class Brukerskjema(Form):
    fornavn = TextField("Fornavn", validators=[DataRequired(), min_lengde])
    etternavn = TextField("Etternavn", validators=[DataRequired(), min_lengde])
    email = EmailField("Email", validaotrs=[DataRequired(), Email()])
    passord = PasswordField("Passord", validators=[DataRequired(), Length(min=8)])

class legg_til_kontoskjema(Form):
    konto_nummer = TextField("Konto nummer")
    f_uttak = TextField("Uttak")