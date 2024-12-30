from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from backendapp.models import Medecin, Patient, Ordonnance, DossierPatient, Consultation
from datetime import datetime
from django.utils import timezone


class OrdonnanceModelTestCase(TestCase):

    def setUp(self):
        # Création d'un médecin 
        self.medecin = Medecin.objects.create_user(
            username='medecin123456789', 
            first_name='Ahmad',  
            last_name='Khatib',  
            email='ahmad.khatib@gmail.com',
            password='password123',
            role='Medecin',
            adresse='Alger',  
            numero_telephone='0723456789',
            date_naissance=datetime(1990, 7, 20)
        )

        # Création d'un dossier patient pour le patient
        self.dossier_patient = DossierPatient.objects.create(
            etat='actif',
            antécédents='aucun'
        )

        # Création d'un patient
        self.patient = Patient.objects.create_user(
            username='patient123456789',
            first_name='Mahmoud',  
            last_name='Sharqawi', 
            email='mahmoud.sharqawi@example.com',
            password='password123',
            role='Patient',
            adresse='Oran', 
            numero_telephone='0612345678',
            date_naissance=datetime(2004, 11, 20),

            nss='12345678912345',
            telephone_urgence='061255678',
            mutuelle='mutuelle',
            medecin_traitant=self.medecin,
            dossier_patient=self.dossier_patient
        )

        # Création d'une consultation
        self.consultation = Consultation.objects.create(
            dossier_patient=self.dossier_patient,
            numero_consultation=1,
            date_consultation=timezone.now(),
            bilan_prescrit=['bilan biologique'],
            resume='Consultation initiale'
        )

    def test_ordonnance_creation(self):
        # Test de création d'une ordonnance valide
        ordonnance = Ordonnance.objects.create(
            dossier_patient=self.dossier_patient,
            consultation=self.consultation
        )
        
        # Vérification de la relation entre l'ordonnance et le dossier patient er la consultation
        self.assertEqual(ordonnance.dossier_patient, self.dossier_patient)
        self.assertEqual(ordonnance.consultation, self.consultation)

    def test_dossier_patient_association(self):
        # Vérifier que le dossier patient est bien associé à son patient
        self.assertEqual(self.dossier_patient.patient, self.patient)