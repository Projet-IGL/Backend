from rest_framework import serializers
from .models import User, Administrateur, Medecin, Patient, Infirmier, Laborantin, Radiologue, DossierPatient, Consultation , Soins , Medicament, Ordonnance , BilanRadiologique, BilanBiologique

class UserSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle utilisateur de base. Gère les champs communs à tous les rôles d'utilisateur.
    Le champ mot de passe est écrit uniquement, il ne sera pas retourné lors de la sérialisation.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'role', 'date_naissance', 'adresse', 'numero_telephone'
        ]

class DossierPatientSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle DossierPatient, liant un patient spécifique au dossier.
    """
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    
    class Meta:
        model = DossierPatient
        fields = '__all__'

class AdministrateurSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le rôle d'Administrateur. Hérite des champs du modèle User.
    """
    class Meta:
        model = Administrateur
        fields = '__all__'

class MedecinSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le rôle de Médecin. Gère les informations spécifiques au médecin.
    """
    class Meta:
        model = Medecin
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le rôle de Patient. Gère la relation avec le médecin traitant et le dossier du patient.
    Les informations du médecin traitant et du dossier sont sérialisées de manière imbriquée.
    """
    medecin_traitant = MedecinSerializer(allow_null=True, required=False)
    dossier_patient = DossierPatientSerializer(allow_null=True, required=False)

    class Meta:
        model = Patient
        fields = '__all__'

class InfirmierSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le rôle d'Infirmier. Gère les informations spécifiques à l'infirmier.
    """
    class Meta:
        model = Infirmier
        fields = '__all__'

class LaborantinSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le rôle de Laborantin. Gère les informations spécifiques au laborantin.
    """
    class Meta:
        model = Laborantin
        fields = '__all__'

class RadiologueSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le rôle de Radiologue. Gère les informations spécifiques au radiologue.
    """
    class Meta:
        model = Radiologue
        fields = '__all__'

class ConsultationSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la consultation d'un patient. Gère les informations de la consultation ainsi que le médecin consultant.
    """
    medecinConsultant = MedecinSerializer()

    class Meta:
        model = Consultation
        fields = '__all__'

class SoinsSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les soins administrés au patient. Gère toutes les informations liées aux soins médicaux.
    """
    class Meta:
        model = Soins
        fields = '__all__'

class MedicamentsSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les médicaments prescrits. Gère les informations des médicaments associés à un soin ou une ordonnance.
    """
    class Meta:
        model = Medicament
        fields = '__all__'

class OrdonnaceSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les ordonnances prescrites. Gère les informations des ordonnances.
    """
    class Meta:
        model = Ordonnance
        fields = '__all__'

class BilanBiologiqueSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le bilan biologique. Gère les informations relatives aux bilans biologiques effectués sur le patient.
    """
    class Meta:
        model = BilanBiologique
        fields = '__all__'

class BilanRadiologiqueSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le bilan radiologique. Gère les informations relatives aux bilans radiologiques effectués sur le patient.
    """
    class Meta:
        model = BilanRadiologique
        fields = '__all__'
