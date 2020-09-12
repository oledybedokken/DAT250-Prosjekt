# Django tutorial: https://www.youtube.com/watch?v=M9rtf7icuG0

from django.db import models
import datetime

class GenerellInfo (models.Model):
    fornavn = models.CharField(max_length = 32, default = None)
    etternavn = models.CharField(max_length = 32, default = None)
    email = models.EmailField(default = None)
    fodselsdato = models.DateField(default = None)
    kjonn = models.CharField(max_length = 1, default = None)
    tlf_nummer = models.IntegerField(default = 0)
    auth_code = models.CharField(max_length = 5, default = None)            
    # Authentication kode - 5 siffer

class BrukerAdresse (models.Model):
    kommune = models.CharField(max_length = 32, default = "Stavanger")      # Last ned liste med by i Norge
    fylke = models.CharField(max_length = 32, default = "Rogaland")         # Rull-bar valg?
    addresse = models.CharField(max_length = 50)
    post = models.IntegerField()
    auth_code = models.CharField(max_length = 5, default = None)

class Status (models.Model):
    konto_nummer = models.IntegerField()
    formue = models.IntegerField()
    auth_code = models.CharField(max_length = 5, default = None)

class Overforing(models.Model):
    auth_code = models.CharField(max_length = 5, default = None)            
    # Spør etter auth kode
    destinasjon_konto_nummer = models.IntegerField()                        # Sende til konto nummer
    mengde_for_overforing = models.IntegerField()                           # Mengde som skal sendes.