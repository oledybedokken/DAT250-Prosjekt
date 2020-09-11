# Django tutorial: https://www.youtube.com/watch?v=M9rtf7icuG0

from django.db import models
import date.time

class Detaljer(models.Model):
    fornavn = model.CharField(max_length = 32, default = None)
    etternavn = model.Charfield(max_length = 32, default = None)
    kjonn = models.Charfield(max_length = 1, default = None)
    email = models.EmailField(default = None)
    tlf_nummer = models.IntegerField(default = 0)
    yrke = models.CharField(max_length = 50, default = None)
    fodselsdato = models.DateField(default = None)
    
class NaverendePosisjon(models.Model):
    fylke = models.CharField(max_length = 50, default = "Rogaland")
    by = models.Charfield(max_length = 50, default = "Stavanger")
    addresse = models.Charfield(max_length = 50)
    post_addresse = models.IntegerField()

class Status(models.Model):
    konto_nummer = models.IntegerField()
    formue = models.IntegerField()

class Transaksjon(models.Model):
    input_konto_nummer_sender = models.CharField(max_length = 8, default = None) # 282.21.391
    input_konto_nummer_mottaker = models.IntegerField()
    input_mengde_sende_NOK = models.IntegerField()