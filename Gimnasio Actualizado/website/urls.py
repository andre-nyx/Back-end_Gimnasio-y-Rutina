from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Vistas públicas
    path('', views.home, name='home'),
    path('rutinas/', views.rutinas_publicas, name='rutinas_publicas'),
    path('rutina/<int:pk>/', views.rutina_detail, name='rutina_detail'),

    # Cuentas y autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='website/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),

    # CRUD de rutinas protegido
    path('mis-rutinas/', views.mis_rutinas, name='mis_rutinas'),
    path('rutinas/crear/', views.crear_rutina, name='crear_rutina'),
    path('rutinas/editar/<int:pk>/', views.editar_rutina, name='editar_rutina'),
    path('rutinas/eliminar/<int:pk>/', views.eliminar_rutina, name='eliminar_rutina'),

    # Inscripciones
    path('rutina/<int:pk>/inscribirse/', views.crear_inscripcion, name='crear_inscripcion'),
    path('mis-inscripciones/', views.mis_inscripciones, name='mis_inscripciones'),
    path('inscripcion/cancelar/<int:pk>/', views.cancelar_inscripcion, name='cancelar_inscripcion'),
    path('entrenador/inscripciones/', views.gestionar_inscripciones, name='gestionar_inscripciones'),
    path('entrenador/inscripcion/<int:pk>/estado/', views.actualizar_estado_inscripcion, name='actualizar_estado_inscripcion'),

    # Catálogos
    path('disciplinas/crear/', views.crear_disciplina, name='crear_disciplina'),
    path('equipamientos/crear/', views.crear_equipamiento, name='crear_equipamiento'),
]