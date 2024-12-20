from rest_framework import serializers
from .models import User, Administrateur, Medecin, Patient, Infirmier, Laborantin, Radiologue, DossierPatient

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the base User model.
    This will handle common fields across all user roles.
    """
    password = serializers.CharField(write_only=True)  # Ensure password is write-only

    """
    the password field is set as write-only in the serializer. 
    This means that when you serialize a User instance,
    the password is intentionally excluded from the output
    The password is meant to be set, not retrieved.
    """

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'role', 'date_naissance', 'adresse', 'numero_telephone'
        ]

class DossierPatientSerializer(serializers.ModelSerializer):
    """
    Serializer for DossierPatient model, linking to the Patient model.
    """
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    
    class Meta:
        model = DossierPatient
        fields = '__all__'

class AdministrateurSerializer(serializers.ModelSerializer):
    """
    Serializer for Administrateur role.
    Inherits from the base UserSerializer.
    """
    class Meta:
        model = Administrateur
        fields = '__all__'

class MedecinSerializer(serializers.ModelSerializer):
    """
    Serializer for Medecin role.
    """
    class Meta:
        model = Medecin
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient role.
    Handles nested relationship with Medecin (medecin_traitant) and adds DossierPatient.
    """
    medecin_traitant = serializers.PrimaryKeyRelatedField(
        queryset=Medecin.objects.all(), required=False
    )
    dossier_patient = DossierPatientSerializer()  # Nested DossierPatient serializer

    class Meta:
        model = Patient
        fields = '__all__'

class InfirmierSerializer(serializers.ModelSerializer):
    """
    Serializer for Infirmier role.
    """
    class Meta:
        model = Infirmier
        fields = '__all__'

class LaborantinSerializer(serializers.ModelSerializer):
    """
    Serializer for Laborantin role.
    """
    class Meta:
        model = Laborantin
        fields = '__all__'

class RadiologueSerializer(serializers.ModelSerializer):
    """
    Serializer for Radiologue role.
    """
    class Meta:
        model = Radiologue
        fields = '__all__'


