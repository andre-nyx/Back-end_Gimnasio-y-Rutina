from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Rutina, Disciplina, Equipamiento, Inscripcion
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User

# Vista de Portada (Hito 2)
def home(request):
    ultimas_rutinas = Rutina.objects.all().order_by('-fecha_creacion')[:4]
    total_rutinas = Rutina.objects.count()
    total_disciplinas = Disciplina.objects.count()
    total_equipamientos = Equipamiento.objects.count()
    total_inscripciones_confirmadas = Inscripcion.objects.filter(estado='confirmada').count()
    
    context = {
        'ultimas_rutinas': ultimas_rutinas,
        'total_rutinas': total_rutinas,
        'total_disciplinas': total_disciplinas,
        'total_equipamientos': total_equipamientos,
        'total_inscripciones_confirmadas': total_inscripciones_confirmadas,
    }
    return render(request, 'website/home.html', context)

# Vista de Rutinas Públicas (Hito 2)
def rutinas_publicas(request):
    rutinas = Rutina.objects.select_related(
        'disciplina', 'entrenador'
    ).prefetch_related('equipamiento').order_by('-fecha_creacion')

    query = request.GET.get('q', '')
    disciplina_id = request.GET.get('disciplina', '')

    if query:
        rutinas = rutinas.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query)
        )



    if disciplina_id:
        rutinas = rutinas.filter(disciplina_id=disciplina_id)

    paginator = Paginator(rutinas, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    disciplinas = Disciplina.objects.all()

    context = {
        'page_obj': page_obj,
        'rutinas': page_obj,
        'query': query,
        'disciplina_seleccionada': disciplina_id,
        'disciplinas': disciplinas,
    }

    return render(request, 'website/rutinas_publicas.html', context)

# Detalle de Rutina
def rutina_detail(request, pk):
    rutina = get_object_or_404(
        Rutina.objects.select_related(
            'disciplina', 'entrenador'
        ).prefetch_related('equipamiento'),
        pk=pk
    )

    return render(
        request,
        'website/rutina_detail.html',
        {'rutina': rutina}
    )

# 1. Registro de Usuarios (Hito 3)

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        email = request.POST.get('email', '').strip()

        if form.is_valid():
            if not email:
                messages.error(
                    request,
                    'El correo electrónico es obligatorio.'
                )

            elif User.objects.filter(email__iexact=email).exists():
                messages.error(
                    request,
                    'Este correo electrónico ya está registrado.'
                )

            else:
                usuario = form.save(commit=False)
                usuario.email = email
                usuario.save()

                messages.success(
                    request,
                    '¡Te has registrado con éxito! Ya puedes iniciar sesión.'
                )
                return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, 'website/registro.html', {
        'form': form
    })
# 2. Mi Cuenta y Cambio de Contraseña (Hito 3)

@login_required
def mi_cuenta(request):
    password_form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion == 'datos':
            nombre = request.POST.get('first_name', '').strip()
            apellido = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()

            if not email:
                messages.error(request, 'El correo electrónico es obligatorio.')

            elif User.objects.filter(email__iexact=email).exclude(
                pk=request.user.pk
            ).exists():
                messages.error(request, 'Ese correo electrónico ya está registrado.')

            else:
                request.user.first_name = nombre
                request.user.last_name = apellido
                request.user.email = email
                request.user.save()

                messages.success(
                    request,
                    'Tus datos personales se actualizaron correctamente.'
                )
                return redirect('mi_cuenta')

        elif accion == 'password':
            password_form = PasswordChangeForm(
                request.user,
                request.POST
            )

            if password_form.is_valid():
                usuario = password_form.save()
                update_session_auth_hash(request, usuario)

                messages.success(
                    request,
                    'Tu contraseña se actualizó correctamente.'
                )
                return redirect('mi_cuenta')

            else:
                messages.error(
                    request,
                    'Por favor corrige los errores en el formulario.'
                )

    return render(request, 'website/mi_cuenta.html', {
        'password_form': password_form
    })

