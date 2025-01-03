from django.apps import AppConfig


class BackendappConfig(AppConfig):
    """
    Configuration de l'application 'backendapp' dans le projet Django.
    
    Cette classe permet de définir les paramètres de base de l'application, tels que :
    - `default_auto_field`: spécifie le type de champ à utiliser pour les clés primaires automatiques.
    - `name`: définit le nom de l'application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backendapp'
