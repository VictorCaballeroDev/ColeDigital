from django.contrib import admin
from .models import *


admin.site.register(Estudiante)
admin.site.register(Profesor)
admin.site.register(Asignatura)
admin.site.register(Tarea)
admin.site.register(Foro)
admin.site.register(Mensaje)
admin.site.register(Reunion)
admin.site.register(ArchivoAdjuntoTarea)
admin.site.register(Entrega)
admin.site.register(ArchivoAdjuntoEntrega)
admin.site.register(CorreccionEntrega)