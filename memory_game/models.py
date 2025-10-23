from django.db import models
from django.contrib.auth.models import User

class Partida(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nivel = models.CharField(max_length=20)
    resultado = models.CharField(max_length=10)  # 'victoria' o 'derrota'
    tiempo_restante = models.IntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.resultado} ({self.nivel})"
