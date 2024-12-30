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
    DossierPatientSerializer
)
from .models import User, Medecin, Patient, Infirmier, Laborantin, Radiologue, DossierPatient , Consultation , Soins , Ordonnance , Medicament ,BilanBiologique , BilanRadiologique , Administrateur
from django.shortcuts import get_object_or_404 
from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.dateparse import parse_date
from .models import Patient, Medecin, DossierPatient, User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Medecin, DossierPatient, User, Patient
from .serializers import PatientSerializer
from datetime import datetime

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Authenticate the user
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)  # Log in the user (sets the session)

        # Get or create an authentication token
        token, created = Token.objects.get_or_create(user=user)

        # Prepare response data
        response_data = {
            'token': token.key,
            'username': user.username,
            'role': user.role,
        }

        # Determine the user's specific role and fetch related data
        if user.role == 'Patient':
            try:
                patient = Patient.objects.get(pk=user.pk)
                response_data['data'] = PatientSerializer(patient).data
            except Patient.DoesNotExist:
                return Response({'message': 'Patient data not found'}, status=status.HTTP_400_BAD_REQUEST)

        elif user.role == 'Medecin':
            try:
                medecin = Medecin.objects.get(pk=user.pk)
                response_data['data'] = MedecinSerializer(medecin).data
            except Medecin.DoesNotExist:
                return Response({'message': 'Medecin data not found'}, status=status.HTTP_400_BAD_REQUEST)

        elif user.role == 'Laborantin':
            try:
                laborantin = Laborantin.objects.get(pk=user.pk)
                response_data['data'] = LaborantinSerializer(laborantin).data
            except Laborantin.DoesNotExist:
                return Response({'message': 'Laborantin data not found'}, status=status.HTTP_400_BAD_REQUEST)

        elif user.role == 'Infirmier':
            try:
                infirmier = Infirmier.objects.get(pk=user.pk)
                response_data['data'] = InfirmierSerializer(infirmier).data
            except Infirmier.DoesNotExist:
                return Response({'message': 'Infirmier data not found'}, status=status.HTTP_400_BAD_REQUEST)

        elif user.role == 'Radiologue':
            try:
                radiologue = Radiologue.objects.get(pk=user.pk)
                response_data['data'] = RadiologueSerializer(radiologue).data
            except Radiologue.DoesNotExist:
                return Response({'message': 'Radiologue data not found'}, status=status.HTTP_400_BAD_REQUEST)
            
        elif user.role == 'Administrateur':
            try:
                administrateur = Administrateur.objects.get(pk=user.pk)
                response_data['data'] = AdministrateurSerializer(administrateur).data
            except Administrateur.DoesNotExist:
                return Response({'message': 'Administrateur data not found'}, status=status.HTTP_400_BAD_REQUEST)    

        # Return the final response
        return Response(response_data, status=status.HTTP_200_OK)

    else:
        return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
