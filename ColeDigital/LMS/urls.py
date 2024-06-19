from django.urls import path, include
from .views import *
urlpatterns = [
    path('login/', inicio_sesion, name="login"),
    path('logout/', cerrar_sesion, name="logout"),


    path('', home, name="home"),
    path('presentacion_asignatura_estudiantes/<str:id_asignatura>', presentacion_asignatura_estudiantes, name="presentacion_asignatura_estudiantes"),
    path('presentacion_asignatura_profesores/<str:id_asignatura>', presentacion_asignatura_profesores, name="presentacion_asignatura_profesores"),

    ## URLS ADMINISTRACION ##
    path('administracion/', panel_administracion, name="panel_administracion"),
    path('gestionar_estudiantes/', gestionar_estudiantes, name="gestionar_estudiantes"),
    path('gestionar_profesores/', gestionar_profesores, name="gestionar_profesores"),
    path('gestionar_asignaturas/', gestionar_asignaturas, name="gestionar_asignaturas"),
    path('detalles_asignatura/<str:id>', detalles_asignatura, name='detalles_asignatura'),
    path('desapuntar_profesor/', desapuntar_profesor, name='desapuntar_profesor'),
    path('desapuntar_estudiante/', desapuntar_estudiante, name='desapuntar_estudiante'),
    path('crear_estudiante/', crear_estudiante, name='crear_estudiante'),
    path('crear_profesor/', crear_profesor, name='crear_profesor'),
    path('crear_asignatura/', crear_asignatura, name='crear_asignatura'),
    path('eliminar_asignatura/', eliminar_asignatura, name='eliminar_asignatura'),
    path('eliminar_profesor/', eliminar_profesor, name='eliminar_profesor'),
    path('eliminar_estudiante/', eliminar_estudiante, name='eliminar_estudiante'),
    #path('cambiar_nombre_asignatura/', cambiar_nombre_asignatura, name='cambiar_nombre_asignatura'),
]