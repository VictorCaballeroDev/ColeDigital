from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import *
from .decorators import*
from .forms import *

#########################################
#### PÁGINA PRINCIPAL ALUMNOS/PROFES ####
#########################################
@login_required(login_url='login')
@usuarios_habilitados(grupos_habilitados=['estudiante','profesor'])
def home(request):
    grupo = None
    user_req = request.user
    if request.user.groups.exists():
        grupo = request.user.groups.all()[0].name

    if grupo == 'estudiante':
        estudiante = get_object_or_404(Estudiante, user=user_req)
        asignaturas = Asignatura.objects.filter(estudiantes=estudiante)

    elif grupo == 'profesor':
        profesor = get_object_or_404(Profesor, user=user_req)
        asignaturas = Asignatura.objects.filter(profesores=profesor)
    


    context = {'asignaturas':asignaturas, 'grupo': grupo}
    return render(request, 'home.html', context)


#######################################
#### PÁGINA ASIGNATURA ESTUDIANTES ####
#######################################
@login_required(login_url='login')
@usuarios_habilitados(grupos_habilitados=['estudiante'])
@estudiante_apuntado_asignatura
def presentacion_asignatura_estudiantes(request, id_asignatura):
    asignatura = get_object_or_404(Asignatura, pk=id_asignatura)
    estudiante = get_object_or_404(Estudiante, user=request.user)
    asignaturas = Asignatura.objects.filter(estudiantes=estudiante)
    tareas = Tarea.objects.filter(asignatura=asignatura).order_by('fecha_entrega')
    grupo = request.user.groups.all()[0].name
    foro = getattr(asignatura, 'foro', None)

    if foro:
        mensajes = foro.mensajes.filter(mensaje_padre__isnull=True).order_by('fecha_creacion')
    else:
        mensajes = []

    reuniones = asignatura.reuniones.all()

    context = {
        'asignatura': asignatura,
        'asignaturas': asignaturas,
        'tareas': tareas,
        'grupo': grupo,
        'reuniones': reuniones,
        'foro': foro,
        'mensajes': mensajes
    }

    return render(request, 'presentacion_asignatura_estudiantes.html', context)

@login_required(login_url='login')
@usuarios_habilitados(grupos_habilitados=['estudiante'])
@tarea_asignada_estudiante
def detalles_tarea_estudiante(request, id_tarea):
    tarea = get_object_or_404(Tarea, pk=id_tarea)
    estudiante = get_object_or_404(Estudiante, user=request.user)
    # PROCESAR FORMULARIO PARA REALIZAR UNA ENTREGA EN ESTA TAREA
    if request.method == 'POST':
        form_entrega = CrearEntregaForm(request.POST, request.FILES)
        if form_entrega.is_valid():
            entrega = form_entrega.save(commit=False)
            entrega.tarea = tarea
            entrega.estudiante = estudiante
            entrega.save()
            if 'archivos' in request.FILES:
                archivos = request.FILES.getlist('archivos')
                for archivo in archivos:
                    ArchivoAdjuntoEntrega.objects.create(entrega=entrega, archivo=archivo)
            #messages.success(request, 'Tarea añadida correctamente')
            return redirect('detalles_tarea_estudiante', id_tarea)

    try:
        entrega = get_object_or_404(Entrega, tarea=tarea, estudiante=estudiante)
    except:
        entrega = None

    grupo = request.user.groups.all()[0].name
    asignaturas = Asignatura.objects.filter(estudiantes=estudiante)
    form_entrega = CrearEntregaForm()

    context = {
        'asignaturas': asignaturas,
        'grupo': grupo,
        'tarea': tarea,
        'form_entrega': form_entrega,
        'entrega': entrega
    }

    return render(request, 'detalles_tarea_estudiante.html', context)

