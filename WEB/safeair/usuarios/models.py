from django.db import models
from django.contrib.auth.models import User

class Usuarios(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario',default=1)
    cedula = models.CharField(max_length=10, unique=True, blank=True,null=True)
    fecha_nacimiento = models.DateTimeField(unique=False,blank=True,null=True)
    lugar_nacimiento = models.CharField(max_length=100,unique=False,blank=True,null=True)
    telefono = models.CharField(max_length=20,unique=False,blank=True,null=True)
    direccion = models.CharField(max_length=100, blank=True,null=True)
    foto = models.ImageField(null=True, blank=True, upload_to="usuariosft")

    def __str__(self):
        return self.user.first_name
    class Meta:
        ordering = ['user__last_name']

class Dispositivo(models.Model):
    token = models.CharField(max_length=255)

    def _str_(self):
        return self.token