from django.http import HttpResponse
from django.shortcuts import redirect

from .models import *

# Para vistas que solo puedan acceder usuarios sin autenticar
def usuario_sin_autenticacion(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

# Recibe por parámetro una lista con los grupos de usuario que pueden acceder a la vista, redirige teniendo en cuenta este parametro
def usuarios_habilitados(grupos_habilitados=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            grupo = None
            if request.user.groups.exists():
                grupo = request.user.groups.all()[0].name

            if grupo in grupos_habilitados:
                return view_func(request, *args, **kwargs)
            else:
                if grupo == 'admin':
                    return redirect('panel_administracion')
                else:
                    return HttpResponse("No se pudo acceder a esta página")
        return wrapper_func
    return decorator

# Solo los usuarios del grupo 'admin' pueden acceder a esta vista
def admin(view_func):
    def wrapper_func(request, *args, **kwargs):
        grupo = None
        if request.user.groups.exists():
            grupo = request.user.groups.all()[0].name

        if grupo != 'admin':
            return redirect('home')
        
        if grupo == 'admin':
            return view_func(request, *args, **kwargs)
        
    return wrapper_func

def estudiante_apuntado_asignatura(view_func):
    def wrapper_func(request, *args, **kwargs):
        estudiante = Estudiante.objects.get(user=request.user)
        
        try:
            asignatura = Asignatura.objects.get(id=kwargs.get('id_asignatura'))
        except:
            return redirect('home')
        

        if estudiante in asignatura.estudiantes.all():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrapper_func


def tarea_asignada_estudiante(view_func):
    def wrapper_func(request, *args, **kwargs):
        estudiante = Estudiante.objects.get(user=request.user)
        
        try:
            asignatura = Asignatura.objects.get(tareas= Tarea.objects.get(id = kwargs.get('id_tarea')))
        except:
            return redirect('home')
        

        if estudiante in asignatura.estudiantes.all():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrapper_func

def profesor_apuntado_asignatura(view_func):
    def wrapper_func(request, *args, **kwargs):
        profesor = Profesor.objects.get(user=request.user)
        
        try:
            asignatura = Asignatura.objects.get(id=kwargs.get('id_asignatura'))
        except:
            return redirect('home')
        

        if profesor in asignatura.profesores.all():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrapper_func

def tarea_asignada_estudiante(view_func):
    def wrapper_func(request, *args, **kwargs):
        estudiante = Estudiante.objects.get(user=request.user)

        try:
            tarea = Tarea.objects.get(id=kwargs.get('id_tarea'))
            asignatura = Asignatura.objects.get(estudiantes=estudiante,tareas=tarea)
            return view_func(request, *args, **kwargs)
        except:
            return redirect('home')
    return wrapper_func
        