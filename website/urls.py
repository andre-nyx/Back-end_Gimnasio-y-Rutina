from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rutinas/', views.rutinas_publicas, name='rutinas_publicas'),
]