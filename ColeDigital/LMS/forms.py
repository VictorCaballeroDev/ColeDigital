from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


from .models import *

class AsignaturaForm(ModelForm):
    class Meta:
        model = Asignatura
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'ej. Matemáticas 4º ESO'}),
            'profesores': forms.SelectMultiple(attrs={'placeholder': 'Puede asignar profesores ahora o más tarde'}),
            'estudiantes': forms.SelectMultiple(attrs={'placeholder': 'Puede asignar estudiantes ahora o más tarde'}),
        }
    


class EstudianteForm(UserCreationForm):
    
    nombre = forms.CharField(max_length=200)
    correo = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'nombre', 'correo')
    
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['username'].widget.attrs.update({'placeholder': 'ej. estudiantevg_5412'})
            self.fields['nombre'].widget.attrs.update({'placeholder': 'ej. Víctor González'})
            self.fields['correo'].widget.attrs.update({'placeholder': 'ej. victorgonzalez@colegio.com'})

    def save(self, commit=True):
        user = super(EstudianteForm, self).save(commit=False)
        user.email = self.cleaned_data['correo']
        user.save()

        estudiante = Estudiante.objects.create(
            user=user,
            nombre = self.cleaned_data['nombre'],
            correo = self.cleaned_data['correo']
        )

        grupo = Group.objects.get(name='estudiante')
        user.groups.add(grupo)

        return user
    
class ProfesorForm(UserCreationForm):
    nombre = forms.CharField(
        max_length=200,
        error_messages={
            'required': 'Este campo es obligatorio.',
            'max_length': 'El nombre no puede tener más de 200 caracteres.'
    })

    correo = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'nombre', 'correo')

        
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['username'].widget.attrs.update({'placeholder': 'ej. profesorvg_5412'})
            self.fields['nombre'].widget.attrs.update({'placeholder': 'ej. Víctor González'})
            self.fields['correo'].widget.attrs.update({'placeholder': 'ej. victorgonzalez@colegio.com'})

    def save(self, commit=True):
        user = super(ProfesorForm, self).save(commit=False)
        user.email = self.cleaned_data['correo']
        user.save()

        profesor = Profesor.objects.create(
            user=user,
            nombre=self.cleaned_data['nombre'],
            correo=self.cleaned_data['correo']
        )

        grupo = Group.objects.get(name='profesor')
        user.groups.add(grupo)

        return user
    
class ApuntarProfesoresForm(forms.ModelForm):

    class Meta:
        model = Asignatura
        fields = ['profesores']
        widgets = {
            'profesores': forms.SelectMultiple(attrs={'required':'true','class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        profesores = kwargs.pop('profesores')
        super(ApuntarProfesoresForm, self).__init__(*args, **kwargs)
        self.fields['profesores'].queryset = Profesor.objects.exclude(pk__in=profesores)

    

class ApuntarEstudiantesForm(forms.ModelForm):
    
    class Meta:
        model = Asignatura
        fields = ['estudiantes']
        widgets = {
            'estudiantes': forms.SelectMultiple(attrs={'required':'true','class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        estudiantes = kwargs.pop('estudiantes')
        super(ApuntarEstudiantesForm, self).__init__(*args, **kwargs)
        self.fields['estudiantes'].queryset = Estudiante.objects.exclude(pk__in=estudiantes)


class CambiarNombreAsignaturaForm(forms.ModelForm):
    
    asignatura_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Asignatura
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'required':'true', 'placeholder': 'Nuevo nombre para la asignatura', 'class': 'form-control'}),
        }

### MODIFICACIÓN DEL FILEFIELD
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class CrearTareaForm(forms.ModelForm):

    archivos = MultipleFileField(widget=MultipleFileInput(attrs={'class':'form-control', 'required': 'false'}))

    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'fecha_entrega', 'archivos']
        widgets = {
            'titulo': forms.TextInput(attrs={'required':'true', 'placeholder': 'ej. Tarea de matemáticas', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha_entrega': forms.DateTimeInput(attrs={'placeholder': 'Sin fecha de entrega', 'class': 'form-control datepicker', 'data-date-format': 'dd/mm/yyyy'}),
        }


class CrearEntregaForm(forms.ModelForm):

    archivos = MultipleFileField(widget=MultipleFileInput(attrs={'class':'form-control'}))

    class Meta:
        model = Entrega
        fields = ['comentario', 'archivos']
        widgets = {
            'comentario': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CorreccionEntregaForm(forms.ModelForm):

    class Meta:
        model = CorreccionEntrega
        fields = ['puntuacion', 'comentario']
        widgets = {
            'puntuacion': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CrearReunionForm(forms.ModelForm):
    class Meta:
        model = Reunion
        fields = ['titulo', 'fecha_inicio', 'enlace', 'plataforma']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej. Sesión de clase'}),
            'fecha_inicio': forms.DateTimeInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Seleccione una fecha en el calendario...'}),
            'enlace': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'ej. https://zoom.us/es'}),
            'plataforma': forms.Select(attrs={'class': 'form-control'}),
        }