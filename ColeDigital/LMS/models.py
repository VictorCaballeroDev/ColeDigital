from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Estudiante(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200, null=True)
    correo = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.nombre
    
class Profesor(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200, null=True)
    correo = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.nombre
    
class Asignatura(models.Model):
    nombre = models.CharField(max_length=200, null=True)

    estudiantes = models.ManyToManyField(Estudiante, blank=True)
    profesores = models.ManyToManyField(Profesor, blank=True)

    def __str__(self):
        return self.nombre


class Foro(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name='foros')
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Tarea(models.Model):
    titulo = models.CharField(max_length=200, null=True)
    descripcion = models.CharField(max_length=200, null=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    asignatura = models.ForeignKey(Asignatura, null=False, on_delete=models.CASCADE, related_name='tareas')

    def __str__(self):
        return self.titulo