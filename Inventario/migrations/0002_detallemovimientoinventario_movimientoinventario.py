# Generated by Django 5.0 on 2024-02-20 01:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleMovimientoInventario',
            fields=[
                ('id_detallemovimiento', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=9)),
                ('tipo', models.CharField(choices=[('E', 'Entrada'), ('S', 'Salida'), ('R', 'Reversion')], max_length=1)),
            ],
            options={
                'db_table': 'detallemovimientoinventario',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MovimientoInventario',
            fields=[
                ('id_movimientoinventario', models.AutoField(primary_key=True, serialize=False)),
                ('fechahora', models.DateTimeField(default=django.utils.timezone.now)),
                ('tipomovimiento', models.CharField(choices=[('E', 'Entrada'), ('S', 'Salida'), ('P', 'Preparacion'), ('R', 'Reversion')], max_length=1)),
            ],
            options={
                'db_table': 'movimientoinventario',
                'managed': False,
            },
        ),
    ]