def rechercher_dpi_par_nss(request):
    nss = request.data.get('nss')  # Get nss from query parameters

    if not nss:
        return Response({'message': 'NSS parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        patient = Patient.objects.get(nss=nss)  # Find the patient by NSS
        dossier_patient = patient.dossier_patient  # Direct reference to DossierPatient
    except Patient.DoesNotExist:
        return Response({'message': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the Patient and DossierPatient instances
    patient_serializer = PatientSerializer(patient) # this will also fetch the dpi data

    # Prepare the response data with both patient and dossier information
    response_data = {
        'patient_data': patient_serializer.data,
    }

    # Return the combined data in the response
    return Response(response_data, status=status.HTTP_200_OK)

        
"""  

@api_view(['POST'])
def create_consultation(request):
        try:
            # Get data from the POST request
            dossier_patient_id = request.POST.get('dossier_patient_id')
            date_consultation_str = request.POST.get('date_consultation', None)

            # Convert date_consultation to datetime and make it timezone-aware
            if date_consultation_str:
                date_consultation = make_aware(datetime.strptime(date_consultation_str, "%Y-%m-%dT%H:%M"))
            else:
                date_consultation = now()

            bilan_prescrit = request.POST.get('bilan_prescrit')
            if bilan_prescrit not in [choice[0] for choice in Consultation.BILAN_CHOICES]:
                messages.error(request, "Invalid value for bilan prescrit.")
                return redirect('create_consultation')

            resume = request.POST.get('resume', '').strip()

            # Find the corresponding dossier patient
            try:
                dossier_patient = DossierPatient.objects.get(id=dossier_patient_id)
            except DossierPatient.DoesNotExist:
                messages.error(request, "Dossier patient not found.")
                return redirect('create_consultation')

            # Create the Consultation object
            consultation = Consultation.objects.create(
                dossier_patient=dossier_patient,
                numero_consultation=numero_consultation,
                date_consultation=date_consultation,
                bilan_prescrit=bilan_prescrit,
                resume=resume,
            )
            messages.success(request, "Consultation created successfully.")
            return redirect('home')

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('create_consultation')

    # For GET requests, render the form
    dossier_patients = DossierPatient.objects.all()
    return render(request, 'consultation.html', {'dossier_patients': dossier_patients})


        
"""  
@api_view(['POST'])
def creer_consultation(request):
    nss = request.data.get('dpi')
    date_consultation = request.data.get('dateTime')
    bilan_prescrit = request.data.get('bilan')
    resume = request.data.get('resume')

    # Check if nss is provided
    if not nss:
        return Response({'message': 'NSS is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Find the corresponding Patient and DossierPatient
    try:
        patient = Patient.objects.get(nss=nss)
        dossier_patient = patient.dossier_patient  # Get the associated DossierPatient
        if not dossier_patient:
            return Response({'message': 'No Dossier Patient found for this patient.'}, status=status.HTTP_404_NOT_FOUND)
    except Patient.DoesNotExist:
        return Response({'message': 'Patient with the given NSS not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Find the last consultation and determine the next numero_consultation
    last_consultation = Consultation.objects.filter(dossier_patient=dossier_patient).order_by('-numero_consultation').first()
    if last_consultation:
        numero_consultation = last_consultation.numero_consultation + 1
    else:
        numero_consultation = 1  # First consultation for this patient

    # Create the Consultation object
    consultation = Consultation.objects.create(
        dossier_patient=dossier_patient,
        date_consultation=date_consultation,
        numero_consultation=numero_consultation,
        bilan_prescrit=bilan_prescrit,
        resume=resume,
    )

    # Return success response
    return Response({'message': 'Consultation created successfully', 'consultation_id': consultation.id}, status=status.HTTP_201_CREATED)

"""
@api_view(['POST'])
def Faire_soin(request):
    dossier_patient_id = request.data.get('dossier_patient')  # Get dossier_patient ID from request data
    infirmier_id = request.data.get('infirmier')  # Get infirmier ID from request data we should have it from the front as the connected
    observation_etat_patient = request.data.get('observation_etat_patient')
    medicament_pris = request.data.get('medicament_pris')
    description_soins = request.data.get('description_soins')
    date_soin = request.data.get('date_soin')

    # Validate the DossierPatient
    try:
        dossier_patient = DossierPatient.objects.get(id=dossier_patient_id)
    except DossierPatient.DoesNotExist:
        return Response({'message': 'Dossier Patient not found'}, status=status.HTTP_404_NOT_FOUND)

    # Validate the Infirmier (optional, since it can be null)
    infirmier = None
    if infirmier_id:
        try:
            infirmier = Infirmier.objects.get(id=infirmier_id)
        except Infirmier.DoesNotExist:
            return Response({'message': 'Infirmier not found'}, status=status.HTTP_404_NOT_FOUND)

    # Create the Soins object
    soins = Soins.objects.create(
        dossier_patient=dossier_patient,
        infirmier=infirmier,
        observation_etat_patient=observation_etat_patient,
        medicament_pris=medicament_pris,
        description_soins=description_soins,
        date_soin=date_soin
    )
    
    return Response({'message': 'Soins created successfully'}, status=status.HTTP_201_CREATED)
"""
@api_view(['POST'])
def Faire_soin(request):
    nss = request.data.get('nss')  # Get NSS from the request data
    infirmier_id = request.data.get('infirmierId')  # Get infirmier ID (optional, linked to the connected user in frontend)
    observation_etat_patient = request.data.get('observations')
    medicament_pris = request.data.get('medicamentAdministre')
    description_soins = request.data.get('details')
    date_soin = request.data.get('time')

    # Validate and retrieve the Patient and their DossierPatient
    try:
        patient = Patient.objects.get(nss=nss)
        dossier_patient = patient.dossier_patient  # Access the linked DossierPatient
    except Patient.DoesNotExist:
        return Response({'message': 'Patient with the provided NSS not found'}, status=status.HTTP_404_NOT_FOUND)
    except DossierPatient.DoesNotExist:
        return Response({'message': 'Dossier Patient for the provided NSS not found'}, status=status.HTTP_404_NOT_FOUND)

    # Validate the Infirmier (optional, since it can be null)
    infirmier = None
    if infirmier_id:
        try:
            infirmier = Infirmier.objects.get(id=infirmier_id)
        except Infirmier.DoesNotExist:
            return Response({'message': 'Infirmier not found'}, status=status.HTTP_404_NOT_FOUND)

    # Create the Soins object
    soins = Soins.objects.create(
        dossier_patient=dossier_patient,
        infirmier=infirmier,
        observation_etat_patient=observation_etat_patient,
        medicament_pris=medicament_pris,
        description_soins=description_soins,
        date_soin=date_soin
    )

    return Response({'message': 'Soins created successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def creer_ordonnance(request):
    try:
        nss = request.data.get('nss', '').strip()
        date_consultation = request.data.get('consultationDate', '').strip()
        medicaments_data = request.data.get('medications', [])  # Expecting a list of medication dictionaries

        if not nss or not date_consultation or not medicaments_data:
            return Response(
                {'error': 'NSS, date_consultation, and medictions are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate and retrieve patient, dossier, and consultation
        patient = get_object_or_404(Patient, nss=nss)
        dossier_patient = get_object_or_404(DossierPatient, patient=patient)
        consultation = get_object_or_404(
            Consultation,
            dossier_patient=dossier_patient,
            date_consultation=date_consultation
        )

        with transaction.atomic():
            # Create the Ordonnance
            ordonnance = Ordonnance.objects.create(
                dossier_patient=dossier_patient,
                consultation=consultation
            )

            # Create Medicaments for the Ordonnance
            for medicament_data in medicaments_data:
                nom = medicament_data.get('medicament')
                dose = medicament_data.get('dose')
                duree = medicament_data.get('duree')

                if not (nom and dose and duree):
                    continue  # Skip incomplete entries

                Medicament.objects.create(
                    ordonnance=ordonnance,
                    nom=nom,
                    dose=dose,
                    duree=duree
                )

        return Response(
            {'message': 'Ordonnance created successfully.'},
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        print("Error:", e)
        return Response(
            {'error': 'An error occurred while creating the ordonnance.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


from django.utils.timezone import make_aware
from datetime import datetime


@api_view(['POST'])
def creer_bilan_biologique(request):
    try:
        # Extract data from the request
        nss = request.data.get('nss')
        laborantin_id = request.data.get('laborantinId')
        print('laborantin ID', laborantin_id)
        date_examen_str = request.data.get('time')
        glycemie = request.data.get('glycemie')
        pression_arterielle = request.data.get('pression')
        cholesterol = request.data.get('cholesterol')
        graphe = request.FILES.get('imageFile')
        numero_consultation = request.data.get ('numcons')

        # Convert date_examen to datetime and make it timezone-aware
        if date_examen_str:
            date_examen = make_aware(datetime.strptime(date_examen_str, "%Y-%m-%dT%H:%M"))
        else:
            date_examen = make_aware(datetime.now())

        # Validate and get laborantin
        try:
            laborantin = Laborantin.objects.get(id=laborantin_id, role='laborantin')
        except Laborantin.DoesNotExist:
            return Response({'message': 'Laborantin not found or invalid ID.'}, status=status.HTTP_404_NOT_FOUND)

        # Validate patient and dossier_patient
        try:
            patient = Patient.objects.get(nss=nss)
            dossier_patient = DossierPatient.objects.get(patient=patient)
        except (Patient.DoesNotExist, DossierPatient.DoesNotExist):
            return Response({'message': 'Patient or Dossier Patient not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Convert glycemie and cholesterol to float if provided
        glycemie = float(glycemie) if glycemie else None
        cholesterol = float(cholesterol) if cholesterol else None

         # Handle image conversion if provided
        if graphe:
            graphe = graphe  # No need to manually read the file; Django handles it
        else:
            graphe = None

        # Create BilanBiologique instance
        bilan_biologique = BilanBiologique.objects.create(
            dossier_patient=dossier_patient,
            laborantin=laborantin,
            date_examen=date_examen,
            graphe= graphe ,  
            glycemie=glycemie,
            pression_arterielle=pression_arterielle,
            cholesterol=cholesterol,
            numero_consultation = numero_consultation
        )


        return Response({'message': 'Bilan Biologique created successfully.'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from .serializers import BilanRadiologiqueSerializer


@api_view(['POST'])
def creer_bilan_radiologique(request):
    try:
        # Extract data from the request
        nss = request.data.get('nss')
        radiologue_id = request.data.get('radiologueId')
        compte_rendu = request.data.get('compteRendu')
        date_examen_str = request.data.get('time')
        numero_consultation = request.data.get('numcons')  # Expecting a number from the request
        image_file = request.FILES.get('imageRadiographie')
        
        
        # Validate and get the radiologue
        try:
            radiologue = Radiologue.objects.get(id=radiologue_id)
        except Radiologue.DoesNotExist:
            return Response({'exists': False, 'message': 'Radiologue not found or invalid ID.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Validate and get the patient and dossier_patient
        try:
            patient = Patient.objects.get(nss=nss)
            dossier_patient = DossierPatient.objects.get(patient=patient)
        except (Patient.DoesNotExist, DossierPatient.DoesNotExist):
            return Response({'exists': False, 'message': 'Patient or Dossier Patient not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        
        # Handle image conversion if provided
        if image_file:
            image_data = image_file  # Django handles file reading
        else:
            image_data = None

        # Create BilanRadiologique instance
        bilan_radiologique = BilanRadiologique.objects.create(
            dossier_patient=dossier_patient,
            radiologue=radiologue,
            compte_rendu=compte_rendu,
            images=image_data,
            date_examen= date_examen_str,
            numero_consultation=numero_consultation
        )

        # Serialize and return the response data
        serializer = BilanRadiologiqueSerializer(bilan_radiologique)
        return Response(
            {'data': serializer.data, 'exists': True},  # Indicating that the bilan was successfully created
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response({'exists': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def creer_patient(request):
    # Extract the patient data from the request

    print("2")

    data = request.data
    if not data:
        return Response({'error': 'No patient data provided.'}, status=status.HTTP_400_BAD_REQUEST)

    # Ensure the provided Medecin exists
    try:
        medecin = Medecin.objects.get(username=data.get('medecin'))
    except Medecin.DoesNotExist:
        return Response({'error': 'Medecin not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Create the DossierPatient instance first
    dossier_patient = DossierPatient.objects.create(
        etat="actif",  # Default state for the dossier
        antécédents="aucun",  # Empty by default
    )

    print('here !')
    

    # Prepare data for the patient (and the nested User fields)
    patient_data = {
        'username': data.get('username'),
        'first_name': data.get('nom'),
        'last_name': data.get('prenom'),
        'email': data.get('email'),
        'password': data.get('password'),
        'role': 'Patient',  # Assigning the role as 'Patient'
        'date_naissance': data.get('dateDeNaissance'),  # Assuming it's in a valid date format
        'adresse': data.get('adresse'),
        'numero_telephone': data.get('numtel'),
        'nss': data.get('nss'),
        'telephone_urgence': data.get('numtelurg'),
        'mutuelle': data.get('mutuelle'),
      
    }

    # Use the PatientSerializer to validate and save the patient
    serializer = PatientSerializer(data=patient_data)

    if serializer.is_valid():
        # Save the patient instance
        patient = serializer.save()
        patient.medecin_traitant = medecin
        patient.dossier_patient = dossier_patient

        # Return the created patient data
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # If the serializer is not valid, return the error response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# THIS FUNCTION SHOULD BE REFACTORED ( IT DOES NOT EVEN HASH THE PASSWORD)
 
@api_view(['GET'])
def verifier_patient_par_nss(request):
    # Get NSS from query parameters
    nss = request.query_params.get('nss', '').strip()  # Strip to remove leading/trailing whitespace or newline
    if not nss:
        return Response({'message': 'NSS is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Check if a patient with the given NSS exists
        patient = Patient.objects.get(nss=nss)
        return Response({
            'exists': 'True', #patient existe f bdd
            'data': {
                'id': patient.id,
                'nom': patient.first_name,  # Using first_name and last_name from AbstractUser
                'prenom': patient.last_name,
                'nss': patient.nss,
                'medecin_traitant': patient.medecin_traitant.first_name if patient.medecin_traitant else None
            }
        }, status=status.HTTP_200_OK)
    except Patient.DoesNotExist:
        return Response({'exists': 'False'}, status=status.HTTP_404_NOT_FOUND) # nexiste pas f bdd 
    

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Patient, Consultation
from .serializers import ConsultationSerializer

@api_view(['POST'])
def get_consultations_by_nss(request):
    """
    Retrieves consultations for a patient identified by their NSS.
    """
    nss = request.data.get('nss')  # Get the NSS from the request data

    if not nss:
        return Response({'message': 'NSS parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Find the patient and their dossier
        patient = Patient.objects.get(nss=nss)
        dossier_patient = patient.dossier_patient

        if not dossier_patient:
            return Response({'message': 'DossierPatient not found for this patient.'}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve consultations associated with the patient's dossier
        consultations = Consultation.objects.filter(dossier_patient=dossier_patient)

        if not consultations.exists():
            return Response({'message': 'No consultations found for this patient.'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize consultations
        serializer = ConsultationSerializer(consultations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Patient.DoesNotExist:
        return Response({'message': 'Patient with the provided NSS not found.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'message': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def get_soins_by_nss(request):
    """
    Retrieves soins (care records) for a patient identified by their NSS.
    """
    nss = request.data.get('nss')  # Get the NSS from the request data

    if not nss:
        return Response({'message': 'NSS parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Find the patient and their dossier
        patient = Patient.objects.get(nss=nss)
        dossier_patient = patient.dossier_patient

        if not dossier_patient:
            return Response({'message': 'DossierPatient not found for this patient.'}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve soins associated with the patient's dossier
        soins_records = Soins.objects.filter(dossier_patient=dossier_patient)

        if not soins_records.exists():
            return Response({'message': 'No soins records found for this patient.'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize soins data
        soins_data = []
        for soin in soins_records:
            soins_data.append({
                'infirmier': soin.infirmier.first_name if soin.infirmier else None,
                'observation_etat_patient': soin.observation_etat_patient,
                'medicament_pris': soin.medicament_pris,
                'description_soins': soin.description_soins,
                'date_soin': soin.date_soin.isoformat()  # Serialize the date to ISO format
            })

        return Response(soins_data, status=status.HTTP_200_OK)

    except Patient.DoesNotExist:
        return Response({'message': 'Patient with the provided NSS not found.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'message': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def check_consultation_existence(request):
    try:
        
        
        # Extraire les données
        nss = request.data.get('nss')
        numero_consultation = request.data.get('numcons')
        
        # Vérifier les champs obligatoires
        if not nss or not numero_consultation:
            return Response(
                {'exists': False, 'message': 'NSS and Consultation Number are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Valider si le patient et le dossier patient existent
        try:
            patient = Patient.objects.get(nss=nss)
            dossier_patient = DossierPatient.objects.get(patient=patient)
        except (Patient.DoesNotExist, DossierPatient.DoesNotExist):
            return Response(
                {'exists': False, 'message': 'Patient or Dossier Patient not found.'},
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
                {'exists': False, 'message': 'Consultation not found for the given NSS and Consultation Number.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier si le 'bilan radiologique' est dans les bilans prescrits
        bilan_prescrit = [bilan.lower() for bilan in consultation.bilan_prescrit]
        if 'bilan radiologique' not in bilan_prescrit:
            return Response(
                {'exists': False, 'message': 'Bilan radiologique is not prescribed for this consultation.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Retourner un succès si toutes les validations sont passées
        return Response({'exists': True}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'exists': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def check_consultation_existence_bilan_biologique(request):
    try:
        
        
        # Extraire les données
        nss = request.data.get('nss')
        numero_consultation = request.data.get('numcons')
        
        # Vérifier les champs obligatoires
        if not nss or not numero_consultation:
            return Response(
                {'exists': False, 'message': 'NSS and Consultation Number are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Valider si le patient et le dossier patient existent
        try:
            patient = Patient.objects.get(nss=nss)
            dossier_patient = DossierPatient.objects.get(patient=patient)
        except (Patient.DoesNotExist, DossierPatient.DoesNotExist):
            return Response(
                {'exists': False, 'message': 'Patient or Dossier Patient not found.'},
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
                {'exists': False, 'message': 'Consultation not found for the given NSS and Consultation Number.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier si le 'bilan biologique' est dans les bilans prescrits
        bilan_prescrit = [bilan.lower() for bilan in consultation.bilan_prescrit]
        if 'bilan biologique' not in bilan_prescrit:
            return Response(
                {'exists': False, 'message': 'Bilan biologique is not prescribed for this consultation.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Retourner un succès si toutes les validations sont passées
        return Response({'exists': True}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'exists': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    