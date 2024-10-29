# Generated by Django 5.1.2 on 2024-10-28 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caja', '0003_alter_caja_abierta_caja_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caja',
            name='total_caja',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total caja'),
        ),
        migrations.AlterField(
            model_name='caja',
            name='total_egresos',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total Egreso'),
        ),
        migrations.AlterField(
            model_name='caja',
            name='total_ingresos',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total Ingreso'),
        ),
    ]
