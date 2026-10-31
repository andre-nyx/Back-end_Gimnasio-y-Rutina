from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Disciplina, Equipamiento, Rutina


def home(request):
    rutinas = Rutina.objects.select_related('disciplina', 'entrenador').prefetch_related('equipamiento').order_by('-fecha_creacion')[:6]
    contexto = {
        'rutinas': rutinas,
        'total_rutinas': Rutina.objects.count(),
        'total_disciplinas': Disciplina.objects.count(),
        'total_equipamientos': Equipamiento.objects.count(),
    }
    return render(request, 'website/home.html', contexto)


def rutinas_publicas(request):
    query = request.GET.get('q', '').strip()
    rutinas = Rutina.objects.select_related('disciplina', 'entrenador').prefetch_related('equipamiento').order_by('-fecha_creacion')

    if query:
        rutinas = rutinas.filter(
            Q(titulo__icontains=query)
            | Q(descripcion__icontains=query)
            | Q(disciplina__nombre__icontains=query)
            | Q(entrenador__username__icontains=query)
        )

    paginator = Paginator(rutinas, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'website/rutinas_publicas.html', {
        'page_obj': page_obj,
        'query': query,
    })


def rutina_detail(request, pk):
    rutina = get_object_or_404(
        Rutina.objects.select_related('disciplina', 'entrenador').prefetch_related('equipamiento'),
        pk=pk,
    )
    return render(request, 'website/rutina_detail.html', {'rutina': rutina})
