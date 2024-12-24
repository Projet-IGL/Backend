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
from .models import User, Medecin, Patient, Infirmier, Laborantin, Radiologue, DossierPatient , Consultation , Soins

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
        
"""  

        
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
    date_consultation = request.data.get('date_consultation')
    bilan_prescrit = request.data.get('bilan_prescrit')
    resume = request.data.get('resume')

    # Find the corresponding dossier patient
    try:
        dossier_patient = DossierPatient.objects.get(id=dossier_patient)
    except DossierPatient.DoesNotExist:
        return Response({'message': 'Dossier Patient not found'}, status=status.HTTP_404_NOT_FOUND)


    # Create the Consultation object
    consultation = Consultation.objects.create(
        dossier_patient=dossier_patient,
        date_consultation=date_consultation,
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


"""
def ajouter_soin(request):
    # Récupérer les dossiers des patients et les infirmiers
    dossier_patients = DossierPatient.objects.all()
    infirmiers = Staff.objects.filter(role='infirmier')  # Assurez-vous d'avoir un champ "role" pour filtrer les infirmiers

    if request.method == 'POST':
        # Récupérer les données du formulaire
        dossier_patient_id = request.POST.get('dossier_patient')
        infirmier_id = request.POST.get('infirmier')
        observation_etat_patient = request.POST.get('observation_etat_patient')
        medicament_pris = request.POST.get('medicament_pris') == 'on'  # Le checkbox envoie "on" si coché
        description_soins = request.POST.get('description_soins')
        date_soin = request.POST.get('date_soin')

        try:
            # Enregistrer les données dans la table Soins
            soin = Soins.objects.create(
                dossier_patient_id=dossier_patient_id,
                infirmier_id=infirmier_id,
                observation_etat_patient=observation_etat_patient,
                medicament_pris=medicament_pris,
                description_soins=description_soins,
                date_soin=date_soin
            )

            messages.success(request, 'Soin ajouté avec succès!')
            return redirect('home')  # Remplacez par l'URL de votre choix

        except Exception as e:
            messages.error(request, f"Erreur lors de l'ajout du soin: {e}")

    return render(request, 'ajouter_soin.html', {
        'dossier_patients': dossier_patients,
        'infirmiers': infirmiers
    })
"""
