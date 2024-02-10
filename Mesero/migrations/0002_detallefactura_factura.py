# Generated by Django 5.0.1 on 2024-02-08 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mesero', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleFactura',
            fields=[
                ('id_detallefactura', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'detallefactura',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id_factura', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_emision', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'factura',
                'managed': False,
            },
        ),
    ]
