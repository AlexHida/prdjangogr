"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.login, name='login'),  # Página de inicio es el login
    path('index/', views.index, name='index'),  # Vista para index.html
    path('qa/', views.qa_index, name='qa_index'),
    path('videos/', views.videos_index, name='videos_index'),
    path('corrector/', views.correctorGramatica, name='corrector'),
    path('ayuda/', views.ayuda, name='ayuda'),
    path('docente/', views.vista_docente, name='docente'),
]