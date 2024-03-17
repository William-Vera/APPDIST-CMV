from django.db import models

# Create your models here.
class NotificacionEnviada(models.Model):
    TIPO_NOTIFICACION_CHOICES = [
        ('last_value1', 'Last Value 1'),
        ('last_value2', 'Last Value 2'),
        ('last_value3', 'Last Value 3'),
        ('last_value4', 'Last Value 4'),
    ]
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    tipo_notificacion = models.CharField(max_length=20, choices=TIPO_NOTIFICACION_CHOICES, blank=True, null=True)

    class Meta:
        db_table = 'notificaciones_enviadas'