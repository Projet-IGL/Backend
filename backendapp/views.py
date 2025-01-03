"""
Vues de l'application backendapp.

Ce fichier contient les vues de l'application backendapp, qui sont responsables
de la gestion des différentes requêtes HTTP pour récupérer les informations liées
aux patients, consultations, bilans radiologiques et ordonnances.

Les vues incluent la récupération des bilans radiologiques, des ordonnances et des informations
relatives à la consultation, ainsi que la validation des informations du patient.

Les réponses sont formatées en JSON, et les erreurs sont gérées de manière appropriée
en renvoyant des codes d'état HTTP pertinents.
"""

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework import status
from .serializers import (
    MedecinSerializer, 
    PatientSerializer, 
    LaborantinSerializer, 
    InfirmierSerializer, 
    RadiologueSerializer,
    AdministrateurSerializer,
    DossierPatientSerializer,
    BilanRadiologiqueSerializer,
    ConsultationSerializer
)
from .models import User, Medecin, Patient, Infirmier, Laborantin, Radiologue, DossierPatient , Consultation , Soins , Ordonnance , Medicament ,BilanBiologique , BilanRadiologique , Administrateur
from django.shortcuts import get_object_or_404 
from django.db import transaction
from rest_framework.views import APIView
from django.utils.dateparse import parse_date
from rest_framework.decorators import api_view
from datetime import datetime
from django.utils.timezone import make_aware 

@api_view(['POST'])
def login_view(request):
    """
    Point d'entrée pour l'authentification de l'utilisateur et la création d'un token d'authentification.

    Cette fonction gère la connexion d'un utilisateur en vérifiant son nom d'utilisateur et son mot de passe.
    Si l'utilisateur est authentifié avec succès, elle crée un token d'authentification, et renvoie les données de l'utilisateur,
    y compris son rôle spécifique et les données associées (par exemple, les informations sur le patient ou le médecin).

    Paramètres:
        request (Request): Requête HTTP contenant les données d'identification (nom d'utilisateur et mot de passe).

    Retour:
        Response: Réponse HTTP contenant le token d'authentification et les informations de l'utilisateur si la connexion est réussie.
                Sinon, un message d'erreur indiquant un échec de l'authentification.
    """
    
    # Récupération du nom d'utilisateur et du mot de passe depuis la requête
    username = request.data.get('username')
    password = request.data.get('password')

    # Authentification de l'utilisateur
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)  # Connexion de l'utilisateur (définir la session)

        # Récupérer ou créer un token d'authentification
        token, created = Token.objects.get_or_create(user=user)

        # les données de la réponse
        response_data = {
            'token': token.key,
            'username': user.username,
            'role': user.role,
        }

        # Déterminer le rôle spécifique de l'utilisateur et récupérer les données associées
        if user.role == 'Patient':
            try:
                patient = Patient.objects.get(pk=user.pk)
                response_data['data'] = PatientSerializer(patient).data
            except Patient.DoesNotExist:
                return Response({'message': 'Les données du patient n''ont pas été trouvées'}, status=status.HTTP_400_BAD_REQUEST)

        elif user.role == 'Medecin':
            try:
                medecin = Medecin.objects.get(pk=user.pk)
                response_data['data'] = MedecinSerializer(medecin).data
            except Medecin.DoesNotExist:
                return Response({'message': 'Les données du médecin n''ont pas été trouvées'}, status=status.HTTP_400_BAD_REQUEST)

        elif user.role == 'Laborantin':
            try:
                laborantin = Laborantin.objects.get(pk=user.pk)
                response_data['data'] = LaborantinSerializer(laborantin).data
            except Laborantin.DoesNotExist:
                return Response({'message': 'Les données du laborantin n''ont pas été trouvées'}, status=status.HTTP_400_BAD_REQUEST)

        elif user.role == 'Infirmier':
            try:
                infirmier = Infirmier.objects.get(pk=user.pk)
                response_data['data'] = InfirmierSerializer(infirmier).data
            except Infirmier.DoesNotExist:
                return Response({'message': 'Les données de l''infirmier n''ont pas été trouvées'}, status=status.HTTP_400_BAD_REQUEST)

        elif user.role == 'Radiologue':
            try:
                radiologue = Radiologue.objects.get(pk=user.pk)
                response_data['data'] = RadiologueSerializer(radiologue).data
            except Radiologue.DoesNotExist:
                return Response({'message': 'Les données du radiologue n''ont pas été trouvées'}, status=status.HTTP_400_BAD_REQUEST)
            
        elif user.role == 'Administrateur':
            try:
                administrateur = Administrateur.objects.get(pk=user.pk)
                response_data['data'] = AdministrateurSerializer(administrateur).data
            except Administrateur.DoesNotExist:
                return Response({'message': 'Les données de l''administrateur n''ont pas été trouvées'}, status=status.HTTP_400_BAD_REQUEST)    

        # Retourner la réponse finale
        return Response(response_data, status=status.HTTP_200_OK)

    else:
        return Response({'message': 'Nom d''utilisateur ou mot de passe invalide'}, status=status.HTTP_401_UNAUTHORIZED)

    
    
