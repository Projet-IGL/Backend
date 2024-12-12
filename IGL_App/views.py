from django.shortcuts import render, redirect
from .models import Staff
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Staff
from django.db import transaction, IntegrityError
from .models import Patient, DossierPatient, Staff


from django.shortcuts import render
from .models import Patient

def rechercher_patient_par_NSS(request):
    patient = None
    no_patient = False

    if request.method == 'POST':
        nss = request.POST.get('nss')
        try:
            patient = Patient.objects.get(nss=nss)
        except Patient.DoesNotExist:
            no_patient = True

    return render(request, 'rechercher_patient.html', {'patient': patient, 'no_patient': no_patient})


 

def login_view(request):
    if request.method == 'POST':
      
        print("POST request received")  # Debug print
        email = request.POST.get('email', '').strip()  # Get and clean the email input
        password = request.POST.get('password', '').strip()  # Get and clean the password input

        # Debug: Print the input values
        print(f"Received email: {email}")
        print(f"Received password: {password}")
        print("All users in the database:")
        for user in Staff.objects.all():
         print(f"Email: {user.email}, Password: {user.mot_de_passe}")        

        try:
            # Attempt to find the user by email
            user = Staff.objects.get(email=email)
            print(f"Found user with email: {user.email}")  # Debug print

            # Verify the password
            if user.mot_de_passe.strip() == password:
                print("Password matches!")  # Debug print
                # Manually set the user in the session
                request.session['user_id'] = user.id
                messages.success(request, 'Login successful!')
                return redirect('rechercher_patient')  # Redirect to rechercher_dpi
            else:
                print("Password does not match.")  # Debug print
                messages.error(request, 'Incorrect password')
        except Staff.DoesNotExist:
            print(f"User not found with email: {email}")  # Debug print
            messages.error(request, 'User not found')

    # Render the login page if the request is not POST or if authentication fails
    return render(request, 'login.html')




def home(request):
    return render(request, 'home.html')



def register_staff(request):
    allowed_roles = ['medecin', 'infirmier', 'radiologue', 'laborantin']  # Allowed roles
    
    if request.method == 'POST':
        # Get and clean the input values
        nom = request.POST.get('nom', '').strip()
        prenom = request.POST.get('prenom', '').strip()
        telephone = request.POST.get('telephone', '').strip()
        email = request.POST.get('email', '').strip()
        adresse = request.POST.get('adresse', '').strip()
        date_naissance = request.POST.get('date_naissance', '').strip()
        mot_de_passe = request.POST.get('mot_de_passe', '').strip()
        role = request.POST.get('role', '').strip()

        # Debugging input
        print(f"Registering staff with Email: {email}, Role: {role}")

        # Validate the role
        if role not in allowed_roles:
            messages.error(request, 'Invalid role. Allowed roles are: medecin, infirmier, radiologue, laborantin.')
            return render(request, 'register.html')  # Render the registration form again

        # Create a new staff member if role is valid
        try:
            staff_member = Staff.objects.create(
                nom=nom,
                prenom=prenom,
                telephone=telephone,
                email=email,
                adresse=adresse,
                date_naissance=date_naissance,
                mot_de_passe=mot_de_passe,  # Plain text password (as requested)
                role=role
            )
            messages.success(request, 'Staff member registered successfully!')
            return redirect('home')  # Redirect to the home page
        except IntegrityError as e:
            if 'unique constraint' in str(e).lower():  # Check for duplicate email
                messages.error(request, 'This email is already registered.')
            else:
                messages.error(request, f'Error registering staff member: {e}')
            print(f"Error: {e}")  # Debug print
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {e}')
            print(f"Unexpected Error: {e}")  # Debug print

    # Render the registration form if the request is not POST
    return render(request, 'register.html')


def register_patient(request):
    if request.method == 'POST':
        # Collect data from the form
        print("Collecting form data...")
        nss = request.POST['nss']
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        date_naissance = request.POST['date_naissance']
        adresse = request.POST['adresse']
        telephone = request.POST['telephone']
        mutuelle = request.POST['mutuelle']
        medecin_traitant_id = request.POST['medecin_traitant']
        personne_a_contacter = request.POST['personne_a_contacter']
        telephone_contact = request.POST['telephone_contact']
        mot_de_passe = request.POST.get('mot_de_passe', '').strip()
        print(f"Form data collected: NSS={nss}, Nom={nom}, Prenom={prenom}, Médecin traitant ID={medecin_traitant_id}")

        try:
            # Verify that the selected médecin traitant is valid
            print(f"Verifying médecin traitant with ID={medecin_traitant_id}...")
            medecin_traitant = Staff.objects.get(id=medecin_traitant_id, role='medecin')
            print(f"Médecin traitant found: {medecin_traitant.nom} {medecin_traitant.prenom}")
        except Staff.DoesNotExist:
            print("Médecin traitant validation failed!")
            messages.error(request, "Le médecin traitant sélectionné n'existe pas ou n'est pas un médecin.")
            return redirect('register_patient')

        try:
            with transaction.atomic():
                print("Starting transaction...")

                # Create the patient
                patient = Patient.objects.create(
                    nss=nss,
                    nom=nom,
                    prenom=prenom,
                    date_naissance=date_naissance,
                    adresse=adresse,
                    telephone=telephone,
                    mutuelle=mutuelle,
                    medecin_traitant=medecin_traitant,
                    personne_a_contacter=personne_a_contacter,
                    telephone_contact=telephone_contact,
                    mot_de_passe=mot_de_passe,
                )
                print(f"Patient created: ID={patient.id}, Name={patient.nom} {patient.prenom}")

                # Create the dossier for the patient
                dossier = DossierPatient.objects.create(
                    patient=patient,
                   
                    code_qr="default_qr_code",  # Replace with logic to generate a QR code if needed
                    etat="Actif",
                    antécédents="/"  # Default value for antecedentes, could be changed if needed
                )
                print(f"Dossier created: ID={dossier.id}, Patient ID={dossier.patient.id}")

            messages.success(request, "Le patient et son dossier ont été créés avec succès.")
            print("Transaction successful: Patient and dossier created.")
            return redirect('home')  # Redirect to a patient list or relevant page
        except Exception as e:
            print(f"An error occurred during the transaction: {str(e)}")
            messages.error(request, f"Une erreur s'est produite: {str(e)}")
            return redirect('register_patient')

    # Handle GET request: Display the form
    print("Fetching list of médecins...")
    medecins = Staff.objects.filter(role='medecin')  # Fetch only médecins
    print(f"Number of médecins found: {medecins.count()}")
    return render(request, 'register_patient.html', {'medecins': medecins})