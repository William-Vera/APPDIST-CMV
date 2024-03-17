from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import transaction
from usuarios.models import Usuarios
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import cache_control

# Create your views here.

def pricipal(request):
    return render(request, 'principal.html')

def registar_usuarios(request):
    if request.POST['contra1'] == request.POST['contra2']:
        try:
            with transaction.atomic():
                if 'foto' in request.FILES:
                    fotoin = request.FILES['foto']
                else:
                    fotoin=""
                user=User.objects.create_user(username=request.POST['email'], 
                                        email=request.POST['email'],password=request.POST['contra1'])
                user.save()
                usuario=Usuarios(user=user,foto=fotoin)
                usuario.save()
                # return HttpResponse('Te has registrado con exito '+usuario.username)
        except:
            return HttpResponse('El usuario ya existe')
    return render(request, 'principal.html')

def autenticacion_usuarios(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            print(username, password, user)
            if user is not None:
                login(request, user)
                # redirige a la página de inicio después del inicio de sesión exitoso
                return redirect('principal')
            else:
                return render(request, 'principal.html',{'error_message': 'Usuario o contraseña incorrecto, porfavor ingrese de nuevo'})
        else:
            return render(request, 'principal.html')
    except:
            messages.warning(request, 'Actualiza la pagina por favor')
            return redirect('principal.html')
    
def cerrar_sesion(request):
    logout(request)
    return render(request, 'principal.html')