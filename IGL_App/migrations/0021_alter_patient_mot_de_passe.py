# Generated by Django 5.1.3 on 2024-12-14 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IGL_App', '0020_alter_patient_mot_de_passe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='mot_de_passe',
            field=models.CharField(default='pbkdf2_sha256$870000$6nXSEDb0LGvO5NnX9HvDC0$FiHuTX9+ZEqL6DOVo4XWhKJP/yurChQFnPE8a3OEIbY=', max_length=255),
        ),
    ]
