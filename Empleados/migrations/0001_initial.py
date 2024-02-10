# Generated by Django 5.0 on 2023-12-29 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JefeCocina',
            fields=[
                ('id_jefecocina', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=300)),
                ('apellido', models.CharField(max_length=300)),
                ('telefono', models.CharField(blank=True, max_length=10, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'jefecocina',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Mesero',
            fields=[
                ('id_mesero', models.AutoField(primary_key=True, serialize=False)),
                ('telefono', models.CharField(max_length=10)),
                ('apellido', models.CharField(max_length=300)),
                ('nombre', models.CharField(max_length=300)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'meseros',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Motorizado',
            fields=[
                ('id_motorizado', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=300)),
                ('apellido', models.CharField(max_length=300)),
                ('telefono', models.CharField(blank=True, max_length=10, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'motorizados',
                'managed': False,
            },
        ),
    ]
