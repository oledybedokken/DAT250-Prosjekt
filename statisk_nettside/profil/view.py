from django.shortcuts import render, redirect
from . import forms
from . import models
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from profil.model import Status 
import random

def randomGen():
    return int(random.uniform(1000,9999))                           # RNG for 5 siffer fra 1e4 til 1e5

def indeks(request):
    try: nav_bruker = Status.objects.get(konto_nummer=request.user) # Ser etter konto_nummer
    except:
        # om nav_bruker ikke finnes, skaper en
        nav_bruker = Status()                                       # Fra model.py
        nav_bruker.account_number = randomGen()                     # Random account number for every user
        nav_bruker.balance = 0
        nav_bruker.save()
    return render(request, {"nav_bruker": nav_bruker})

def money_transfer(request):
    if request.method == "POST":
        pass ## WOP