# 3. CRUD de Rutinas - Listar, Crear, Editar y Eliminar (Hito 3)

@login_required
def mis_rutinas(request):
    rutinas = Rutina.objects.filter(
        entrenador=request.user
    ).select_related(
        'disciplina'
    ).prefetch_related(
        'equipamiento'
    ).order_by('-fecha_creacion')

    return render(request, 'website/mis_rutinas.html', {
        'rutinas': rutinas
    })


@login_required
def crear_rutina(request):
    disciplinas = Disciplina.objects.all()
    equipamientos = Equipamiento.objects.all()

    if request.method == 'POST':
        try:
            rutina = Rutina(
                titulo=request.POST.get('titulo', '').strip(),
                descripcion=request.POST.get('descripcion', '').strip(),
                descripcion_equipamiento=request.POST.get(
                    'descripcion_equipamiento', ''
                ).strip(),
                duracion_minutos=request.POST.get('duracion_minutos'),
                cupos=request.POST.get('cupos'),
                nivel=request.POST.get('nivel'),
                disciplina_id=request.POST.get('disciplina') or None,
                entrenador=request.user
            )

            rutina.full_clean()
            rutina.save()

            equipos_seleccionados = request.POST.getlist('equipamiento')
            rutina.equipamiento.set(equipos_seleccionados)

            messages.success(request, '¡Rutina creada con éxito!')
            return redirect('mis_rutinas')

        except (ValidationError, ValueError, TypeError) as e:
            messages.error(request, f'Error al crear la rutina: {e}')

    return render(request, 'website/crear_rutina.html', {
        'disciplinas': disciplinas,
        'equipamientos': equipamientos
    })


@login_required
def editar_rutina(request, pk):
    rutina = get_object_or_404(Rutina, pk=pk)

    if rutina.entrenador != request.user:
        messages.error(
            request,
            'No tienes permiso para editar esta rutina.'
        )
        return redirect('mis_rutinas')

    disciplinas = Disciplina.objects.all()
    equipamientos = Equipamiento.objects.all()

    if request.method == 'POST':
        try:
            rutina.titulo = request.POST.get('titulo', '').strip()
            rutina.descripcion = request.POST.get('descripcion', '').strip()
            rutina.descripcion_equipamiento = request.POST.get(
                'descripcion_equipamiento', ''
            ).strip()
            rutina.duracion_minutos = request.POST.get('duracion_minutos')
            rutina.cupos = request.POST.get('cupos')
            rutina.nivel = request.POST.get('nivel')

            disciplina_id = request.POST.get('disciplina')
            rutina.disciplina_id = disciplina_id if disciplina_id else None

            rutina.full_clean()
            rutina.save()

            equipos_seleccionados = request.POST.getlist('equipamiento')
            rutina.equipamiento.set(equipos_seleccionados)

            messages.success(request, '¡Rutina actualizada con éxito!')
            return redirect('mis_rutinas')

        except (ValidationError, ValueError, TypeError) as e:
            messages.error(request, f'Error al actualizar la rutina: {e}')

    return render(request, 'website/crear_rutina.html', {
        'rutina': rutina,
        'disciplinas': disciplinas,
        'equipamientos': equipamientos,
        'editando': True
    })


@login_required
def eliminar_rutina(request, pk):
    rutina = get_object_or_404(Rutina, pk=pk)

    if rutina.entrenador != request.user:
        messages.error(
            request,
            'No tienes permiso para eliminar esta rutina.'
        )
        return redirect('mis_rutinas')

    if request.method == 'POST':
        rutina.delete()
        messages.success(request, 'Rutina eliminada correctamente.')
        return redirect('mis_rutinas')

    return render(
        request,
        'website/eliminar_rutina_confirm.html',
        {'rutina': rutina}
    )


