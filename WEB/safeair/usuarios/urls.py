from django.urls import path
from .views import pricipal, registar_usuarios,autenticacion_usuarios,cerrar_sesion

urlpatterns = [
    path('', pricipal, name='principal'),
    path('regitrar_usuarios/', registar_usuarios, name='regitrar_usuarios'),
    path('autenticacion_usuarios/', autenticacion_usuarios, name='autenticacion_usuarios'),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
]