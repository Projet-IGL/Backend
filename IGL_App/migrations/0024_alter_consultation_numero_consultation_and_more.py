# Generated by Django 5.1.3 on 2024-12-14 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IGL_App', '0023_alter_patient_mot_de_passe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='numero_consultation',
            field=models.IntegerField(default=0, unique=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='mot_de_passe',
            field=models.CharField(default='pbkdf2_sha256$870000$WoV8SXufdcjTace58Dt3Ka$VRpV5k5rernVKLSm4UHlhdFENvzA26r/6rASCOAMecM=', max_length=255),
        ),
    ]
