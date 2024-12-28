# Generated by Django 5.1.4 on 2024-12-27 23:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0009_patient_telephone_urgence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='dossier_patient',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient', to='backendapp.dossierpatient'),
        ),
    ]