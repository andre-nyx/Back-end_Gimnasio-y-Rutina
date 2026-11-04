import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gimnasio_project.settings')
django.setup()

from django.contrib.auth.models import User
from website.models import Disciplina, Equipamiento, Rutina, Inscripcion

print("Actualizando inscripciones de prueba...")

usuarios = list(User.objects.all())
rutinas_todas = list(Rutina.objects.all()[:5])
estados = ['pendiente', 'confirmada', 'cancelada', 'confirmada', 'pendiente']

for idx, rutina in enumerate(rutinas_todas):
    try:
        Inscripcion.objects.get_or_create(
            rutina=rutina,
            socio=usuarios[idx % len(usuarios)], # Cambiado de usuario a socio
            defaults={'estado': estados[idx]}
        )
    except Exception as e:
        print(f"Nota: {e}")

print(f"-> ¡Inscripciones creadas con éxito! Total en BD: {Inscripcion.objects.count()}")