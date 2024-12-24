# Generated by Django 5.1.4 on 2024-12-23 18:19

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0002_consultation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='bilan_prescrit',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('bilan bio-Glycémie', 'bilan bio-Glycémie'), ('bilan bio-Pression artérielle', 'bilan bio-Pression artérielle'), ('bilan bio-Niveau Cholésterole', 'bilan bio-Niveau Cholésterole'), ('bilan Rad-IRM', 'bilan Rad-IRM'), ('bilan Rad-Echographie', 'bilan Rad-Echographie'), ('bilan Rad-Radiographie', 'bilan Rad-Radiographie'), ('Aucun bilan', 'Aucun Bilan')], max_length=149),
        ),
    ]