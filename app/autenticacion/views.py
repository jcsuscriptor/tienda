from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import RegistroForm

def acceder(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre_usuario, password=password)
            if usuario is not None:
                login(request, usuario)
                messages.success(request, F"Bienvenid@ de nuevo {nombre_usuario}")
                return redirect("listado_productos")
            else:
                messages.error(request, "Los datos son incorrectos")
        else:
            messages.error(request, " Los datos son incorrectos")

    form = AuthenticationForm()
    return render(request, "autenticacion/acceder.html", {"form": form})

#Acceder al registro de autenticacion
class VistaRegistro(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        form = RegistroForm()
        return render(request, "autenticacion/registro.html", {"form": form})

    # noinspection PyMethodMaybeStatic
    def post(self, request):
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            nombre_usuario = form.cleaned_data.get("username")
            messages.success(request, F"Bienvenid@ a la plataforma {nombre_usuario}")
            login(request, usuario)
            return redirect("listado_productos")
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
            return render(request, "autenticacion/registro.html", {"form": form})

def salir(request):
    logout(request)
    messages.success(request, F"Tu sesi??n se ha cerrado correctamente")
    return redirect("acceder")