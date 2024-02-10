# Generated by Django 5.0.1 on 2024-01-21 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0002_componente_horarioproducto'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleEnsambleComponente',
            fields=[
                ('id_detalleensamblec', models.AutoField(primary_key=True, serialize=False)),
                ('cantidadhijo', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
            options={
                'db_table': 'detalleensamblecomponente',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DetalleEnsambleProducto',
            fields=[
                ('id_detalleensamblep', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad_hijo', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
            options={
                'db_table': 'detalleensambleproducto',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EnsambleComponente',
            fields=[
                ('id_ensamblec', models.AutoField(primary_key=True, serialize=False)),
                ('padrecantidad', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
            options={
                'db_table': 'ensamblecomponente',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EnsambleProducto',
            fields=[
                ('id_emsamblep', models.AutoField(primary_key=True, serialize=False)),
                ('padre_cantidad', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
            options={
                'db_table': 'ensambleproducto',
                'managed': False,
            },
        ),
    ]
