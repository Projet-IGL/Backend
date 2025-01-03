from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Administrateur, Medecin, Patient, Infirmier, Laborantin, Radiologue, DossierPatient

# Ce fichier admin.py configure l'interface d'administration pour les modèles définis dans l'application.
# Il personnalise l'affichage et la gestion des utilisateurs avec différents rôles dans l'interface d'administration de Django.

class PatientAdminForm(forms.ModelForm):
    """
    Formulaire personnalisé pour le modèle Patient dans l'interface d'administration.
    Permet d'ajouter des champs spécifiques tels que le NSS, la mutuelle et le médecin traitant.
    """
    nss = forms.CharField(
        required=True,
        label="Numéro de Sécurité Sociale",
        help_text="Entrez le NSS du patient."
    )
    mutuelle = forms.CharField(
        required=False,
        label="Mutuelle",
        help_text="Entrez le nom de la mutuelle du patient (facultatif)."
    )
    medecin_traitant = forms.ModelChoiceField(
        queryset=Medecin.objects.all(),
        required=False,
        label="Médecin Traitant",
        help_text="Choisissez un médecin traitant pour le patient.",
        empty_label="Choisissez un Médecin"
    )

    class Meta:
        """
        Méta-données associées au formulaire PatientAdminForm.
        Indique que ce formulaire est lié au modèle Patient.
        """
        model = Patient
        fields = '__all__'

class PatientAdmin(UserAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Patient.
    Personnalise l'affichage, les champs disponibles et les actions possibles.
    """
    model = Patient
    list_display = ('username', 'role', 'email', 'first_name', 'last_name', 'date_naissance', 'numero_telephone', 'nss', 'mutuelle', 'medecin_traitant')
    search_fields = ('nss',)
    ordering = ('nss',)

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_naissance', 'adresse', 'numero_telephone', 'nss', 'mutuelle', 'medecin_traitant')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name','date_naissance', 'adresse', 'numero_telephone', 'nss', 'mutuelle', 'medecin_traitant')}),
    )

    form = PatientAdminForm

    def save_model(self, request, obj, form, change):
        """
        Méthode appelée lors de la sauvegarde d'un objet Patient dans l'interface d'administration.
        Personnalise la sauvegarde en définissant le username comme le NSS, en créant un DossierPatient par défaut,
        et en assignant les rôles et champs spécifiques.
        """
        obj.username = form.cleaned_data.get('nss')
        dossier_patient = DossierPatient.objects.create(
            etat="actif",
            antécédents="aucun",
        )
        obj.dossier_patient = dossier_patient
        obj.role = 'Patient'
        obj.nss = form.cleaned_data.get('nss')
        obj.medecin_traitant = form.cleaned_data.get('medecin_traitant')
        obj.mutuelle = form.cleaned_data.get('mutuelle')
        super().save_model(request, obj, form, change)

class MedecinAdmin(UserAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Medecin.
    Gère les utilisateurs ayant le rôle de médecin.
    """
    model = Medecin
    list_display = ('username', 'role', 'email', 'first_name', 'last_name', 'date_naissance', 'numero_telephone')
    search_fields = ('username', 'email',)
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_naissance', 'adresse', 'numero_telephone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name','date_naissance', 'adresse', 'numero_telephone')}),
    )

    def save_model(self, request, obj, form, change):
        """
        Définit le rôle de l'utilisateur comme 'Medecin' lors de la sauvegarde.
        """
        obj.role = 'Medecin'
        super().save_model(request, obj, form, change)

class InfirmierAdmin(UserAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Infirmier.
    Gère les utilisateurs ayant le rôle d'infirmier.
    """
    model = Infirmier
    list_display = ('username', 'role', 'email', 'first_name', 'last_name', 'date_naissance', 'numero_telephone')
    search_fields = ('username', 'email',)
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_naissance', 'adresse', 'numero_telephone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name','date_naissance', 'adresse', 'numero_telephone')}),
    )

    def save_model(self, request, obj, form, change):
        """
        Définit le rôle de l'utilisateur comme 'Infirmier' lors de la sauvegarde.
        """
        obj.role = 'Infirmier'
        super().save_model(request, obj, form, change)

class LaborantinAdmin(UserAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Laborantin.
    Gère les utilisateurs ayant le rôle de laborantin.
    """
    model = Laborantin
    list_display = ('username', 'role', 'email', 'first_name', 'last_name', 'date_naissance', 'numero_telephone')
    search_fields = ('username', 'email',)
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_naissance', 'adresse', 'numero_telephone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name','date_naissance', 'adresse', 'numero_telephone')}),
    )

    def save_model(self, request, obj, form, change):
        """
        Définit le rôle de l'utilisateur comme 'Laborantin' lors de la sauvegarde.
        """
        obj.role = 'Laborantin'
        super().save_model(request, obj, form, change)

class RadiologueAdmin(UserAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Radiologue.
    Gère les utilisateurs ayant le rôle de radiologue.
    """
    model = Radiologue
    list_display = ('username', 'role', 'email', 'first_name', 'last_name', 'date_naissance', 'numero_telephone')
    search_fields = ('username', 'email',)
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_naissance', 'adresse', 'numero_telephone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name','date_naissance', 'adresse', 'numero_telephone')}),
    )

    def save_model(self, request, obj, form, change):
        """
        Définit le rôle de l'utilisateur comme 'Radiologue' lors de la sauvegarde.
        """
        obj.role = 'Radiologue'
        super().save_model(request, obj, form, change)

class AdministrateurAdmin(UserAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Administrateur.
    Gère les utilisateurs ayant le rôle d'administrateur.
    """
    model = Administrateur
    list_display = ('username', 'role', 'email', 'first_name', 'last_name', 'date_naissance', 'numero_telephone')
    search_fields = ('username', 'email',)
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_naissance', 'adresse', 'numero_telephone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name','date_naissance', 'adresse', 'numero_telephone')}),
    )

    def save_model(self, request, obj, form, change):
        """
        Définit le rôle de l'utilisateur comme 'Administrateur' lors de la sauvegarde.
        """
        obj.role = 'Administrateur'
        super().save_model(request, obj, form, change)

# Enregistrement des modèles et des classes admin associées dans l'interface d'administration
admin.site.register(Patient, PatientAdmin)
admin.site.register(Medecin, MedecinAdmin)
admin.site.register(Infirmier, InfirmierAdmin)
admin.site.register(Laborantin, LaborantinAdmin)
admin.site.register(Radiologue, RadiologueAdmin)
admin.site.register(Administrateur, AdministrateurAdmin)
