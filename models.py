# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BilanBiologique(models.Model):
    dossier_patient = models.ForeignKey('DossierPatient', models.DO_NOTHING, blank=True, null=True)
    laborantin = models.ForeignKey('Staff', models.DO_NOTHING, blank=True, null=True)
    resultat_analyse = models.TextField(blank=True, null=True)
    resultat_examen_imagerie = models.TextField(blank=True, null=True)
    date_examen = models.DateTimeField(blank=True, null=True)
    graphe = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bilan_biologique'


class BilanRadiologique(models.Model):
    dossier_patient = models.ForeignKey('DossierPatient', models.DO_NOTHING, blank=True, null=True)
    radiologue = models.ForeignKey('Staff', models.DO_NOTHING, blank=True, null=True)
    compte_rendu = models.TextField(blank=True, null=True)
    images = models.TextField(blank=True, null=True)
    date_examen = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bilan_radiologique'


class Consultation(models.Model):
    dossier_patient = models.ForeignKey('DossierPatient', models.DO_NOTHING, blank=True, null=True)
    date_consultation = models.DateTimeField(blank=True, null=True)
    bilan_prescrit = models.TextField(blank=True, null=True)
    resume = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'consultation'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DossierPatient(models.Model):
    patient = models.ForeignKey('Patient', models.DO_NOTHING, blank=True, null=True)
    medecintraitant = models.ForeignKey('Staff', models.DO_NOTHING, db_column='medecinTraitant_id', blank=True, null=True)  # Field name made lowercase.
    code_qr = models.CharField(max_length=255, blank=True, null=True)
    etat = models.CharField(max_length=20, blank=True, null=True)
    antلcلdents = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dossier_patient'


class IglAppBilanbiologique(models.Model):
    id = models.BigAutoField(primary_key=True)
    resultat_analyse = models.TextField()
    resultat_examen_imagerie = models.TextField()
    date_examen = models.DateTimeField()
    graphe = models.TextField()
    laborantin = models.ForeignKey('IglAppStaff', models.DO_NOTHING, blank=True, null=True)
    dossier_patient = models.ForeignKey('IglAppDossierpatient', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'igl_app_bilanbiologique'


class IglAppBilanradiologique(models.Model):
    id = models.BigAutoField(primary_key=True)
    compte_rendu = models.TextField()
    images = models.TextField()
    date_examen = models.DateTimeField()
    radiologue = models.ForeignKey('IglAppStaff', models.DO_NOTHING, blank=True, null=True)
    dossier_patient = models.ForeignKey('IglAppDossierpatient', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'igl_app_bilanradiologique'


class IglAppConsultation(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_consultation = models.DateTimeField()
    bilan_prescrit = models.TextField()
    resume = models.TextField()
    dossier_patient = models.ForeignKey('IglAppDossierpatient', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'igl_app_consultation'


class IglAppDossierpatient(models.Model):
    id = models.BigAutoField(primary_key=True)
    code_qr = models.CharField(max_length=255)
    etat = models.CharField(max_length=20)
    antecedents = models.TextField()
    medecin_traitant = models.ForeignKey('IglAppStaff', models.DO_NOTHING, blank=True, null=True)
    patient = models.ForeignKey('IglAppPatient', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'igl_app_dossierpatient'


class IglAppOrdonnance(models.Model):
    id = models.BigAutoField(primary_key=True)
    medicament = models.TextField()
    quantite = models.IntegerField()
    duree = models.CharField(max_length=255)
    consultation = models.ForeignKey(IglAppConsultation, models.DO_NOTHING)
    dossier_patient = models.ForeignKey(IglAppDossierpatient, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'igl_app_ordonnance'


class IglAppPatient(models.Model):
    id = models.BigAutoField(primary_key=True)
    nss = models.CharField(unique=True, max_length=15)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    mutuelle = models.CharField(max_length=100)
    personne_a_contacter = models.CharField(max_length=100)
    telephone_contact = models.CharField(max_length=20)
    medecin_traitant = models.ForeignKey('IglAppStaff', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'igl_app_patient'


class IglAppSoins(models.Model):
    id = models.BigAutoField(primary_key=True)
    observation_etat_patient = models.TextField()
    medicament_pris = models.IntegerField()
    description_soins = models.TextField()
    date_soin = models.DateTimeField()
    dossier_patient = models.ForeignKey(IglAppDossierpatient, models.DO_NOTHING)
    infirmier = models.ForeignKey('IglAppStaff', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'igl_app_soins'


class IglAppStaff(models.Model):
    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.CharField(unique=True, max_length=254)
    adresse = models.CharField(max_length=255)
    date_naissance = models.DateField()
    mot_de_passe = models.CharField(max_length=255)
    role = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'igl_app_staff'


class Ordonnance(models.Model):
    dossier_patient = models.ForeignKey(DossierPatient, models.DO_NOTHING, blank=True, null=True)
    consutlation = models.ForeignKey(Consultation, models.DO_NOTHING, blank=True, null=True)
    medicament = models.TextField(blank=True, null=True)
    quantite = models.IntegerField(blank=True, null=True)
    durلe = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ordonnance'


class Patient(models.Model):
    nss = models.CharField(unique=True, max_length=15, blank=True, null=True)
    nom = models.CharField(max_length=100, blank=True, null=True)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    mutuelle = models.CharField(max_length=100, blank=True, null=True)
    medecin_traitant = models.ForeignKey('Staff', models.DO_NOTHING, blank=True, null=True)
    personne_a_contacter = models.CharField(max_length=100, blank=True, null=True)
    telephone_contact = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient'


class Soins(models.Model):
    dossier_patient = models.ForeignKey(DossierPatient, models.DO_NOTHING, blank=True, null=True)
    infirmier = models.ForeignKey('Staff', models.DO_NOTHING, blank=True, null=True)
    observation_etat_patient = models.TextField(blank=True, null=True)
    medicament_pris = models.IntegerField(blank=True, null=True)
    description_soins = models.TextField(blank=True, null=True)
    date_soin = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'soins'


class Staff(models.Model):
    nom = models.CharField(max_length=100, blank=True, null=True)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    mot_de_passe = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staff'
