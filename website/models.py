from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

# 1. Catálogo: Disciplina
class Disciplina(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


# 2. Etiqueta: Equipamiento
class Equipamiento(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


# 3. Entidad Principal: Rutina (Dueño: Entrenador)
class Rutina(models.Model):
    NIVELES = [
        ('basico', 'Básico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    duracion_minutos = models.IntegerField()
    cupos = models.IntegerField()
    nivel = models.CharField(max_length=20, choices=NIVELES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    entrenador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rutinas')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.SET_NULL, null=True, blank=True)
    equipamiento = models.ManyToManyField(Equipamiento, blank=True)

    def clean(self):
        if self.duracion_minutos is not None and (self.duracion_minutos < 10 or self.duracion_minutos > 120):
            raise ValidationError({'duracion_minutos': 'La duración debe estar entre 10 y 120 minutos.'})
        
        if self.cupos is not None and (self.cupos < 1 or self.cupos > 30):
            raise ValidationError({'cupos': 'Los cupos deben estar entre 1 y 30.'})

    def __str__(self):
        return f"{self.titulo} - {self.entrenador.username}"


# 4. Solicitud: Inscripcion (La crea el socio)
class Inscripcion(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('rechazada', 'Rechazada'),
    ]

    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE, related_name='inscripciones')
    socio = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mis_inscripciones')
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    class Meta:
        unique_together = ('rutina', 'socio')

    def clean(self):
        if hasattr(self, 'rutina') and self.rutina.entrenador == self.socio:
            raise ValidationError('Un entrenador no puede inscribirse en su propia rutina.')

    def __str__(self):
        return f"{self.socio.username} -> {self.rutina.titulo} [{self.estado}]"