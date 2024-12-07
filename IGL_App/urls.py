from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Login view
    path('', views.home, name='home'),  # Home view for the root URL
]
