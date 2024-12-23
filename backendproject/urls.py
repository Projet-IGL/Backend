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
from django.contrib import admin
from django.urls import path, include

from backendapp.views import login_view
from backendapp.views import rechercher_dpi_par_nss
from backendapp.views import creer_consultation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', login_view, name='login'),
    path('api/rechercher_dpi_par_nss/', rechercher_dpi_par_nss, name='rechercher_dpi_par_nss'),
    path('api/creer_consultation/', creer_consultation , name='creer_consultation'),

]