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
    DossierPatientSerializer
)
from .models import User, Medecin, Patient, Infirmier, Laborantin, Radiologue, DossierPatient , Consultation , Soins , Ordonnance , Medicament ,BilanBiologique , BilanRadiologique
from django.shortcuts import get_object_or_404 
from django.db import transaction

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
    dossier_patient = request.data.get('dossier_patient')  # Get nss from query parameters
    print(f"Dossier Patient ID: {dossier_patient}")
    date_consultation = request.data.get('date_consultation')
    bilan_prescrit = request.data.get('bilan_prescrit')
    resume = request.data.get('resume')

    # Find the corresponding dossier patient
    try:
        dossier_patient = DossierPatient.objects.get(id=dossier_patient)
        print(f"Dossier Patient ID: {dossier_patient}")
    except DossierPatient.DoesNotExist:
        return Response({'message': 'Dossier Patient not found'}, status=status.HTTP_404_NOT_FOUND)
    
    last_consultation = Consultation.objects.filter(dossier_patient=dossier_patient).order_by('-numero_consultation').first()
    if last_consultation:
        numero_consultation = last_consultation.numero_consultation + 1
    else:
        numero_consultation = 1  # First consultation for this patient
    print(f"New Numero Consultation: {numero_consultation}")


    # Create the Consultation object
    consultation = Consultation.objects.create(
        dossier_patient=dossier_patient,
        date_consultation=date_consultation,
        numero_consultation=numero_consultation,
        bilan_prescrit=bilan_prescrit,
        resume=resume,
        )
    
    return Response({'message': 'Consultation created successefully'}, status=status.HTTP_200_OK)


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



@api_view(['POST'])
def creer_ordonnance(request):
    try:
        nss = request.data.get('nss', '').strip()
        numero_consultation = request.data.get('numero_consultation', '').strip()
        medicaments_data = request.data.get('medicaments', [])  # Expecting a list of medication dictionaries

        if not nss or not numero_consultation or not medicaments_data:
            return Response(
                {'error': 'NSS, numero_consultation, and medicaments are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate and retrieve patient, dossier, and consultation
        patient = get_object_or_404(Patient, nss=nss)
        dossier_patient = get_object_or_404(DossierPatient, patient=patient)
        consultation = get_object_or_404(
            Consultation,
            dossier_patient=dossier_patient,
            numero_consultation=numero_consultation
        )

        with transaction.atomic():
            # Create the Ordonnance
            ordonnance = Ordonnance.objects.create(
                dossier_patient=dossier_patient,
                consultation=consultation
            )

            # Create Medicaments for the Ordonnance
            for medicament_data in medicaments_data:
                nom = medicament_data.get('nom')
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
        laborantin_id = request.data.get('laborantin_id')
        resultat_analyse = request.data.get('resultat_analyse')
        resultat_examen_imagerie = request.data.get('resultat_examen_imagerie')
        date_examen_str = request.data.get('date_examen')
        glycemie = request.data.get('glycemie')
        pression_arterielle = request.data.get('pression_arterielle')
        cholesterol = request.data.get('cholesterol')

        # Validate required fields
        if not nss or not laborantin_id or not resultat_analyse:
            return Response({'message': 'NSS, Laborantin ID, and Resultat Analyse are required.'}, 
                            status=status.HTTP_400_BAD_REQUEST)

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

        # Create BilanBiologique instance
        bilan_biologique = BilanBiologique.objects.create(
            dossier_patient=dossier_patient,
            laborantin=laborantin,
            resultat_analyse=resultat_analyse,
            resultat_examen_imagerie=resultat_examen_imagerie,
            date_examen=date_examen,
            graphe=None,  # Add logic for handling the graph if needed
            glycemie=glycemie,
            pression_arterielle=pression_arterielle,
            cholesterol=cholesterol
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
        radiologue_id = request.data.get('radiologue_id')
        compte_rendu = request.data.get('compte_rendu')
        date_examen_str = request.data.get('date_examen')
        image_file = request.FILES.get('image')

        # Validate required fields
        if not nss or not radiologue_id or not compte_rendu:
            return Response({'message': 'NSS, Radiologue ID, and Compte Rendu are required.'}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # Convert date_examen to datetime and make it timezone-aware
        if date_examen_str:
            date_examen = make_aware(datetime.strptime(date_examen_str, "%Y-%m-%dT%H:%M:%S"))
        else:
            date_examen = make_aware(datetime.now())

        # Validate and get the radiologue
        try:
            radiologue = Radiologue.objects.get(id=radiologue_id)
        except Radiologue.DoesNotExist:
            return Response({'message': 'Radiologue not found or invalid ID.'}, status=status.HTTP_404_NOT_FOUND)

        # Validate and get the patient and dossier_patient
        try:
            patient = Patient.objects.get(nss=nss)
            dossier_patient = DossierPatient.objects.get(patient=patient)
        except (Patient.DoesNotExist, DossierPatient.DoesNotExist):
            return Response({'message': 'Patient or Dossier Patient not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Handle image conversion if provided
        if image_file:
            image_data = image_file  # No need to manually read the file; Django handles it
        else:
            image_data = None
            
        # Create BilanRadiologique instance
        bilan_radiologique = BilanRadiologique.objects.create(
            dossier_patient=dossier_patient,
            radiologue=radiologue,
            compte_rendu=compte_rendu,
            images=image_data,
            date_examen=date_examen
        )

        # Serialize and return the response data
        serializer = BilanRadiologiqueSerializer(bilan_radiologique)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