@api_view(['POST'])
def rechercher_dpi_par_nss(request):
    """
    Recherche le dossier patient à partir du numéro de sécurité sociale (NSS).

    Cette fonction permet de récupérer les informations du patient en fonction de son NSS (Numéro de Sécurité Sociale),
    et retourne les données du patient ainsi que son dossier médical.

    Paramètres:
        request (Request): La requête HTTP contenant le numéro de sécurité sociale (NSS) du patient.

    Retour:
        Response: La réponse HTTP contenant les données du patient et de son dossier si le NSS est valide, 
                  ou un message d'erreur si le NSS est manquant ou que le patient n'est pas trouvé.
    """
    
    nss = request.data.get('nss')  # Récupérer le NSS depuis les paramètres de la requête

    if not nss:
        return Response({'message': 'Le paramètre NSS est requis'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        patient = Patient.objects.get(nss=nss)  # Trouver le patient par NSS
        dossier_patient = patient.dossier_patient  # Référence directe au DossierPatient
    except Patient.DoesNotExist:
        return Response({'message': 'Patient non trouvé'}, status=status.HTTP_404_NOT_FOUND)

    # Sérialiser l'instance du patient et du dossier médical
    patient_serializer = PatientSerializer(patient)  # Cela récupère également les données du DPI (Dossier Patient Informatique)

    # Préparer les données de réponse avec les informations du patient et du dossier
    response_data = {
        'patient_data': patient_serializer.data,
    }

    # Retourner les données combinées dans la réponse
    return Response(response_data, status=status.HTTP_200_OK)


         
@api_view(['POST'])
def creer_consultation(request):
    """
    Crée une nouvelle consultation pour un patient donné.

    Cette fonction permet de créer une consultation pour un patient à partir de son numéro de sécurité sociale (NSS),
    de la date et heure de la consultation, du bilan prescrit, du résumé et du médecin consultant.
    Elle associe également la consultation au patient et au médecin.

    Paramètres:
        request (Request): La requête HTTP contenant les informations nécessaires à la création de la consultation.

    Retour:
        Response: La réponse HTTP contenant un message de succès avec l'ID de la consultation créée ou un message d'erreur.
    """
    
    nss = request.data.get('dpi')  # Récupérer le NSS (DPI) depuis les paramètres de la requête
    
    date_consultation = request.data.get('dateTime')  # Récupérer la date et l'heure de la consultation
    bilan_prescrit = request.data.get('bilan')  # Récupérer le bilan prescrit
    resume = request.data.get('resume')  # Récupérer le résumé de la consultation
    medecin_id = request.data.get('medecinConsultant')  # Récupérer l'ID du médecin consultant

    if not medecin_id:
        return Response({'message': 'Le Médecin Consultant est requis'}, status=status.HTTP_400_BAD_REQUEST)

    # Vérifier si le NSS est fourni
    if not nss:
        return Response({'message': 'Le NSS est requis'}, status=status.HTTP_400_BAD_REQUEST)

    # Trouver le patient correspondant et son dossier
    try:
        patient = Patient.objects.get(nss=nss)
        dossier_patient = patient.dossier_patient  # Récupérer le DossierPatient associé
        if not dossier_patient:
            return Response({'message': 'Aucun Dossier Patient trouvé pour ce patient.'}, status=status.HTTP_404_NOT_FOUND)
    except Patient.DoesNotExist:
        return Response({'message': 'Patient avec le NSS donné non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

    # Trouver la dernière consultation et déterminer le numéro de consultation suivant
    last_consultation = Consultation.objects.filter(dossier_patient=dossier_patient).order_by('-numero_consultation').first()
    if last_consultation:
        numero_consultation = last_consultation.numero_consultation + 1
    else:
        numero_consultation = 1  # Première consultation pour ce patient
    
    # Trouver le médecin consultant
    try:
        medecin_consultant = Medecin.objects.get(id=medecin_id)
    except Medecin.DoesNotExist:
        return Response({'message': 'Médecin Consultant non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

    # Créer l'objet Consultation
    consultation = Consultation.objects.create(
        dossier_patient=dossier_patient,
        date_consultation=date_consultation,
        numero_consultation=numero_consultation,
        bilan_prescrit=bilan_prescrit,
        resume=resume,
        medecinConsultant=medecin_consultant,  # Associer le médecin consultant
    )

    # Retourner la réponse de succès avec l'ID de la consultation créée
    return Response({'message': 'Consultation créée avec succès', 'consultation_id': consultation.id}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def Faire_soin(request):
    """
    Crée un soin pour un patient donné.

    Cette fonction permet de créer un soin pour un patient en utilisant son numéro de sécurité sociale (NSS),
    les observations sur l'état du patient, les médicaments administrés, la description du soin,
    ainsi que l'infirmier en charge (optionnel).

    Paramètres:
        request (Request): La requête HTTP contenant les informations nécessaires à la création du soin.

    Retour:
        Response: La réponse HTTP contenant un message de succès ou un message d'erreur.
    """
    
    nss = request.data.get('nss')  # Récupérer le NSS depuis les données de la requête
    infirmier_id = request.data.get('infirmierId')  # Récupérer l'ID de l'infirmier (optionnel, lié à l'utilisateur connecté)
    observation_etat_patient = request.data.get('observations')  # Récupérer les observations sur l'état du patient
    medicament_pris = request.data.get('medicamentAdministre')  # Récupérer les médicaments administrés
    description_soins = request.data.get('details')  # Récupérer la description du soin
    date_soin = request.data.get('time')  # Récupérer la date du soin

    # Valider et récupérer le Patient et son DossierPatient
    try:
        patient = Patient.objects.get(nss=nss)
        dossier_patient = patient.dossier_patient  # Accéder au DossierPatient lié
    except Patient.DoesNotExist:
        return Response({'message': 'Patient avec le NSS fourni non trouvé'}, status=status.HTTP_404_NOT_FOUND)
    except DossierPatient.DoesNotExist:
        return Response({'message': 'Dossier Patient pour le NSS fourni non trouvé'}, status=status.HTTP_404_NOT_FOUND)

    # Valider l'Infirmier (optionnel, car peut être null)
    infirmier = None
    if infirmier_id:
        try:
            infirmier = Infirmier.objects.get(id=infirmier_id)
        except Infirmier.DoesNotExist:
            return Response({'message': 'Infirmier non trouvé'}, status=status.HTTP_404_NOT_FOUND)

    # Créer l'objet Soins
    soins = Soins.objects.create(
        dossier_patient=dossier_patient,
        infirmier=infirmier,
        observation_etat_patient=observation_etat_patient,
        medicament_pris=medicament_pris,
        description_soins=description_soins,
        date_soin=date_soin
    )

    # Retourner la réponse de succès
    return Response({'message': 'Soin créé avec succès'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def creer_ordonnance(request):
    """
    Crée une ordonnance pour un patient donné à partir de la consultation spécifiée.

    Cette fonction crée une ordonnance pour un patient, associée à une consultation spécifique et à une liste de médicaments.
    Elle attend un NSS pour identifier le patient, une date de consultation pour associer la consultation, 
    et une liste de médicaments à prescrire. Si un champ requis est manquant ou incorrect, un message d'erreur est renvoyé.

    Paramètres:
        request (Request): La requête HTTP contenant les données nécessaires pour créer l'ordonnance.

    Retour:
        Response: La réponse HTTP avec un message de succès ou d'erreur.
    """
    try:
        # Récupérer les données nécessaires de la requête
        nss = request.data.get('nss', '').strip()
        date_consultation = request.data.get('consultationDate', '').strip()
        medicaments_data = request.data.get('medications', [])  # Liste des médicaments attendus

        # Vérifier la présence des données nécessaires
        if not nss or not date_consultation or not medicaments_data:
            return Response(
                {'error': 'NSS, date_consultation, et médicaments sont requis.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Valider et récupérer le patient, le dossier et la consultation
        patient = get_object_or_404(Patient, nss=nss)
        dossier_patient = get_object_or_404(DossierPatient, patient=patient)
        consultation = get_object_or_404(
            Consultation,
            dossier_patient=dossier_patient,
            date_consultation=date_consultation
        )

        # Création de l'ordonnance dans une transaction atomique
        with transaction.atomic():
            # Créer l'ordonnance
            ordonnance = Ordonnance.objects.create(
                dossier_patient=dossier_patient,
                consultation=consultation
            )

            # Créer les médicaments associés à l'ordonnance
            for medicament_data in medicaments_data:
                nom = medicament_data.get('medicament')
                dose = medicament_data.get('dose')
                duree = medicament_data.get('duree')

                if not (nom and dose and duree):
                    continue  # Passer les entrées incomplètes

                Medicament.objects.create(
                    ordonnance=ordonnance,
                    nom=nom,
                    dose=dose,
                    duree=duree
                )

        # Retourner un message de succès
        return Response(
            {'message': 'Ordonnance créée avec succès.'},
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        print("Error:", e)
        # En cas d'erreur, retourner un message d'erreur
        return Response(
            {'error': 'Une erreur est survenue lors de la création de l\'ordonnance.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def creer_bilan_biologique(request):
    """
    Crée un bilan biologique pour un patient à partir des données fournies.

    Cette fonction permet de créer un bilan biologique pour un patient donné. Elle attend des informations telles que le NSS du patient,
    l'ID du laborantin qui effectue l'examen, la date de l'examen, ainsi que des résultats de tests médicaux comme la glycémie, la pression artérielle,
    le cholestérol et un graphique (image). Elle vérifie également si un bilan biologique existe déjà pour ce patient et ce numéro de consultation.

    Paramètres:
        request (Request): La requête HTTP contenant les données nécessaires pour créer le bilan biologique.

    Retour:
        Response: La réponse HTTP avec un message de succès ou d'erreur.
    """
    try:
        # Extraire les données de la requête
        nss = request.data.get('nss')
        laborantin_id = request.data.get('laborantinId')
        print('laborantin ID', laborantin_id)
        date_examen_str = request.data.get('time')
        glycemie = request.data.get('glycemie')
        pression_arterielle = request.data.get('pression')
        cholesterol = request.data.get('cholesterol')
        graphe = request.FILES.get('imageFile')
        numero_consultation = request.data.get('numcons')

        # Convertir la date de l'examen en datetime et la rendre compatible avec le fuseau horaire
        if date_examen_str:
            date_examen = make_aware(datetime.strptime(date_examen_str, "%Y-%m-%dT%H:%M"))
        else:
            date_examen = make_aware(datetime.now())

        # Valider et récupérer le laborantin
        try:
            laborantin = Laborantin.objects.get(id=laborantin_id, role='laborantin')
        except Laborantin.DoesNotExist:
            return Response({'message': 'Laborantin non trouvé ou ID invalide.'}, status=status.HTTP_404_NOT_FOUND)

        # Valider et récupérer le patient et le dossier_patient
        try:
            patient = Patient.objects.get(nss=nss)
            dossier_patient = DossierPatient.objects.get(patient=patient)
        except (Patient.DoesNotExist, DossierPatient.DoesNotExist):
            return Response({'message': 'Patient ou Dossier Patient non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier si un BilanBiologique existe déjà pour ce patient et ce numéro de consultation
        existing_bilan = BilanBiologique.objects.filter(dossier_patient=dossier_patient, numero_consultation=numero_consultation).first()
        
        if existing_bilan:
            return Response({'message': 'Bilan Biologique existe déjà pour ce patient et cette consultation.'}, status=status.HTTP_400_BAD_REQUEST)

        # Convertir la glycémie et le cholestérol en float si fournis
        glycemie = float(glycemie) if glycemie else None
        cholesterol = float(cholesterol) if cholesterol else None

        # Gérer la conversion de l'image si elle est fournie
        if graphe:
            graphe = graphe  # Django gère déjà la lecture du fichier
        else:
            graphe = None

        # Créer l'instance BilanBiologique
        bilan_biologique = BilanBiologique.objects.create(
            dossier_patient=dossier_patient,
            laborantin=laborantin,
            date_examen=date_examen,
            graphe=graphe,  
            glycemie=glycemie,
            pression_arterielle=pression_arterielle,
            cholesterol=cholesterol,
            numero_consultation=numero_consultation
        )

        # Retourner une réponse de succès
        return Response({'message': 'Bilan Biologique créé avec succès.'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        # En cas d'erreur, retourner un message d'erreur
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def creer_bilan_radiologique(request):
    """
    Crée un bilan radiologique pour un patient à partir des données fournies.

    Cette fonction permet de créer un bilan radiologique pour un patient donné. Elle attend des informations telles que le NSS du patient,
    l'ID du radiologue qui a effectué l'examen, le compte-rendu de l'examen, la date de l'examen, ainsi qu'une image radiographique. 
    Elle vérifie également si un bilan radiologique existe déjà pour ce patient et ce numéro de consultation.

    Paramètres:
        request (Request): La requête HTTP contenant les données nécessaires pour créer le bilan radiologique.

    Retour:
        Response: La réponse HTTP avec un message de succès ou d'erreur.
    """
    try:
        # Extraire les données de la requête
        nss = request.data.get('nss')
        radiologue_id = request.data.get('radiologueId')
        compte_rendu = request.data.get('compteRendu')
        date_examen_str = request.data.get('time')
        numero_consultation = request.data.get('numcons')  # Attente d'un numéro de la part de la requête
        image_file = request.FILES.get('imageRadiographie')
        
        # Valider et récupérer le radiologue
        try:
            radiologue = Radiologue.objects.get(id=radiologue_id)
        except Radiologue.DoesNotExist:
            return Response({'exists': False, 'message': 'Radiologue non trouvé ou ID invalide.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Valider et récupérer le patient et le dossier_patient
        try:
            patient = Patient.objects.get(nss=nss)
            dossier_patient = DossierPatient.objects.get(patient=patient)
        except (Patient.DoesNotExist, DossierPatient.DoesNotExist):
            return Response({'exists': False, 'message': 'Patient ou Dossier Patient non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Vérifier si un Bilan Radiologique existe déjà pour ce patient et ce numéro de consultation
        existing_bilan = BilanRadiologique.objects.filter(dossier_patient=dossier_patient, numero_consultation=numero_consultation).first()
        
        if existing_bilan:
            return Response({'exists': False, 'message': 'Un Bilan Radiologique existe déjà pour ce patient et cette consultation.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Gérer la conversion de l'image si elle est fournie
        if image_file:
            image_data = image_file  # Django gère la lecture du fichier
        else:
            image_data = None

        # Créer l'instance Bilan Radiologique
        bilan_radiologique = BilanRadiologique.objects.create(
            dossier_patient=dossier_patient,
            radiologue=radiologue,
            compte_rendu=compte_rendu,
            images=image_data,
            date_examen=date_examen_str,
            numero_consultation=numero_consultation
        )

        # Sérialiser et retourner les données de la réponse
        serializer = BilanRadiologiqueSerializer(bilan_radiologique)
        return Response(
            {'data': serializer.data, 'exists': True},  # Indique que le bilan a été créé avec succès
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        # En cas d'erreur, retourner un message d'erreur
        return Response({'exists': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['POST'])
def creer_patient(request):
    """
    Crée un nouveau patient à partir des données fournies.

    Cette fonction permet de créer un nouveau patient en extrayant les informations envoyées dans la requête. 
    Elle vérifie si le médecin (medecin_traitant) existe, crée un dossier patient, et associe les informations du patient.
    Elle s'assure également que les données du patient sont valides avant de les enregistrer.

    Paramètres:
        request (Request): La requête HTTP contenant les données du patient à créer.

    Retour:
        Response: La réponse HTTP avec les données du patient créé ou un message d'erreur en cas de problème.
    """
    # Extraire les données du patient de la requête
    data = request.data
    if not data:
        return Response({'error': 'Aucune donnée de patient fournie.'}, status=status.HTTP_400_BAD_REQUEST)

    # Vérifier si le Médecin fourni existe
    try:
        medecin = Medecin.objects.get(username=data.get('medecin'))
    except Medecin.DoesNotExist:
        return Response({'error': 'Médecin non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

    # Créer l'instance DossierPatient
    dossier_patient = DossierPatient.objects.create(
        etat="actif",  # État par défaut du dossier
        antécédents="aucun"  # Antécédents vides par défaut
    )

    # Mapper les champs de données selon l'entrée JSON
    patient_data = {
        'username': data.get('nss'),  # Le nom d'utilisateur est défini comme le NSS
        'first_name': data.get('nom'),
        'last_name': data.get('prenom'),
        'email': data.get('email'),
        'password': data.get('password'),  # Inclure le mot de passe ici
        'role': 'Patient',  # Rôle fixe de Patient
        'date_naissance': data.get('dateDeNaissance'),
        'adresse': data.get('adresse'),
        'numero_telephone': data.get('numtel'),
        'nss': data.get('nss'),
        'telephone_urgence': data.get('numtelurg'),
        'mutuelle': data.get('mutuelle'),
    }

    # Utiliser le serializer PatientSerializer pour valider les données du patient
    serializer = PatientSerializer(data=patient_data)
    if serializer.is_valid():
        # Sauvegarder l'instance Patient sans encore hacher le mot de passe
        patient = serializer.save()
        patient.set_password(patient_data['password'])  # Hacher le mot de passe
        patient.medecin_traitant = medecin  # Associer le Médecin traitant
        patient.dossier_patient = dossier_patient  # Lier le DossierPatient
        patient.save()  # Sauvegarder l'instance Patient complètement préparée

        # Retourner les données du patient créé
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Si le serializer n'est pas valide, retourner l'erreur
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def verifier_patient_par_nss(request):
    """
    Vérifie si un patient existe dans la base de données en fonction de son NSS.

    Cette fonction reçoit un numéro de sécurité sociale (NSS) en paramètre de la requête et vérifie si un patient
    avec ce NSS existe dans la base de données. Si le patient existe, elle retourne ses informations, sinon elle
    retourne une réponse indiquant que le patient n'a pas été trouvé.

    Paramètres:
        request (Request): La requête HTTP contenant le NSS en paramètre de la query.

    Retour:
        Response: La réponse HTTP contenant les données du patient si trouvé, ou un message d'erreur si non trouvé.
    """
    # Extraire le NSS des paramètres de la requête
    nss = request.query_params.get('nss', '').strip()  # Supprimer les espaces ou nouvelles lignes superflus
    if not nss:
        return Response({'message': 'Le NSS est requis'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Vérifier si un patient avec le NSS donné existe
        patient = Patient.objects.get(nss=nss)
        return Response({
            'exists': 'True',  # Le patient existe dans la base de données
            'data': {
                'id': patient.id,
                'nom': patient.first_name,  # Utilisation de first_name et last_name de AbstractUser
                'prenom': patient.last_name,
                'nss': patient.nss,
                'medecin_traitant': patient.medecin_traitant.first_name if patient.medecin_traitant else None
            }
        }, status=status.HTTP_200_OK)
    except Patient.DoesNotExist:
        return Response({'exists': 'False'}, status=status.HTTP_404_NOT_FOUND)  # Le patient n'existe pas dans la base de données

    


@api_view(['POST'])
def get_consultations_by_nss(request):
    """
    Récupère les consultations d'un patient identifié par son NSS.

    Cette fonction prend le NSS d'un patient, vérifie si le patient existe dans la base de données, puis 
    récupère toutes les consultations associées à ce patient et les renvoie sous forme de réponse JSON.

    Paramètres:
        request (Request): La requête HTTP contenant le NSS du patient dans les données de la requête.

    Retour:
        Response: La réponse HTTP contenant les consultations du patient si elles sont trouvées, 
                  ou un message d'erreur si le patient ou ses consultations ne sont pas trouvés.
    """
    # Extraire le NSS des données de la requête
    nss = request.data.get('nss')  # Récupère le NSS depuis les données de la requête

    if not nss:
        return Response({'message': 'Le paramètre NSS est requis.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Trouver le patient et son dossier
        patient = Patient.objects.get(nss=nss)
        dossier_patient = patient.dossier_patient

        if not dossier_patient:
            return Response({'message': 'DossierPatient non trouvé pour ce patient.'}, status=status.HTTP_404_NOT_FOUND)

        # Récupérer les consultations associées au dossier du patient
        consultations = Consultation.objects.filter(dossier_patient=dossier_patient)

        if not consultations.exists():
            return Response({'message': 'Aucune consultation trouvée pour ce patient.'}, status=status.HTTP_404_NOT_FOUND)

        # Sérialiser les consultations
        serializer = ConsultationSerializer(consultations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Patient.DoesNotExist:
        return Response({'message': 'Patient avec le NSS fourni non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'message': f'Une erreur inattendue est survenue : {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def get_soins_by_nss(request):
    """
    Récupère les soins (dossiers de soins) pour un patient identifié par son NSS.

    Cette fonction prend le NSS d'un patient, vérifie si le patient existe dans la base de données, puis 
    récupère tous les soins associés à ce patient et les renvoie sous forme de réponse JSON.

    Paramètres:
        request (Request): La requête HTTP contenant le NSS du patient dans les données de la requête.

    Retour:
        Response: La réponse HTTP contenant les soins du patient si ils sont trouvés, 
                  ou un message d'erreur si le patient ou ses soins ne sont pas trouvés.
    """
    # Extraire le NSS des données de la requête
    nss = request.data.get('nss')  # Récupère le NSS depuis les données de la requête

    if not nss:
        return Response({'message': 'Le paramètre NSS est requis.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Trouver le patient et son dossier
        patient = Patient.objects.get(nss=nss)
        dossier_patient = patient.dossier_patient

        if not dossier_patient:
            return Response({'message': 'DossierPatient non trouvé pour ce patient.'}, status=status.HTTP_404_NOT_FOUND)

        # Récupérer les soins associés au dossier du patient
        soins_records = Soins.objects.filter(dossier_patient=dossier_patient)

        if not soins_records.exists():
            return Response({'message': 'Aucun dossier de soins trouvé pour ce patient.'}, status=status.HTTP_404_NOT_FOUND)

        # Sérialiser les données des soins
        soins_data = []
        for soin in soins_records:
            soins_data.append({
                'infirmier': soin.infirmier.first_name if soin.infirmier else None,
                'observation_etat_patient': soin.observation_etat_patient,
                'medicament_pris': soin.medicament_pris,
                'description_soins': soin.description_soins,
                'date_soin': soin.date_soin.isoformat()  # Sérialiser la date au format ISO
            })

        return Response(soins_data, status=status.HTTP_200_OK)

    except Patient.DoesNotExist:
        return Response({'message': 'Patient avec le NSS fourni non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'message': f'Une erreur inattendue est survenue : {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def check_consultation_existence(request):
    """
    Vérifie l'existence d'une consultation pour un patient, et si un bilan radiologique a été prescrit.

    Cette fonction prend le NSS et le numéro de consultation en entrée, et elle vérifie si :
    - Le patient existe dans la base de données.
    - Le dossier patient existe pour ce patient.
    - La consultation existe avec le numéro donné.
    - Le 'bilan radiologique' est prescrit dans les bilans de la consultation.

    Paramètres:
        request (Request): La requête HTTP contenant les informations de NSS et de numéro de consultation.

    Retour:
        Response: La réponse HTTP indiquant si la consultation existe, si un bilan radiologique est prescrit ou si des erreurs se sont produites.
    """
    try:
        # Extraire les données
        nss = request.data.get('nss')
        numero_consultation = request.data.get('numcons')
        
        # Vérifier les champs obligatoires
        if not nss or not numero_consultation:
            return Response(
                {'exists': False, 'message': 'Le NSS et le numéro de consultation sont requis.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Valider si le patient et le dossier patient existent
        try:
            patient = Patient.objects.get(nss=nss)
            dossier_patient = DossierPatient.objects.get(patient=patient)
        except (Patient.DoesNotExist, DossierPatient.DoesNotExist):
            return Response(
                {'exists': False, 'message': 'Patient ou Dossier Patient non trouvé.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier si la consultation existe
        try:
            consultation = Consultation.objects.get(
                dossier_patient=dossier_patient,
                numero_consultation=numero_consultation
            )
        except Consultation.DoesNotExist:
            return Response(
                {'exists': False, 'message': 'Consultation non trouvée pour le NSS et le numéro de consultation fournis.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier si le 'bilan radiologique' est dans les bilans prescrits
        bilan_prescrit = [bilan.lower() for bilan in consultation.bilan_prescrit]
        if 'bilan radiologique' not in bilan_prescrit:
            return Response(
                {'exists': False, 'message': 'Bilan radiologique non prescrit pour cette consultation.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Retourner un succès si toutes les validations sont passées
        return Response({'exists': True}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'exists': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

@api_view(['POST'])
def check_consultation_existence_bilan_biologique(request):
    """
    Vérifie l'existence d'une consultation pour un patient, et si un bilan biologique a été prescrit.

    Cette fonction prend le NSS et le numéro de consultation en entrée, et elle vérifie si :
    - Le patient existe dans la base de données.
    - Le dossier patient existe pour ce patient.
    - La consultation existe avec le numéro donné.
    - Le 'bilan biologique' est prescrit dans les bilans de la consultation.

    Paramètres:
        request (Request): La requête HTTP contenant les informations de NSS et de numéro de consultation.

    Retour:
        Response: La réponse HTTP indiquant si la consultation existe, si un bilan biologique est prescrit ou si des erreurs se sont produites.
    """
    try:
        # Extraire les données
        nss = request.data.get('nss')
        numero_consultation = request.data.get('numcons')
        
        # Vérifier les champs obligatoires
        if not nss or not numero_consultation:
            return Response(
                {'exists': False, 'message': 'Le NSS et le numéro de consultation sont requis.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Valider si le patient et le dossier patient existent
        try:
            patient = Patient.objects.get(nss=nss)
            dossier_patient = DossierPatient.objects.get(patient=patient)
        except (Patient.DoesNotExist, DossierPatient.DoesNotExist):
            return Response(
                {'exists': False, 'message': 'Patient ou Dossier Patient non trouvé.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier si la consultation existe
        try:
            consultation = Consultation.objects.get(
                dossier_patient=dossier_patient,
                numero_consultation=numero_consultation
            )
        except Consultation.DoesNotExist:
            return Response(
                {'exists': False, 'message': 'Consultation non trouvée pour le NSS et le numéro de consultation fournis.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier si le 'bilan biologique' est dans les bilans prescrits
        bilan_prescrit = [bilan.lower() for bilan in consultation.bilan_prescrit]
        if 'bilan biologique' not in bilan_prescrit:
            return Response(
                {'exists': False, 'message': 'Bilan biologique non prescrit pour cette consultation.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Retourner un succès si toutes les validations sont passées
        return Response({'exists': True}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'exists': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

@api_view(['POST'])
def recuperer_bilan_biologique(request):
    """
    Récupère le bilan biologique pour une consultation spécifique d'un patient.

    Cette fonction prend le NSS et le numéro de consultation en entrée et vérifie les conditions suivantes :
    - Si le patient existe.
    - Si le dossier patient existe.
    - Si la consultation existe.
    - Si le 'bilan biologique' est prescrit.
    - Si un bilan biologique est disponible pour la consultation demandée.

    Paramètres:
        request (Request): La requête HTTP contenant les informations du NSS et du numéro de consultation.

    Retour:
        Response: La réponse HTTP avec les détails du bilan biologique ou un message d'erreur si une étape échoue.
    """
    try:
        # Extraire les données de la requête
        nss = request.data.get('nss')
        numero_consultation = request.data.get('numcons')

        # Vérifier que les champs nécessaires sont fournis
        if not nss or not numero_consultation:
            return Response(
                {'exists': False, 'message': 'NSS et Numéro de Consultation sont requis.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifier si le patient existe
        try:
            patient = Patient.objects.get(nss=nss)
            dossier_patient = DossierPatient.objects.get(patient=patient)
        except (Patient.DoesNotExist, DossierPatient.DoesNotExist):
            return Response(
                {'exists': False, 'message': 'Patient ou Dossier Patient introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier si la consultation existe
        try:
            consultation = Consultation.objects.get(
                dossier_patient=dossier_patient,
                numero_consultation=numero_consultation
            )
        except Consultation.DoesNotExist:
            return Response(
                {'exists': False, 'message': 'Consultation introuvable pour le NSS et Numéro de Consultation donnés.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier si 'bilan biologique' est prescrit
        bilan_prescrit = [bilan.lower() for bilan in consultation.bilan_prescrit]
        if 'bilan biologique' not in bilan_prescrit:
            return Response(
                {'exists': False, 'message': 'Bilan biologique n\'est pas prescrit pour cette consultation.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Si le bilan biologique est prescrit, rechercher les données correspondantes
        try:
            bilan_biologique = BilanBiologique.objects.filter(
                dossier_patient=dossier_patient,
                numero_consultation=numero_consultation
            ).last()
        except BilanBiologique.DoesNotExist:
            return Response(
                {'exists': False, 'message': 'Bilan biologique non trouvé pour cette consultation.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Retourner les détails du bilan biologique trouvé
        return Response(
            {
                'exists': True,
                'bilan_biologique': {
                    'glycemie': bilan_biologique.glycemie,
                    'pression_arterielle': bilan_biologique.pression_arterielle,
                    'cholesterol': bilan_biologique.cholesterol,
                    'date_examen': bilan_biologique.date_examen,
                    'graphe': bilan_biologique.graphe.url if bilan_biologique.graphe else None
                }
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response({'exists': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['POST'])
def recuperer_bilan_radiologique(request):
    """
    Récupère le bilan radiologique pour une consultation spécifique d'un patient.

    Cette fonction prend le NSS et le numéro de consultation en entrée et vérifie les conditions suivantes :
    - Si le patient existe.
    - Si le dossier patient existe.
    - Si la consultation existe.
    - Si le 'bilan radiologique' est prescrit.
    - Si un bilan radiologique est disponible pour la consultation demandée.

    Paramètres:
        request (Request): La requête HTTP contenant les informations du NSS et du numéro de consultation.

    Retour:
        Response: La réponse HTTP avec les détails du bilan radiologique ou un message d'erreur si une étape échoue.
    """
    try:
        # Extraire les données de la requête
        nss = request.data.get('nss')
        numero_consultation = request.data.get('numcons')

        # Vérifier que les champs nécessaires sont fournis
        if not nss or not numero_consultation:
            return Response(
                {'exists': False, 'message': 'NSS et Numéro de Consultation sont requis.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifier si le patient existe
        try:
            patient = Patient.objects.get(nss=nss)
            dossier_patient = DossierPatient.objects.get(patient=patient)
        except (Patient.DoesNotExist, DossierPatient.DoesNotExist):
            return Response(
                {'exists': False, 'message': 'Patient ou Dossier Patient introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier si la consultation existe
        try:
            consultation = Consultation.objects.get(
                dossier_patient=dossier_patient,
                numero_consultation=numero_consultation
            )
        except Consultation.DoesNotExist:
            return Response(
                {'exists': False, 'message': 'Consultation introuvable pour le NSS et Numéro de Consultation donnés.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier si 'bilan radiologique' est prescrit
        bilan_prescrit = [bilan.lower() for bilan in consultation.bilan_prescrit]
        if 'bilan radiologique' not in bilan_prescrit:
            return Response(
                {'exists': False, 'message': 'Bilan radiologique n\'est pas prescrit pour cette consultation.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Si le bilan radiologique est prescrit, rechercher les données correspondantes
        try:
            bilan_radiologique = BilanRadiologique.objects.filter(
                dossier_patient=dossier_patient,
                numero_consultation=numero_consultation
            ).last()
        except BilanRadiologique.DoesNotExist:
            return Response(
                {'exists': False, 'message': 'Bilan radiologique non trouvé pour cette consultation.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Retourner les détails du bilan radiologique trouvé
        return Response(
            {
                'exists': True,
                'bilan_radiologique': {
                    'compte_rendu': bilan_radiologique.compte_rendu,
                    'date_examen': bilan_radiologique.date_examen,
                    'images': bilan_radiologique.images.url if bilan_radiologique.images else None
                }
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response({'exists': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

@api_view(['POST'])
def recuperer_ordonnance(request):
    """
    Récupère l'ordonnance pour une consultation spécifique d'un patient.

    Cette fonction prend le NSS et le numéro de consultation en entrée et vérifie les conditions suivantes :
    - Si le patient existe.
    - Si le dossier patient existe.
    - Si la consultation existe.
    - Si une ordonnance existe pour cette consultation.
    - Si des médicaments sont associés à l'ordonnance.

    Paramètres:
        request (Request): La requête HTTP contenant les informations du NSS et du numéro de consultation.

    Retour:
        Response: La réponse HTTP avec les détails de l'ordonnance et des médicaments ou un message d'erreur si une étape échoue.
    """
    try:
        # Extraire les données de la requête
        nss = request.data.get('nss')
        numero_consultation = request.data.get('numcons')

        # Vérifier que les champs nécessaires sont fournis
        if not nss or not numero_consultation:
            return Response(
                {'exists': False, 'message': 'NSS et Numéro de Consultation sont requis.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifier si le patient existe
        try:
            patient = Patient.objects.get(nss=nss)
            dossier_patient = DossierPatient.objects.get(patient=patient)
        except (Patient.DoesNotExist, DossierPatient.DoesNotExist):
            return Response(
                {'exists': False, 'message': 'Patient ou Dossier Patient introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier si la consultation existe
        try:
            consultation = Consultation.objects.get(
                dossier_patient=dossier_patient,
                numero_consultation=numero_consultation
            )
        except Consultation.DoesNotExist:
            return Response(
                {'exists': False, 'message': 'Consultation introuvable pour le NSS et Numéro de Consultation donnés.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier si une ordonnance existe pour cette consultation
        ordonnance = Ordonnance.objects.filter(
            dossier_patient=dossier_patient,
            consultation=consultation
        ).last()  # Cela renverra None si aucune ordonnance n'est trouvée

        if not ordonnance:
            return Response(
                {'exists': False, 'message': 'Ordonnance non trouvée pour cette consultation.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Récupérer les médicaments associés à l'ordonnance
        medicaments = Medicament.objects.filter(ordonnance=ordonnance)

        # Construire la liste des médicaments
        medicaments_data = []
        for medicament in medicaments:
            medicaments_data.append({
                'nom': medicament.nom,
                'dose': medicament.dose,
                'duree': medicament.duree
            })

        # Retourner les informations de l'ordonnance et des médicaments
        return Response(
            {
                'exists': True,
                'ordonnance': {
                    'id': ordonnance.id,
                    'consultation_id': ordonnance.consultation.id,
                    'dossier_patient_id': ordonnance.dossier_patient.id
                },
                'medicaments': medicaments_data
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response({'exists': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def get_ordonnance_by_nss_and_consultation(request):
    """
    Récupère l'ordonnance d'un patient identifiée par son NSS et le numéro de consultation,
    si le 'bilan_prescrit' contient 'ordonnance'.
    
    Cette fonction cherche la consultation associée au patient, vérifie si l'ordonnance est incluse
    dans le bilan prescrit, et retourne les informations de l'ordonnance et des médicaments associés.

    Paramètres:
        request (Request): La requête HTTP contenant les informations du NSS et du numéro de consultation.
        
    Retour:
        Response: La réponse HTTP avec les détails de l'ordonnance et des médicaments ou un message d'erreur si une étape échoue.
    """
    nss = request.data.get('nss')  # Extraire le NSS des données de la requête
    numero_consultation = request.data.get('numero_consultation')  # Extraire le numéro de consultation

    # Vérifier que les champs nécessaires sont fournis
    if not nss or not numero_consultation:
        return Response({'message': 'Le NSS et le numéro de consultation sont requis.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Trouver le patient avec le NSS fourni
        patient = Patient.objects.get(nss=nss)

        # Récupérer la consultation correspondant au patient et au numéro de consultation,
        # en vérifiant si 'ordonnance' est dans le bilan_prescrit
        consultation = Consultation.objects.filter(
            dossier_patient=patient.dossier_patient,
            numero_consultation=numero_consultation,
            bilan_prescrit__contains='ordonnance'  # Vérifier si 'ordonnance' est dans bilan_prescrit
        ).first()  # Prendre la première consultation qui correspond aux critères

        if not consultation:
            return Response({'message': 'Aucune consultation trouvée correspondant aux critères.'}, status=status.HTTP_404_NOT_FOUND)

        # Récupérer l'ordonnance liée à la consultation
        ordonnance = Ordonnance.objects.filter(consultation=consultation).first()

        if not ordonnance:
            return Response({'message': 'Aucune ordonnance trouvée pour cette consultation.'}, status=status.HTTP_404_NOT_FOUND)

        # Récupérer les médicaments associés à l'ordonnance
        medicaments = Medicament.objects.filter(ordonnance=ordonnance)

        # Sérialiser les données de l'ordonnance et des médicaments
        ordonnance_data = {
            "dossier_patient_id": ordonnance.dossier_patient.id,
            "consultation_id": ordonnance.consultation.id,
            "medicaments": [
                {
                    "nom": medicament.nom,
                    "dose": medicament.dose,
                    "duree": medicament.duree,
                }
                for medicament in medicaments
            ]
        }

        return Response(ordonnance_data, status=status.HTTP_200_OK)

    except Patient.DoesNotExist:
        return Response({'message': 'Aucun patient trouvé avec le NSS fourni.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'message': f'Une erreur inattendue est survenue : {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
