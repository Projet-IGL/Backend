# Generated by Django 5.1.4 on 2024-12-25 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0005_consultation_numero_consultation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='numero_consultation',
            field=models.IntegerField(default=0),
        ),
    ]