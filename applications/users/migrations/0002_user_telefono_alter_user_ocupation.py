# Generated by Django 5.1.2 on 2024-10-22 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telefono',
            field=models.CharField(default='123', max_length=50, verbose_name='Telefono'),
        ),
        migrations.AlterField(
            model_name='user',
            name='ocupation',
            field=models.CharField(blank=True, choices=[('0', 'Administrador'), ('1', 'Cajero'), ('2', 'Cocinero')], max_length=1),
        ),
    ]
