# Generated by Django 5.1.4 on 2024-12-13 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IGL_App', '0015_alter_patient_mot_de_passe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='mot_de_passe',
            field=models.CharField(default='pbkdf2_sha256$870000$IUE0ua8gGyWcbSj1Fup7gW$4AYtiGehkg2Pf9gpZfIUMpqPSYX3GP0pKo1CX3nr6Ek=', max_length=255),
        ),
    ]
