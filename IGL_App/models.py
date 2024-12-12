from django.db import models
from django.contrib.auth.hashers import make_password
class Staff(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    adresse = models.CharField(max_length=255)
    date_naissance = models.DateField()
    mot_de_passe = models.CharField(max_length=255)
    role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    class Meta:
        managed = True
        db_table = 'Staff'

class Patient(models.Model):
    nss = models.CharField(max_length=15, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    mutuelle = models.CharField(max_length=100)
    mot_de_passe = models.CharField(max_length=255, default=make_password('password'))
    medecin_traitant = models.ForeignKey(Staff, on_delete=models.CASCADE)
    personne_a_contacter = models.CharField(max_length=100)
    telephone_contact = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    class Meta:
        
        db_table = 'Patient'

class DossierPatient(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    code_qr = models.CharField(max_length=255)
    etat = models.CharField(max_length=20)
    antécédents = models.TextField()

    def __str__(self):
        return f"Dossier for {self.patient.nom} {self.patient.prenom}"
    class Meta:
        db_table = 'Dossier_patient'
        

class Consultation(models.Model):
    dossier_patient = models.ForeignKey(DossierPatient, on_delete=models.CASCADE)
    date_consultation = models.DateTimeField()
    bilan_prescrit = models.TextField(blank=True, null=True)
    resume = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Consultation for {self.dossier_patient.patient.nom} {self.dossier_patient.patient.prenom}"
    class Meta:
        db_table = 'Consultation'
    

class Soins(models.Model):
    dossier_patient = models.ForeignKey(DossierPatient, on_delete=models.CASCADE)
    infirmier = models.ForeignKey('Staff', on_delete=models.CASCADE, limit_choices_to={'role': 'infirmier'})
    observation_etat_patient = models.TextField()
    medicament_pris = models.BooleanField(default=False)
    description_soins = models.TextField()
    date_soin = models.DateTimeField()

    def __str__(self):
        return f"Soins for {self.dossier_patient.patient.nom} {self.dossier_patient.patient.prenom}"
    class Meta:
        db_table = 'Soins'

class Ordonnance(models.Model):
    dossier_patient = models.ForeignKey(DossierPatient, on_delete=models.CASCADE)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    medicament = models.TextField()
    quantite = models.IntegerField()
    duree = models.CharField(max_length=255)

    def __str__(self):
        return f"Ordonnance for {self.dossier_patient.patient.nom} {self.dossier_patient.patient.prenom}"

class BilanBiologique(models.Model):
    dossier_patient = models.ForeignKey(DossierPatient, on_delete=models.CASCADE)
    laborantin = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, related_name="bilans_biologiques")
    resultat_analyse = models.TextField()
    resultat_examen_imagerie = models.TextField()
    date_examen = models.DateTimeField()
    graphe = models.BinaryField()

    def __str__(self):
        return f"Bilan biologique for {self.dossier_patient.patient.nom} {self.dossier_patient.patient.prenom}"

class BilanRadiologique(models.Model):
    dossier_patient = models.ForeignKey(DossierPatient, on_delete=models.CASCADE)
    radiologue = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, related_name="bilans_radiologiques")
    compte_rendu = models.TextField()
    images = models.BinaryField()
    date_examen = models.DateTimeField()

    def __str__(self):
        return f"Bilan radiologique for {self.dossier_patient.patient.nom} {self.dossier_patient.patient.prenom}"