@login_required(login_url='login')
@usuarios_habilitados(grupos_habilitados=['estudiante'])
def marcar_tarea_completada(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        id_tarea = request.POST.get('id_tarea')
        try:
            tarea = get_object_or_404(Tarea, pk=id_tarea)
            estudiante = get_object_or_404(Estudiante, user=request.user)
            Entrega.objects.create(tarea=tarea, estudiante=estudiante)
            messages.success(request, 'La tarea se marcó como completada')
            return JsonResponse({'status':'success'})
        except:
            return JsonResponse({'status':'error', 'message':'Algo falló, inténtelo más tarde'})
        

######################################
#### PÁGINA ASIGNATURA PROFESORES ####
######################################
@login_required(login_url='login')
@usuarios_habilitados(grupos_habilitados=['profesor'])
@profesor_apuntado_asignatura
def presentacion_asignatura_profesores(request, id_asignatura):
    asignatura = get_object_or_404(Asignatura, pk=id_asignatura)

    if request.method == 'POST':
        if 'crear_tarea' in request.POST:
            form_tarea = CrearTareaForm(request.POST, request.FILES)
            if form_tarea.is_valid():
                tarea = form_tarea.save(commit=False)
                tarea.asignatura = asignatura
                tarea.save()
                if 'archivos' in request.FILES:
                    archivos = request.FILES.getlist('archivos')
                    print(request.FILES)
                    print(archivos)
                    for archivo in archivos:
                        ArchivoAdjuntoTarea.objects.create(tarea=tarea, archivo=archivo)
                #messages.success(request, 'Tarea añadida correctamente')
                return redirect('presentacion_asignatura_profesores', id_asignatura)
            
        elif 'crear_reunion' in request.POST:
            form_reunion = CrearReunionForm(request.POST)
            if form_reunion.is_valid():
                reunion = form_reunion.save(commit=False)
                reunion.asignatura = asignatura
                reunion.save()
                return redirect('presentacion_asignatura_profesores', id_asignatura)
            
    profesor = get_object_or_404(Profesor, user=request.user)
    asignaturas = Asignatura.objects.filter(profesores=profesor)
    tareas = Tarea.objects.filter(asignatura=asignatura)
    grupo = request.user.groups.all()[0].name
    foro = getattr(asignatura, 'foro', None)

    if foro:
        mensajes = foro.mensajes.filter(mensaje_padre__isnull=True).order_by('fecha_creacion')
    else:
        mensajes = []

    reuniones = asignatura.reuniones.all()

    form_tarea = CrearTareaForm()
    form_reunion = CrearReunionForm()

    context = {
        'asignatura': asignatura,
        'asignaturas' : asignaturas,
        'tareas': tareas,
        'grupo' : grupo,
        'form_tarea': form_tarea,
        'reuniones': reuniones,
        'foro': foro,
        'mensajes': mensajes,
        'form_reunion': form_reunion
    }
    
    return render(request, 'presentacion_asignatura_profesores.html', context)


@login_required(login_url='login')
@usuarios_habilitados(grupos_habilitados=['profesor'])
def eliminar_tarea(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        id_tarea = request.POST.get('id_tarea')
        try:
            tarea = get_object_or_404(Tarea, pk=id_tarea)
            tarea.delete()
            messages.success(request, 'La tarea '+tarea.titulo+' se eliminó correctamente')
            return JsonResponse({'status':'success'})
        except:
            return JsonResponse({'status':'error', 'message':'Algo falló, inténtelo más tarde'})
    
    else:
        return redirect('home')

@login_required(login_url='login')
@usuarios_habilitados(grupos_habilitados=['profesor'])
def visualizar_entregas(request, id_tarea):
    tarea = get_object_or_404(Tarea, pk=id_tarea)
    entregas = tarea.entregas

    context = {
        'tarea': tarea,
        'entregas': entregas
    }

    return render(request, 'visualizar_entregas.html', context)

@login_required(login_url='login')
@usuarios_habilitados(grupos_habilitados=['profesor'])
def corregir_entrega(request, id_entrega):
    entrega = get_object_or_404(Entrega, pk=id_entrega)
    try:
        correccion = entrega.correccion
    except:
        correccion = None
    
    if request.method == 'POST':
        if correccion:
            form_correccion = CorreccionEntregaForm(request.POST, instance=correccion)
        else:
            form_correccion = CorreccionEntregaForm(request.POST)
        if form_correccion.is_valid():
            correccion = form_correccion.save(commit=False)
            correccion.entrega = entrega
            profesor = get_object_or_404(Profesor, user=request.user)
            correccion.corrector = profesor
            correccion.save()
            return redirect('corregir_entrega', id_entrega)
    
    if correccion:
        form_correccion = CorreccionEntregaForm(instance=correccion)
    else:
        form_correccion = CorreccionEntregaForm()

    tarea = entrega.tarea
    estudiante = entrega.estudiante
    context = {
        'entrega': entrega,
        'tarea': tarea,
        'estudiante': estudiante,
        'correccion': correccion,
        'form_correccion': form_correccion
    }

    return render(request, 'corregir_entrega.html', context)

#########################################
#### FUNCIONALIDADES DE AUTENTICACION ###
#########################################
@usuario_sin_autenticacion
def inicio_sesion(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Los datos introducidos no son correctos')
        
    context = {}
    return render(request, 'login.html', context)

@login_required(login_url='login')
def cerrar_sesion(request):
    logout(request)
    return redirect('login')

#########################################
### FUNCIONALIDADES DE ADMINISTRACION ###
#########################################

@login_required(login_url='login')
@admin
def panel_administracion(request):
    return render(request, 'panel_administracion.html')

# Gestión de estudiantes
@login_required(login_url='login')
@admin
def gestionar_estudiantes(request):

    estudiantes = Estudiante.objects.all().order_by('nombre')
    paginator = Paginator(estudiantes, 10)

    pagina = request.GET.get('page')
    page_obj = paginator.get_page(pagina)

    context = {'page_obj':page_obj}
    return render(request, 'gestionar_estudiantes.html',context)

#Gestión de profesores
@login_required(login_url='login')
@admin
def gestionar_profesores(request):

    profesores = Profesor.objects.all().order_by('nombre')
    paginator = Paginator(profesores, 10)

    pagina = request.GET.get('page')
    page_obj = paginator.get_page(pagina)

    context = {'page_obj': page_obj}
    return render(request, 'gestionar_profesores.html',context)

#Gestión de asignaturas
@login_required(login_url='login')
@admin
def gestionar_asignaturas(request):

    form_cambio_nombre = CambiarNombreAsignaturaForm()
    if request.method == 'POST':
        form_cambio_nombre = CambiarNombreAsignaturaForm(request.POST)
        if form_cambio_nombre.is_valid():
            asignatura_id = form_cambio_nombre.cleaned_data.get('asignatura_id')
            asignatura = get_object_or_404(Asignatura, pk=asignatura_id)
            viejo_nombre = asignatura.nombre
            nuevo_nombre = form_cambio_nombre.cleaned_data.get('nombre')
            asignatura.nombre = nuevo_nombre
            asignatura.save()
            messages.success(request, 'La asignatura "'+viejo_nombre+ '" ahora se llama "'+nuevo_nombre+'"')
            return redirect('gestionar_asignaturas')
        
    asignaturas = Asignatura.objects.all().order_by('nombre')
    paginator = Paginator(asignaturas, 10)

    pagina = request.GET.get('page')
    page_obj = paginator.get_page(pagina)

    context = {'page_obj': page_obj, 'form_cambio_nombre':form_cambio_nombre}
    return render(request, 'gestionar_asignaturas.html',context)

"""
@login_required(login_url='login')
@admin
def cambiar_nombre_asignatura(request):
    if request.method == 'POST':
        form_cambio_nombre = CambiarNombreAsignaturaForm(request.POST)
        if form_cambio_nombre.is_valid():
            asignatura_id = form_cambio_nombre.cleaned_data.get('asignatura_id')
            asignatura = get_object_or_404(Asignatura, pk=asignatura_id)
            viejo_nombre = asignatura.nombre
            nuevo_nombre = form_cambio_nombre.cleaned_data.get('nombre')
            asignatura.nombre = nuevo_nombre
            asignatura.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form_cambio_nombre.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
"""

@login_required(login_url='login')
@admin
def detalles_asignatura(request, id):

    asignatura = get_object_or_404(Asignatura, pk = id)
    estudiantes = asignatura.estudiantes.all()
    profesores = asignatura.profesores.all()

    form_apuntar_profesor = ApuntarProfesoresForm(profesores=profesores)
    form_apuntar_estudiantes = ApuntarEstudiantesForm(estudiantes=estudiantes)

    if request.method == 'POST':
        if 'form-apuntar-profesor' in request.POST:
            form_apuntar_profesor = ApuntarProfesoresForm(request.POST, profesores=profesores)
            if form_apuntar_profesor.is_valid():
                nuevos_profesores = form_apuntar_profesor.cleaned_data.get('profesores')
                asignatura.profesores.add(*nuevos_profesores)
                asignatura.save()
                messages.success(request, 'Profesor/es se apuntaron correctamente a '+asignatura.nombre, extra_tags='messages_profesores')
                return redirect('detalles_asignatura', id=id)
            
        elif 'form-apuntar-estudiante' in request.POST:
            form_apuntar_estudiantes = ApuntarEstudiantesForm(request.POST, estudiantes=estudiantes)
            if form_apuntar_estudiantes.is_valid():
                nuevos_estudiantes = form_apuntar_estudiantes.cleaned_data.get('estudiantes')
                asignatura.estudiantes.add(*nuevos_estudiantes)
                asignatura.save()
                messages.success(request, 'Estudiante/s se apuntaron correctamente a '+asignatura.nombre, extra_tags='messages_estudiantes')
                return redirect('detalles_asignatura', id=id)
            return redirect('detalles_asignatura', id=id)
    else:
        context = {
            'asignatura':asignatura, 
            'estudiantes':estudiantes, 
            'profesores':profesores,
            'form_apuntar_profesor': form_apuntar_profesor,
            'form_apuntar_estudiantes': form_apuntar_estudiantes
        }

        return render(request, 'detalles_asignatura.html',context)

@login_required(login_url='login')
@admin
def desapuntar_profesor(request):

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        id_profesor = request.POST.get('id_profesor')
        id_asignatura = request.POST.get('id_asignatura')
        
        try:
            profesor = get_object_or_404(Profesor, pk=id_profesor)
            asignatura = get_object_or_404(Asignatura, pk=id_asignatura)
            asignatura.profesores.remove(profesor)
            messages.success(request, 'Profesor desapuntado de la asignatura correctamente', extra_tags='messages_profesores')
            return JsonResponse({'status':'success'})
        except:
            return JsonResponse({'status':'error', 'message':'Algo falló, inténtelo más tarde'})
    else:
        return redirect('panel_administracion')
    
@login_required(login_url='login')
@admin
def desapuntar_estudiante(request):

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        id_estudiante = request.POST.get('id_estudiante')
        id_asignatura = request.POST.get('id_asignatura')
        try:
            estudiante = get_object_or_404(Estudiante, pk=id_estudiante)
            asignatura = get_object_or_404(Asignatura, pk=id_asignatura)
            asignatura.estudiantes.remove(estudiante)
            messages.success(request, 'Estudiante desapuntado de la asignatura correctamente', extra_tags='messages_estudiantes')
            return JsonResponse({'status':'success'})
        except:
            return JsonResponse({'status':'error', 'message':'Algo falló, inténtelo más tarde'})
    else:
        return redirect('panel_administracion')

@login_required(login_url='login')
@admin
def crear_estudiante(request):

    form = EstudianteForm()

    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            nombre = form.cleaned_data.get('nombre')
            messages.success(request, 'El estudiante '+nombre+' se añadió correctamente a la plataforma')
            if 'guardar_otro' in request.POST:
                return redirect('crear_estudiante')
            else:
                return redirect('gestionar_estudiantes')


    context = {'form':form}
    return render(request, 'estudiante_form.html', context)

@login_required(login_url='login')
@admin
def crear_profesor(request):

    form = ProfesorForm()

    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            nombre = form.cleaned_data.get('nombre')
            messages.success(request, 'El profesor '+nombre+' se añadió correctamente a la plataforma')
            if 'guardar_otro' in request.POST:
                return redirect('crear_profesor')
            else:
                return redirect('gestionar_profesores')


    context = {'form':form}
    return render(request, 'profesor_form.html', context)

@login_required(login_url='login')
@admin
def crear_asignatura(request):

    form = AsignaturaForm()

    if request.method == 'POST':
        form = AsignaturaForm(request.POST)
        if form.is_valid():
            form.save()
            nombre = form.cleaned_data.get('nombre')
            messages.success(request, 'La asignatura '+nombre+' se añadió correctamente a la plataforma')
            if 'guardar_otra' in request.POST:
                return redirect('crear_asignatura')
            else:
                return redirect('gestionar_asignaturas')


    context = {'form':form}
    return render(request, 'asignatura_form.html', context)

@login_required(login_url='login')
@admin
def eliminar_asignatura(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        id_asignatura = request.POST.get('id_asignatura')
        try:
            asignatura = get_object_or_404(Asignatura, pk=id_asignatura)
            asignatura.delete()
            messages.success(request, 'La asignatura '+asignatura.nombre+' se eliminó correctamente')
            return JsonResponse({'status':'success'})
        except:
            return JsonResponse({'status':'error', 'message':'Algo falló, inténtelo más tarde'})
    
    else:
        return redirect('panel_administracion')


@login_required(login_url='login')
@admin
def eliminar_profesor(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        id_profesor = request.POST.get('id_profesor')
        try:
            profesor = get_object_or_404(Profesor, pk=id_profesor)
            profesor.delete()
            messages.success(request, 'El profesor '+profesor.nombre+' se eliminó correctamente de la plataforma')
            return JsonResponse({'status':'success'})
        except:
            return JsonResponse({'status':'error', 'message':'Algo falló, inténtelo más tarde'})
    
    else:
        return redirect('panel_administracion')


@login_required(login_url='login')
@admin
def eliminar_estudiante(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        id_estudiante = request.POST.get('id_estudiante')
        try:
            estudiante = get_object_or_404(Estudiante, pk=id_estudiante)
            estudiante.delete()
            messages.success(request, 'El estudiante '+estudiante.nombre+' se eliminó correctamente de la plataforma')
            return JsonResponse({'status':'success'})
        except:
            return JsonResponse({'status':'error', 'message':'Algo falló, inténtelo más tarde'})
    
    else:
        return redirect('panel_administracion')
