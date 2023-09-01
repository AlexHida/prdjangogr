# Generated by Django 4.0.6 on 2023-08-31 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('correo', models.CharField(max_length=100)),
                ('usua', models.CharField(default='guest', max_length=50)),
                ('pass1', models.CharField(default='guest', max_length=100)),
                ('asistencia', models.IntegerField()),
            ],
        ),
    ]