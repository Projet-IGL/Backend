from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Login view
    path('', views.home, name='home'),  # Home view for the root URL
    path('register/', views.register_staff, name='register_staff'),
    path('register_patient/', views.register_patient, name='register_patient'),
    path('rechercher_patient/', views.rechercher_patient_par_NSS, name='rechercher_patient'),
]
