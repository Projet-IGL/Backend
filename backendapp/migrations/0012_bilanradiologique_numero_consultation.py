# Generated by Django 5.1.4 on 2024-12-29 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0011_alter_bilanbiologique_graphe'),
    ]

    operations = [
        migrations.AddField(
            model_name='bilanradiologique',
            name='numero_consultation',
            field=models.IntegerField(default=1),
        ),
    ]
