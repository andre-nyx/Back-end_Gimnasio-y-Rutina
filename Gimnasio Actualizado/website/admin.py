from django.contrib import admin
from .models import Disciplina, Equipamiento, Rutina, Inscripcion

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Equipamiento)
class EquipamientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Rutina)
class RutinaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'entrenador', 'duracion_minutos', 'cupos', 'nivel', 'disciplina')
    list_filter = ('nivel', 'disciplina')
    search_fields = ('titulo', 'descripcion', 'entrenador__username')

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('id', 'rutina', 'socio', 'estado', 'fecha')
    list_filter = ('estado',)
    search_fields = ('rutina__titulo', 'socio__username')