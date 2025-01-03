"""
Tests unitaires pour les vues de l'application backendapp.

Ce fichier contient les tests associés aux vues du backendapp. Les tests visent à vérifier le bon fonctionnement
des API créées pour interagir avec les modèles et les données de l'application.

Ces tests sont utilisés pour s'assurer que les vues du backend fonctionnent comme prévu et renvoient
les bonnes informations ou des erreurs appropriées.
"""

from django.test import TestCase
from backendapp.models import Medecin, Patient, Ordonnance, DossierPatient, Consultation
from datetime import datetime
from django.utils import timezone


class OrdonnanceModelTestCase(TestCase):
    """
    Test des fonctionnalités liées au modèle Ordonnance.
    
    Cette classe regroupe les tests pour vérifier :
    - La création d'une ordonnance valide.
    - La bonne association d'un dossier patient avec un patient et une consultation.
    """

    def setUp(self):
        """
        Préparation des données de test avant chaque test.
        
        Cette méthode crée un médecin, un patient, un dossier patient et une consultation
        nécessaires pour les tests de l'ordonnance.
        """
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
        """
        Tester la création d'une ordonnance valide.
        
        Ce test vérifie que l'ordonnance est correctement créée et que 
        la relation entre l'ordonnance, le dossier patient et la consultation est correcte.
        """
        ordonnance = Ordonnance.objects.create(
            dossier_patient=self.dossier_patient,
            consultation=self.consultation
        )
        
        # Vérification de la relation entre l'ordonnance et le dossier patient et la consultation
        self.assertEqual(ordonnance.dossier_patient, self.dossier_patient)
        self.assertEqual(ordonnance.consultation, self.consultation)

    def test_dossier_patient_association(self):
        """
        Vérifier que le dossier patient est bien associé à son patient.
        
        Ce test assure que la relation entre le patient et son dossier patient est correctement établie.
        """
        self.assertEqual(self.dossier_patient.patient, self.patient)
