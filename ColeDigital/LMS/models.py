from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
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
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not hasattr(self, 'foro'):
            Foro.objects.create(asignatura=self, titulo=f"Foro de {self.nombre}")


class Foro(models.Model):
    asignatura = models.OneToOneField(Asignatura, on_delete=models.CASCADE, related_name='foro')
    titulo = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo

# Se adapta en patrón composite
class Mensaje(models.Model): #Component
    foro = models.ForeignKey('Foro', related_name='mensajes', on_delete=models.CASCADE)
    autor = models.ForeignKey(User, related_name='mensajes', on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    mensaje_padre = models.ForeignKey('self', related_name='respuestas', null=True, blank=True, on_delete=models.CASCADE) #Composite

    def __str__(self):
        return f"{self.autor.username}: {self.contenido[:30]+'...'}"

    #Leaf
    @property
    def es_hoja(self):
        return not self.respuestas.exists()

class Tarea(models.Model):
    titulo = models.CharField(max_length=200, null=True)
    descripcion = models.CharField(max_length=200, null=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    asignatura = models.ForeignKey(Asignatura, null=False, on_delete=models.CASCADE, related_name='tareas')

    def __str__(self):
        return self.titulo
    
class ArchivoAdjuntoTarea(models.Model):
    tarea = models.ForeignKey(Tarea, related_name='archivos', on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='archivos_tareas/')

    def __str__(self):
        return f"{self.tarea.titulo} - {self.archivo.name}"


class Entrega(models.Model):
    tarea = models.ForeignKey(Tarea, null=False, on_delete=models.CASCADE, related_name='entregas')
    comentario = models.CharField(max_length=1000, null=True)
    estudiante = models.ForeignKey(Estudiante, null=False, on_delete=models.CASCADE)
    fecha_entrega = models.DateTimeField(auto_now_add=True)
    puntual = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.tarea.titulo} - {self.estudiante.nombre}"
    
class ArchivoAdjuntoEntrega(models.Model):
    entrega = models.ForeignKey(Entrega, null=False, on_delete=models.CASCADE, related_name='archivos')
    archivo = models.FileField(null=True, upload_to='archivos_entregas/')

    def __str__(self):
        return f"{self.entrega.tarea} - {self.archivo.name}"

class CorreccionEntrega(models.Model):
    entrega = models.OneToOneField(Entrega, null=True, blank=True, on_delete=models.CASCADE, related_name='correccion')
    corrector = models.ForeignKey(Profesor, null=False, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(default=100, validators=[MaxValueValidator(100), MinValueValidator(0)])
    comentario = models.CharField(null=True, max_length=1000)

class Reunion(models.Model):
    PLATAFORMAS = [
        ('zoom', 'Zoom'),
        ('google_meet', 'Google Meet'),
        ('teams', 'Microsoft Teams'),
        ('otra', 'Otra')
    ]

    titulo = models.CharField(max_length=200, null=True)
    asignatura = models.ForeignKey('Asignatura', on_delete=models.CASCADE, related_name='reuniones')
    fecha_inicio = models.DateTimeField()
    enlace = models.URLField()
    plataforma = models.CharField(max_length=50, choices=PLATAFORMAS)

    def __str__(self):
        return f"{self.asignatura.nombre} - {self.plataforma} - {self.fecha_inicio}"