@login_required
def crear_inscripcion(request, pk):
    rutina = get_object_or_404(Rutina, pk=pk)

    if rutina.entrenador == request.user:
        messages.error(request, 'No puedes inscribirte en tu propia rutina.')
        return redirect('rutina_detail', pk=pk)

    existente = Inscripcion.objects.filter(
        rutina=rutina,
        socio=request.user
    ).first()

    if request.method == 'POST':
        if existente:
            messages.warning(request, 'Ya tienes una solicitud para esta rutina.')
            return redirect('rutina_detail', pk=pk)

        inscripcion = Inscripcion(
            rutina=rutina,
            socio=request.user,
            comentario=request.POST.get('comentario', '').strip()
        )

        try:
            inscripcion.full_clean()
            inscripcion.save()
            messages.success(request, 'Solicitud enviada correctamente.')
        except ValidationError as error:
            messages.error(request, str(error))

        return redirect('rutina_detail', pk=pk)

    return render(request, 'website/solicitud_registro.html', {
        'rutina': rutina,
        'inscripcion_existente': existente
    })


@login_required
def mis_inscripciones(request):
    inscripciones = Inscripcion.objects.filter(
        socio=request.user
    ).select_related('rutina', 'rutina__entrenador').order_by('-fecha')

    return render(request, 'website/mis_inscripciones.html', {
        'inscripciones': inscripciones
    })


@login_required
@require_POST
def cancelar_inscripcion(request, pk):
    inscripcion = get_object_or_404(
        Inscripcion,
        pk=pk,
        socio=request.user
    )

    if inscripcion.estado == 'pendiente':
        inscripcion.delete()
        messages.success(request, 'Solicitud cancelada correctamente.')
    else:
        messages.error(request, 'Solo puedes cancelar solicitudes pendientes.')

    return redirect('mis_inscripciones')


@login_required
def gestionar_inscripciones(request):
    inscripciones = Inscripcion.objects.filter(
        rutina__entrenador=request.user
    ).select_related('rutina', 'socio').order_by('-fecha')

    return render(request, 'website/gestionar_inscripciones.html', {
        'inscripciones': inscripciones
    })


@login_required
@require_POST
def actualizar_estado_inscripcion(request, pk):
    inscripcion = get_object_or_404(
        Inscripcion,
        pk=pk,
        rutina__entrenador=request.user
    )

    nuevo_estado = request.POST.get('estado')

    if nuevo_estado in ['confirmada', 'rechazada']:
        inscripcion.estado = nuevo_estado
        inscripcion.save()
        messages.success(request, 'Estado de inscripción actualizado.')
    else:
        messages.error(request, 'Estado no válido.')

    return redirect('gestionar_inscripciones')

@login_required
def crear_disciplina(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()

        if not nombre:
            messages.error(request, 'Debes ingresar un nombre.')
        elif len(nombre) > 50:
            messages.error(request, 'El nombre no puede superar los 50 caracteres.')
        elif Disciplina.objects.filter(nombre__iexact=nombre).exists():
            messages.error(request, 'Esa disciplina ya existe.')
        else:
            Disciplina.objects.create(nombre=nombre)
            messages.success(request, 'Disciplina creada correctamente.')
            return redirect('crear_rutina')

    return render(request, 'website/crear_disciplina.html')


@login_required
def crear_equipamiento(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()

        if not nombre:
            messages.error(request, 'Debes ingresar un nombre.')
        elif len(nombre) > 50:
            messages.error(request, 'El nombre no puede superar los 50 caracteres.')
        elif Equipamiento.objects.filter(nombre__iexact=nombre).exists():
            messages.error(request, 'Ese equipamiento ya existe.')
        else:
            Equipamiento.objects.create(nombre=nombre)
            messages.success(request, 'Equipamiento creado correctamente.')
            return redirect('crear_rutina')

    return render(request, 'website/crear_equipamiento.html')