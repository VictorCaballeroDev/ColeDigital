from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Entrega

@receiver(post_save, sender=Entrega)
def actualizar_puntualidad(sender, instance, created, **kwargs):
    if created:
        if instance.fecha_entrega < instance.tarea.fecha_entrega:
            instance.puntual = True
        else:
            instance.puntual = False
        instance.save()