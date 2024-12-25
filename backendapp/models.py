from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField

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
        ('Aucun bilan', 'Aucun Bilan'),
    ]
    #author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL)  # Référence à Author ou NULL
    dossier_patient = models.ForeignKey(DossierPatient, on_delete=models.CASCADE)
    numero_consultation = models.IntegerField(default=0)
    date_consultation = models.DateTimeField()
    bilan_prescrit = MultiSelectField(choices=BILAN_CHOICES, blank=True)
    resume = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Consultation for {self.dossier_patient.patient.nom} {self.dossier_patient.patient.prenom}"

    class Meta:
        db_table = 'consultation'
        
class Soins(models.Model):
    dossier_patient = models.ForeignKey(DossierPatient, on_delete=models.CASCADE)
    infirmier = models.ForeignKey(
        Infirmier,
        on_delete=models.SET_NULL,  # If the referenced doctor is deleted, the field is set to NULL.
        null=True,  # Makes this field optional by allowing it to be null
        blank=True,  # Makes this field optional by allowing it to be blank
        related_name="patients"  # Allows reverse access from a Medecin instance to their patients
    )
    
    observation_etat_patient = models.TextField()
    medicament_pris = models.BooleanField(default=False)
    description_soins = models.TextField()
    date_soin = models.DateTimeField()

    def __str__(self):
        return f"Soins for {self.dossier_patient.patient.nom} {self.dossier_patient.patient.prenom}"
    class Meta:
        db_table = 'soins'        

class Medicament(models.Model):
    ordonnance = models.ForeignKey(
        'Ordonnance', 
        on_delete=models.CASCADE, 
        related_name='medicaments'
    )  # ForeignKey to link medications to an ordonnance
    nom = models.CharField(max_length=255)  # Name of the medication
    dose = models.CharField(max_length=255)  # Dosage of the medication
    duree = models.CharField(max_length=255, db_column='durée')  # Duration for which the medication is prescribed

    def __str__(self):
        return f"{self.nom} ({self.dose}) for {self.duree}"

    class Meta:
        db_table = 'medicament'


class Ordonnance(models.Model):
    dossier_patient = models.ForeignKey(DossierPatient, on_delete=models.CASCADE, db_column='dossier_patient_id')
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, db_column='consultation_id')

    def __str__(self):
        return f"Ordonnance for {self.dossier_patient.patient.nom} {self.dossier_patient.patient.prenom}"

    class Meta:
        db_table = 'ordonnance'


class BilanBiologique(models.Model):
    dossier_patient = models.ForeignKey(DossierPatient, on_delete=models.CASCADE)
    laborantin = models.ForeignKey(
        Laborantin,
        on_delete=models.SET_NULL,  # If the referenced doctor is deleted, the field is set to NULL.
        null=True,  # Makes this field optional by allowing it to be null
        blank=True,  # Makes this field optional by allowing it to be blank
        related_name="patients"  # Allows reverse access from a Medecin instance to their patients
    )
    resultat_analyse = models.TextField()
    resultat_examen_imagerie = models.TextField()
    date_examen = models.DateTimeField()
    graphe = models.BinaryField(null=True, blank=True)
    glycemie = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pression_arterielle = models.CharField(max_length=20, null=True, blank=True)
    cholesterol = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)


    def __str__(self):
        return f"Bilan biologique for {self.dossier_patient.patient.nom} {self.dossier_patient.patient.prenom}"
    class Meta:
        db_table = 'Bilan_Biologique'

class BilanRadiologique(models.Model):
    dossier_patient = models.ForeignKey(DossierPatient, on_delete=models.CASCADE)
    radiologue = models.ForeignKey(
        Radiologue,
        on_delete=models.SET_NULL,  # If the referenced doctor is deleted, the field is set to NULL.
        null=True,  # Makes this field optional by allowing it to be null
        blank=True,  # Makes this field optional by allowing it to be blank
        related_name="patients"  # Allows reverse access from a Medecin instance to their patients
    )
    compte_rendu = models.TextField()
    images = models.ImageField(null=True, blank=True)
    date_examen = models.DateTimeField()

    def __str__(self):
        return f"Bilan radiologique for {self.dossier_patient.patient.nom} {self.dossier_patient.patient.prenom}"
    class Meta: 
        db_table = 'Bilan_Radiologique'