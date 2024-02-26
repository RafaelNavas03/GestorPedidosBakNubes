# Generated by Django 5.0.2 on 2024-02-26 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CodigoFactura', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Codigoautorizacion',
            fields=[
                ('id_codigosauto', models.AutoField(primary_key=True, serialize=False)),
                ('codigo_autorizacion', models.CharField(max_length=49)),
                ('fecha_vencimiento', models.DateField(blank=True, null=True)),
                ('fecha_autorizacion', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'codigoautorizacion',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Puntofacturacion',
            fields=[
                ('id_puntofacturacion', models.AutoField(primary_key=True, serialize=False)),
                ('nombrepunto', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=3)),
                ('sestado', models.CharField(max_length=1)),
            ],
            options={
                'db_table': 'puntofacturacion',
                'managed': False,
            },
        ),
    ]