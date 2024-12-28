from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Administrateur, Medecin, Patient, Infirmier, Laborantin, Radiologue, DossierPatient


# this admin approach only supports one admin class which is the CustomUserAdmin class 
# the CustomUserAdmin class is defined below
# it handles editing and adding users while taking into consideration their different roles

# Customize the UserAdmin to make sure custom fields appear in the admin dashboard

class PatientAdminForm(forms.ModelForm):
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
        model = Patient
        fields = '__all__'

class PatientAdmin(UserAdmin):
    model = Patient
    list_display = ('username', 'role', 'email', 'first_name', 'last_name', 'date_naissance', 'numero_telephone', 'nss', 'mutuelle', 'medecin_traitant')
    search_fields = ('nss',)
    ordering = ('nss',)
    
    # Add the custom fields in the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_naissance', 'adresse', 'numero_telephone', 'nss', 'mutuelle', 'medecin_traitant')}),
    )
    # Add the custom fields in the add_fieldsets
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name','date_naissance', 'adresse', 'numero_telephone', 'nss', 'mutuelle', 'medecin_traitant')}),
    )

    # Use the custom form in the admin interface
    form = PatientAdminForm

    #override the save_model function
    def save_model(self, request, obj, form, change):
        # Force the username to be the same as nss
        obj.username = form.cleaned_data.get('nss')  # Set username as nss

        # Check if the object is a Patient and does not already have a 'dossier_patient'
        dossier_patient = DossierPatient.objects.create(
            etat="actif",  # Default state for the dossier
            antécédents="aucun",  # Empty by default
        )

        # Assign this newly created DossierPatient to the Patient object
        obj.dossier_patient = dossier_patient

        # Set other specific fields for the Patient

        obj.role = 'Patient'
        obj.nss = form.cleaned_data.get('nss')
        obj.medecin_traitant = form.cleaned_data.get('medecin_traitant')
        obj.mutuelle = form.cleaned_data.get('mutuelle')

        # Save the object
        super().save_model(request, obj, form, change)



class MedecinAdmin(UserAdmin):
    model = Medecin
    # specifies the model that represents the users
    list_display = ('username', 'role', 'email', 'first_name', 'last_name', 'date_naissance', 'numero_telephone') 
    # Adds the ability to filter the list of users by role in the admin interface.
    search_fields = ('username', 'email',) 
    # Allows the admin to search for users by username, email, and role
    ordering = ('username',)
    # Defines how the users will be ordered in the admin panel (username in this case).
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_naissance', 'adresse', 'numero_telephone')}),
    )
    # Specifies the fields shown when editing a User in the admin interface.
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name','date_naissance', 'adresse', 'numero_telephone')}),
    # Defines which fields appear when creating a new User
    )

    def save_model(self, request, obj, form, change):
        obj.role = 'Medecin'  # Ensure role is 'Medecin' on creation
        super().save_model(request, obj, form, change)

class InfirmierAdmin(UserAdmin):
    model = Infirmier
    # specifies the model that represents the users
    list_display = ('username', 'role', 'email', 'first_name', 'last_name', 'date_naissance', 'numero_telephone') 
    # Adds the ability to filter the list of users by role in the admin interface.
    search_fields = ('username', 'email',) 
    # Allows the admin to search for users by username, email, and role
    ordering = ('username',)
    # Defines how the users will be ordered in the admin panel (username in this case).
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_naissance', 'adresse', 'numero_telephone')}),
    )
    # Specifies the fields shown when editing a User in the admin interface.
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name','date_naissance', 'adresse', 'numero_telephone')}),
    # Defines which fields appear when creating a new User
    )

    def save_model(self, request, obj, form, change):
        obj.role = 'Infirmier'        
        super().save_model(request, obj, form, change)

class LaborantinAdmin(UserAdmin):
    model = Laborantin
    # specifies the model that represents the users
    list_display = ('username', 'role', 'email', 'first_name', 'last_name', 'date_naissance', 'numero_telephone') 
    # Adds the ability to filter the list of users by role in the admin interface.
    search_fields = ('username', 'email',) 
    # Allows the admin to search for users by username, email, and role
    ordering = ('username',)
    # Defines how the users will be ordered in the admin panel (username in this case).
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_naissance', 'adresse', 'numero_telephone')}),
    )
    # Specifies the fields shown when editing a User in the admin interface.
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name','date_naissance', 'adresse', 'numero_telephone')}),
    # Defines which fields appear when creating a new User
    )

    def save_model(self, request, obj, form, change):
        obj.role = 'Laborantin'        
        super().save_model(request, obj, form, change)

class RadiologueAdmin(UserAdmin):
    model = Radiologue
    # specifies the model that represents the users
    list_display = ('username', 'role', 'email', 'first_name', 'last_name', 'date_naissance', 'numero_telephone') 
    # Adds the ability to filter the list of users by role in the admin interface.
    search_fields = ('username', 'email',) 
    # Allows the admin to search for users by username, email, and role
    ordering = ('username',)
    # Defines how the users will be ordered in the admin panel (username in this case).
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_naissance', 'adresse', 'numero_telephone')}),
    )
    # Specifies the fields shown when editing a User in the admin interface.
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name','date_naissance', 'adresse', 'numero_telephone')}),
    # Defines which fields appear when creating a new User
    )

    def save_model(self, request, obj, form, change):
        obj.role = 'Radiologue'        
        super().save_model(request, obj, form, change)

class AdministrateurAdmin(UserAdmin):
    model = Administrateur
    # specifies the model that represents the users
    list_display = ('username', 'role', 'email', 'first_name', 'last_name', 'date_naissance', 'numero_telephone') 
    # Adds the ability to filter the list of users by role in the admin interface.
    search_fields = ('username', 'email',) 
    # Allows the admin to search for users by username, email, and role
    ordering = ('username',)
    # Defines how the users will be ordered in the admin panel (username in this case).
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_naissance', 'adresse', 'numero_telephone')}),
    )
    # Specifies the fields shown when editing a User in the admin interface.
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name','date_naissance', 'adresse', 'numero_telephone')}),
    # Defines which fields appear when creating a new User
    )

    def save_model(self, request, obj, form, change):
        obj.role = 'Administrateur'        
        super().save_model(request, obj, form, change)






# I do not want to register a user without a role
# admin.site.register(User, CustomUserAdmin)
# Registers the custom admin interface for the User model, 
# applying the customizations from CustomUserAdmin

# Register user types 
admin.site.register(Patient, PatientAdmin)
admin.site.register(Medecin, MedecinAdmin)
admin.site.register(Infirmier, InfirmierAdmin)
admin.site.register(Laborantin, LaborantinAdmin)
admin.site.register(Radiologue, RadiologueAdmin)
admin.site.register(Administrateur, AdministrateurAdmin)