"""CV URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from CV_APP.views import cv, coordinacion, rectores, psicologa


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('CV_APP.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/coordinador/', coordinacion.CoordinadorSignUpView.as_view(), name='coordinador_signup'),
    path('accounts/coordinador2/', coordinacion.CoordinadorSignUpView2.as_view(), name='coordinador_signup2'),
    path('accounts/rector/', rectores.RectorSignUpView.as_view(), name='rector_signup'),
    path('accounts/psicologa/', psicologa.PsicologaSignUpView.as_view(), name='psicologa_signup'),




]
