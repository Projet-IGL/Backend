# Generated by Django 5.1.4 on 2024-12-29 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0010_alter_patient_dossier_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bilanbiologique',
            name='graphe',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
