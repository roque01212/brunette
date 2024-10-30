# Generated by Django 5.1.2 on 2024-10-29 20:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('caja', '0005_mesas'),
    ]

    operations = [
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_prod', models.CharField(max_length=100)),
                ('precio_prod', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock_min_prod', models.PositiveIntegerField()),
                ('stock_actual_prod', models.PositiveIntegerField()),
                ('existencia_insumo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pedidos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_pago_pedido', models.CharField(choices=[('0', 'Tarjeta'), ('1', 'Efectivo'), ('2', 'Tranferecia'), ('3', 'Otro')], max_length=2, verbose_name='Tipo de pago')),
                ('fecha_hs_pedido', models.DateTimeField(auto_now_add=True)),
                ('entrega_pedido', models.BooleanField(default=False)),
                ('pagado_pedido', models.BooleanField(default=False)),
                ('caja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caja.caja')),
                ('mesa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caja.mesas')),
            ],
            options={
                'verbose_name': 'Pedidos',
                'verbose_name_plural': 'Pedidoss',
            },
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_pedido', models.IntegerField()),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cocina.pedidos')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cocina.productos')),
            ],
            options={
                'verbose_name': 'DetallePedido',
                'verbose_name_plural': 'DetallePedidos',
            },
        ),
    ]
