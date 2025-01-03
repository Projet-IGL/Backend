from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField

class User(AbstractUser):
    """
    Modèle personnalisé d'utilisateur.

    Attributes:
        role (str): Le rôle de l'utilisateur parmi les choix disponibles (administrateur, patient, etc.).
        date_naissance (date): Date de naissance de l'utilisateur (peut être vide pour les super-utilisateurs).
        adresse (str): Adresse de l'utilisateur.
        numero_telephone (str): Numéro de téléphone de l'utilisateur.
    """
    ROLE_CHOICES = (
        ('Administrateur', 'administrateur'),
        ('Patient', 'patient'),
        ('Medecin', 'medecin'),
        ('Infirmier', 'infirmier'),
        ('Laborantin', 'laborantin'),
        ('Radiologue', 'radiologue'),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    date_naissance = models.DateField(blank=True, null=True)
    adresse = models.CharField(max_length=255)
    numero_telephone = models.CharField(max_length=15)

    class Meta:
        db_table = 'users'


class Administrateur(User):
    """
    Modèle spécifique pour les administrateurs.
    Hérite de la classe User.
    """
    class Meta:
        db_table = 'administrateurs'


class Medecin(User):
    """
    Modèle spécifique pour les médecins.
    Hérite de la classe User.
    """
    class Meta:
        db_table = 'medecins'


class Patient(User):
    """
    Modèle spécifique pour les patients.

    Attributes:
        nss (str): Numéro de sécurité sociale unique.
        medecin_traitant (ForeignKey): Médecin traitant associé au patient.
        mutuelle (str): Nom de la mutuelle du patient (facultatif).
        dossier_patient (OneToOneField): Référence au dossier du patient.
        telephone_urgence (str): Numéro de téléphone d'urgence (facultatif).
    """
    nss = models.CharField(max_length=15, unique=True)
    medecin_traitant = models.ForeignKey(
        Medecin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients"
    )
    mutuelle = models.CharField(max_length=15, blank=True)
    dossier_patient = models.OneToOneField(
        'DossierPatient',
        on_delete=models.CASCADE,
        related_name='patient',
        null=True,
        blank=True,
    )
    telephone_urgence = models.CharField(max_length=15, unique=True, null=True, blank=True)

    class Meta:
        db_table = 'patients'


class Infirmier(User):
    """
    Modèle spécifique pour les infirmiers.
    Hérite de la classe User.
    """
    class Meta:
        db_table = 'infirmiers'


class Laborantin(User):
    """
    Modèle spécifique pour les laborantins.
    Hérite de la classe User.
    """
    class Meta:
        db_table = 'laboronatins'


class Radiologue(User):
    """
    Modèle spécifique pour les radiologues.
    Hérite de la classe User.
    """
    class Meta:
        db_table = 'radiologues'


class DossierPatient(models.Model):
    """
    Modèle représentant le dossier médical d'un patient.

    Attributes:
        etat (str): État général du dossier (facultatif).
        antécédents (TextField): Antécédents médicaux du patient (facultatif).
    """
    etat = models.CharField(max_length=20, blank=True, null=True)
    antécédents = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'dossiers_patients'


class Consultation(models.Model):
    """
    Modèle représentant une consultation médicale.

    Attributes:
        dossier_patient (ForeignKey): Référence au dossier du patient.
        numero_consultation (int): Numéro unique de la consultation.
        date_consultation (datetime): Date de la consultation.
        bilan_prescrit (MultiSelectField): Bilan prescrit lors de la consultation.
        resume (TextField): Résumé de la consultation.
        medecinConsultant (ForeignKey): Médecin ayant réalisé la consultation.
    """
    BILAN_CHOICES = [
        ('bilan biologique', 'Bilan Biologique'),
        ('bilan radiologique', 'Bilan Radiologique'),
        ('Aucun bilan', 'Aucun Bilan'),
    ]

    dossier_patient = models.ForeignKey(DossierPatient, on_delete=models.CASCADE)
    numero_consultation = models.IntegerField(default=0)
    date_consultation = models.DateTimeField()
    bilan_prescrit = MultiSelectField(choices=BILAN_CHOICES, blank=True)
    resume = models.TextField(blank=True, null=True)
    medecinConsultant = models.ForeignKey(Medecin, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Consultation for {self.dossier_patient.patient.nom} {self.dossier_patient.patient.prenom}"

    class Meta:
        db_table = 'consultation'


class Soins(models.Model):
    """
    Modèle représentant les soins administrés à un patient.

    Attributes:
        dossier_patient (ForeignKey): Référence au dossier du patient.
        infirmier (ForeignKey): Référence à l'infirmier ayant administré les soins.
        observation_etat_patient (TextField): Observations sur l'état du patient.
        medicament_pris (bool): Indique si un médicament a été pris.
        description_soins (TextField): Description des soins administrés.
        date_soin (datetime): Date des soins.
    """
    dossier_patient = models.ForeignKey(DossierPatient, on_delete=models.CASCADE)
    infirmier = models.ForeignKey(
        Infirmier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients"
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
    """
    Modèle représentant un médicament prescrit.

    Attributes:
        ordonnance (ForeignKey): Référence à l'ordonnance associée.
        nom (str): Nom du médicament.
        dose (str): Dosage du médicament.
        duree (str): Durée pendant laquelle le médicament doit être pris.
    """
    ordonnance = models.ForeignKey(
        'Ordonnance',
        on_delete=models.CASCADE,
        related_name='medicaments'
    )
    nom = models.CharField(max_length=255)
    dose = models.CharField(max_length=255)
    duree = models.CharField(max_length=255, db_column='durée')

    def __str__(self):
        return f"{self.nom} ({self.dose}) for {self.duree}"

    class Meta:
        db_table = 'medicament'


class Ordonnance(models.Model):
    """
    Modèle représentant une ordonnance médicale.

    Attributes:
        dossier_patient (ForeignKey): Référence au dossier du patient.
        consultation (ForeignKey): Référence à la consultation associée.
    """
    dossier_patient = models.ForeignKey(DossierPatient, on_delete=models.CASCADE, db_column='dossier_patient_id')
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, db_column='consultation_id')

    def __str__(self):
        return f"Ordonnance for {self.dossier_patient.patient.nom} {self.dossier_patient.patient.prenom}"

    class Meta:
        db_table = 'ordonnance'


class BilanBiologique(models.Model):
    """
    Modèle représentant un bilan biologique.

    Attributes:
        dossier_patient (ForeignKey): Référence au dossier du patient.
        laborantin (ForeignKey): Référence au laborantin ayant effectué le bilan.
        date_examen (datetime): Date de l'examen.
        graphe (ImageField): Graphe associé au bilan (facultatif).
        glycemie (DecimalField): Glycémie mesurée (facultatif).
        pression_arterielle (str): Pression artérielle mesurée (facultatif).
        cholesterol (DecimalField): Cholestérol mesuré (facultatif).
        numero_consultation (int): Numéro de consultation associé.
    """
    dossier_patient = models.ForeignKey(DossierPatient, on_delete=models.CASCADE)
    laborantin = models.ForeignKey(
        Laborantin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients"
    )
    date_examen = models.DateTimeField()
    graphe = models.ImageField(null=True, blank=True)
    glycemie = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pression_arterielle = models.CharField(max_length=20, null=True, blank=True)
    cholesterol = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    numero_consultation = models.IntegerField(default=1)

    def __str__(self):
        return f"Bilan biologique for {self.dossier_patient.patient.nom} {self.dossier_patient.patient.prenom}"

    class Meta:
        db_table = 'Bilan_Biologique'


class BilanRadiologique(models.Model):
    """
    Modèle représentant un bilan radiologique.

    Attributes:
        dossier_patient (ForeignKey): Référence au dossier du patient.
        radiologue (ForeignKey): Référence au radiologue ayant effectué le bilan.
        compte_rendu (TextField): Compte rendu de l'examen.
        images (ImageField): Images associées au bilan (facultatif).
        date_examen (datetime): Date de l'examen.
        numero_consultation (int): Numéro de consultation associé.
    """
    dossier_patient = models.ForeignKey(DossierPatient, on_delete=models.CASCADE)
    radiologue = models.ForeignKey(
        Radiologue,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients"
    )
    compte_rendu = models.TextField()
    images = models.ImageField(null=True, blank=True)
    date_examen = models.DateTimeField()
    numero_consultation = models.IntegerField(default=1)

    def __str__(self):
        return f"Bilan radiologique for {self.dossier_patient.patient.nom} {self.dossier_patient.patient.prenom}"

    class Meta:
        db_table = 'Bilan_Radiologique'
