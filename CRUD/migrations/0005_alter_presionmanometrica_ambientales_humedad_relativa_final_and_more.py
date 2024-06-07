# Generated by Django 4.2.13 on 2024-05-27 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRUD', '0004_patronespresionmanometrica_reproducibilidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presionmanometrica',
            name='ambientales_humedad_relativa_final',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='presionmanometrica',
            name='ambientales_humedad_relativa_inicial',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='presionmanometrica',
            name='ambientales_presion_barometrica_final',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='presionmanometrica',
            name='ambientales_presion_barometrica_inicial',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='presionmanometrica',
            name='ambientales_temperatura_final',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='presionmanometrica',
            name='ambientales_temperatura_inicial',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
