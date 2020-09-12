from django.shortcuts import render, redirect                       # Render side og redirect til side
from profil import forms                                            # forms.py
from profil import models                                           # models.py
from django.contrib.auth.forms import PasswordChangeForm            # Egen Form for å bytte passord
from django.contrib import messages                                 # Gir melding
from django.contrib.auth import update_session_auth_hash            # Ikke logge ut etter passordet er skrevet.
from profiles.models import Status                                  # import bare Status
import random


# Spør etter email - UNIQUE KEY

def randomGen():
    return int(random.uniform(10000, 99999))                        
    # RNG for 5 siffer tall

def indeks(request):
    try:
        nav_bruker = Status.objects.get(auth_code = request.user)     
        # Detaljer om nåværende bruker
    except:
        # om det er ingen detaljer for nav_bruker, lag ny detaljer
        nav_bruker = Status()
        nav_bruker.konto_nummer = randomGen()                       
        # random konto nummer for ny brukere (brukskonto)
        nav_bruker.auth_code = request.user
        nav_bruker.save()
    return render(request, "statisk_nettside/Konto.html", {"nav_bruker": nav_bruker})
    # Kombinerer en gitt mal med en gitt kontekstordbok og returnerer 
    # et HttpResponse-objekt med den gjengitte teksten.

def overforing(request):
    if request.method == "POST"
    # HHTP-metode POST. Det betyr at skjemaet ble sendt inn av en bruker,
    # og vi kan finne dems utfylte svar ved hjelp av forespørselen. POST QueryDict
    # TRUE / FALSE

    # Bedre forklarelse: 
    # https://stackoverflow.com/questions/19132210/what-does-request-method-post-mean-in-django

    form = forms.OverforingForm(request.POST)
    if form.is_valid():
        form.save()

        nav_bruker = models.Overforing.objects.get(auth_code=request.user)
        # nåværende bruker blir spurt for auth kode

        destinasjon_konto_nummer = nav_bruker.input_destinasjon_konto_nummer
        
        midlertid = nav_bruker 
        # OBS: Dette er midlertidig filen for å lagre nav_bruker. 
        # Slettes når overføring er bekreftet.

        destinasjon_bruker = models.Status.objects.get(konto_nummer=destinasjon_konto_nummer)
        mengde_for_overforing = nav_bruker.input_destinasjon_konto_nummer
        nav_bruker = models.Status.objects.get(auth_code=request.user)
        # Tre-fase omgang for å konfirmere sending, mengde for å sende og 
        # spør etter auth_code for confirmasjon.

        nav_bruker.formue = nav_bruker.formue - mengde_for_overforing
        destinasjon_bruker = destinasjon_bruker.formue + mengde_for_overforing
        # Pengene sendes.

        nav_bruker.save()
        destinasjon_bruker.save()
        # Lagrer endringene på kontoene av det som vises over.

        midlertid.delete() 
        # OBS: Fjerner muligheten for fremtidig overførelse (ingen caching)

        return redirect("statisk_nettside/Konto.html")
        # Kaster deg over til annet side.
    else:
        form = forms.OverforingForm()
    return render(request, "statisk_nettisde/Betaling", {"form": form})

def laan(request):
    return render(request, "statisk_nettside/laan.html")
    # Rendre lån mal

def efaktura(request):
    return render(request, "statisk_nettside/efaktura.html")
    # Rendre efaktura mal

def profil(request):
    return render(request, "statisk_nettside/profil")
    # Rendre profil mal

def profil_redigering(request):
    if request.method == "POST":
        # POST for GenerellInfoForm
        try:
            nav_bruker = models.GenerellInfo.objects.get(auth_code=request.user)
            # Nåværende bruker blir spurt om auth kode
            form = forms.GenerellInfoForm(request.POST, forekomst=nav_bruker)
            if form.is_valid():
                form.save()

        except:
            form = forms.GenerellInfoForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.auth_code = request.user
                form.save()

        # POST for BrukerAdresseForm
        try:
            nav_bruker = models.BrukerAdresse.objects.get(auth_code=request.user)
            # Nåværende bruker blir spurt om auth kode
            form = forms.BrukerAdresseForm(request.POST, forekomst=nav_bruker)
            if form.is_valid():
                form.save()
        except:
            form = forms.save(commit=False)
            form.auth_code = request.user
            form.save()

        # POST for å bytte passord - Egen form i django
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            # Tar den gjeldende forespørselen og oppdaterer brukerobject (user object) 
            # som den nye 'session hash' blir hentet fra, og oppdaterer 'session hash'. 
            # Den roterer 'session hash' slik at en stjålet session cookie blir ugyldiggjort.
            # Ikke logge ut etter passordet er skrevet.

            message.success(request, "Passordet ditt ble oppdatert!")
            return redirect("statisk_nettside/Profil.html")
        else:
            messages.error(request, "Noe gikk galt! Passordet kunne ikke endres, prøv igjen.")

        return redirect("statisk_nettside/Profil.html")
        # Når ferdig/feil-melding kastes man bort til Profil.html

    else: # Forsetter bare med get handlinger
        try: 
            nav_bruker = models.GenerellInfo.objects.get(auth_code=request.user)
            f1 = forms.GenerellInfoForm(forekomst=nav_bruker)   # GenerellInfo
        except:
            f1 = forms.GenerellInfoForm()
        
        try:
            nav_bruker = models.BrukerAdresse.objects.get(auth_code=request.user)
            f2 = forms.BrukerAdresseForm(forekomst=nav_bruker)  # BrukerAdresseForm
        except:
            f2 = forms.BrukerAdresseForm()

        f3 = PasswordChangeForm(request.user)
        # Passord bytte

        nokkel = {"f1": f1, "f2": f2, "f3": f3}
        return render(request, "statisk_nettside/ProfilRedigering.html", nokkel)

def slett_konto(request):
    return render(request, "statisk_nettside/SlettKonto.html")
         
