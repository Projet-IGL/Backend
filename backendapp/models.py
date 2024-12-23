from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('Administrateur', 'administrateur'),
        ('Patient', 'patient'),
        ('Medecin', 'medecin'),
        ('Infirmier', 'infirmier'),
        ('Laborantin', 'laborantin'),
        ('Radiologue', 'radiologue'),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    date_naissance = models.DateField(blank = True,null= True) 
    # added blank/null = true to date de naissance just because i couldn't create a superuser 
    # via the command line so i just decided to allow it to be blank or null
    # we do not need the date_naissance for a superuser anyway
    adresse = models.CharField(max_length=255)
    numero_telephone = models.CharField(max_length=15)

    class Meta:
        db_table = 'users'  # Custom table name for the model

class Administrateur(User):
    # Add additional fields specific to Administrateurs if needed
    pass

    class Meta:
        db_table = 'administrateurs'  # Custom table name for the model

class Medecin(User):
    # Add additional fields specific to Medecins if needed
    pass

    class Meta:
        db_table = 'medecins'  # Custom table name for the model

class Patient(User):
    nss = models.CharField(max_length=15, unique=True)
    medecin_traitant = models.ForeignKey(
        Medecin,
        on_delete=models.SET_NULL,  # If the referenced doctor is deleted, the field is set to NULL.
        null=True,  # Makes this field optional by allowing it to be null
        blank=True,  # Makes this field optional by allowing it to be blank
        related_name="patients"  # Allows reverse access from a Medecin instance to their patients
    )
    mutuelle = models.CharField(max_length=15, blank=True)
    dossier_patient = models.OneToOneField(
        'DossierPatient',  # Reference to the DossierPatient model
        on_delete=models.CASCADE,  # If the patient is deleted, delete the dossier as well.
        related_name='patient',  # Allows reverse access from DossierPatient to Patient
    )

    class Meta:
        db_table = 'patients'  # Custom table name for the model


class Infirmier(User):
    # Add additional fields specific to Infirmiers if needed
    pass

    class Meta:
        db_table = 'infirmiers'  # Custom table name for the model

class Laborantin(User):
    # Add additional fields specific to Laborantins if needed
    pass

    class Meta:
        db_table = 'laboronatins'  # Custom table name for the model

class Radiologue(User):
    # Add additional fields specific to Radiologues if needed
    pass

    class Meta:
        db_table = 'radiologues'  # Custom table name for the model


class DossierPatient(models.Model):
    etat = models.CharField(max_length=20,blank = True , null= True)
    antécédents = models.TextField(blank = True , null= True)
    
    class Meta:
        db_table = 'dossiers_patients'  # Custom table name for the model


class Consultation(models.Model):
    BILAN_CHOICES = [
        ('bilan biologique', 'Bilan Biologique'),
        ('bilan radiologique', 'Bilan Radiologique'),
        ('bilan biologique et radiologique', 'Bilan Biologique et Radiologique'),
        ('Aucun bilan', 'Aucun Bilan'),
    ]

    dossier_patient = models.ForeignKey(DossierPatient, on_delete=models.CASCADE)
    date_consultation = models.DateTimeField()
    bilan_prescrit = models.CharField(max_length=50, choices=BILAN_CHOICES, default='Aucun bilan')
    resume = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Consultation for {self.dossier_patient.patient.nom} {self.dossier_patient.patient.prenom}"

    class Meta:
        db_table = 'consultation'
        