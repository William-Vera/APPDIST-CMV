from django.urls import path
from .views import procesos, actualizar_propiedades,datos_sensores

urlpatterns = [
    path('procesos/', procesos, name='procesos'),
    path('actualizar_propiedades/', actualizar_propiedades, name='actualizar_propiedades'),
    path('datos_sensores/', datos_sensores, name='datos_sensores'),
]