# Generated by Django 5.1.4 on 2024-12-25 10:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0007_ordonnance_medicament'),
    ]

    operations = [
        migrations.CreateModel(
            name='BilanBiologique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resultat_analyse', models.TextField()),
                ('resultat_examen_imagerie', models.TextField()),
                ('date_examen', models.DateTimeField()),
                ('graphe', models.BinaryField(blank=True, null=True)),
                ('glycemie', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('pression_arterielle', models.CharField(blank=True, max_length=20, null=True)),
                ('cholesterol', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('dossier_patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backendapp.dossierpatient')),
                ('laborantin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patients', to='backendapp.laborantin')),
            ],
            options={
                'db_table': 'Bilan_Biologique',
            },
        ),
        migrations.CreateModel(
            name='BilanRadiologique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compte_rendu', models.TextField()),
                ('images', models.ImageField(blank=True, null=True, upload_to='')),
                ('date_examen', models.DateTimeField()),
                ('dossier_patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backendapp.dossierpatient')),
                ('radiologue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patients', to='backendapp.radiologue')),
            ],
            options={
                'db_table': 'Bilan_Radiologique',
            },
        ),
    ]
