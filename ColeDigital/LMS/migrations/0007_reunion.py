# Generated by Django 5.0.6 on 2024-07-03 13:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0006_remove_foro_contenido_remove_foro_fecha_creacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reunion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateTimeField()),
                ('enlace', models.URLField()),
                ('plataforma', models.CharField(choices=[('zoom', 'Zoom'), ('google_meet', 'Google Meet'), ('teams', 'Microsoft Teams')], max_length=50)),
                ('asignatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reuniones', to='LMS.asignatura')),
            ],
        ),
    ]
