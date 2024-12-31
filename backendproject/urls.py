"""
URL configuration for backendproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from backendapp.views import login_view
from backendapp.views import rechercher_dpi_par_nss
from backendapp.views import creer_consultation
from backendapp.views import Faire_soin
from backendapp.views import creer_patient , creer_ordonnance ,creer_bilan_biologique, creer_bilan_radiologique, verifier_patient_par_nss, rechercher_dpi_par_nss, get_consultations_by_nss,get_soins_by_nss, check_consultation_existence, check_consultation_existence_bilan_biologique, recuperer_bilan_biologique, recuperer_bilan_radiologique, recuperer_ordonnance, get_ordonnance_by_nss_and_consultation


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', login_view, name='login'),
    path('api/rechercher_dpi_par_nss/', rechercher_dpi_par_nss, name='rechercher_dpi_par_nss'),
    path('api/creer_consultation/', creer_consultation , name='creer_consultation'),
    path('api/faire_soin/', Faire_soin, name='faire_soin'),
    path('api/Rediger_ordonnance/', creer_ordonnance, name='Rediger_ordonnance'),
    path('api/creer_bilan_biologique/', creer_bilan_biologique, name='creer_bilan_biologique'),
    path('api/creer_bilan_radiologique/', creer_bilan_radiologique, name='creer_bilan_radiologique'),
    path('api/creer_patient/', creer_patient, name='creer_patient'),
    path('api/checkNss/', verifier_patient_par_nss, name='checkNss'),
    path('api/ConsultationbyNSS/', get_consultations_by_nss, name='ConsultationbyNSS'),
    path('api/soinsByNSS/', get_soins_by_nss, name='soinsByNSS'),
    path('api/check_consultation_existence/', check_consultation_existence, name='check_consultation_existence'),
    path('api/check_consultation_existence_bilan_biologique/', check_consultation_existence_bilan_biologique, name='check_consultation_existence_bilan_biologique'),
    path('api/recuperer_bilan_biologique/', recuperer_bilan_biologique, name='recuperer_bilan_biologique'),
    path('api/recuperer_bilan_radiologique/', recuperer_bilan_radiologique, name='recuperer_bilan_radiologique'),
    path('api/recuperer_ordonnance/', recuperer_ordonnance, name='recuperer_ordonnance'),
    path('api/get_ordonnace/', get_ordonnance_by_nss_and_consultation, name='get_ordonnance'),

]




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)