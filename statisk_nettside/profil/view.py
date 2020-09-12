from django.shortcuts import render, redirect
from django.db import forms
from django.db import models
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from profil.model import Status 
import random


# Spør etter email - UNIQUE KEY

def randomGen():
    return int(random.uniform(10000, 99999))                        # RNG for 5 siffer tall

def indeks(request):
    try:
        nav_bruker = Status.objects.get(auth_code=request.user)     # Detaljer om nåværende bruker
    except:
        # om det er ingen detaljer for nav_bruker, lag ny detaljer
        nav_bruker = Status()
        nav_bruker.konto_nummer = randomGen()                       # random konto nummer for ny brukere (brukskonto)
        nav_bruker.auth_code = request.user
        nav_bruker.save()
    return render(request, {"nav_bruker": nav_bruker})
