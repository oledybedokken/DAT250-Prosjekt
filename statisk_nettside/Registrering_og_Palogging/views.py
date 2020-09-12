from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def registrer(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid()
        form.save()
        return redirect("statisk_nettside/Login.html")
    else:
        form = UserCreationForm()
    return render(request, "statisk_nettside/Registrer.html", {"form": form})

def loggin(request):
    if request.method == "POST"
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        bruker = form.get_user()
        login(request, user)
        return redirect("statisk_nettside/MainPage.html")
    else:
        form = AuthenticationForm()
        return render(request, "statisk_nettisde/Login.html", {"form": form})

def logg_av(request): 
    # Trykke på logout-knappen for å logge ut. 
    # Må linkes til i html fila. Idk hvordan.

    logout(request)
    return redirect("statisk_nettside/Login.html")