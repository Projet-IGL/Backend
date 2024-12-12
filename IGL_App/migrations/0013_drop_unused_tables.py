from django.db import migrations, connection

def drop_unused_tables(apps, schema_editor):
    with connection.cursor() as cursor:
        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        # List of tables to drop
        tables_to_drop = [
            'igl_app_staff', 
            'igl_app_soins', 
            'igl_app_patient', 
            'igl_app_ordonnance',
            'igl_app_dossierpatient', 
            'igl_app_consultation', 
            'igl_app_bilanradiologique',
            'igl_app_bilanbiologique',
        ]
        
        # Drop each table from the list
        for table in tables_to_drop:
            cursor.execute(f"DROP TABLE IF EXISTS {table};")
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

class Migration(migrations.Migration):

    dependencies = [
        ('IGL_App', '0012_alter_patient_mot_de_passe'),
    ]

    operations = [
        migrations.RunPython(drop_unused_tables),
    ]