# Generated by Django 5.1.4 on 2024-12-07 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IGL_App', '0002_alter_patient_medecin_traitant_dossierpatient_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='staff',
            options={'managed': False},
        ),
    ]
