import json
import traceback
from itertools import chain
from .__init__ import *
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, PatternFill, Font, Side
from openpyxl.drawing.image import Image
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template,render_to_string
from django.utils.html import strip_tags
from django.template import Context
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count, Sum, Min, Max, Func
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (TemplateView,CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, TemplateView, View)
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from CV_APP.models import Años, Cargo, Colegios, Disposicion, Postulacion, User, Cargo, Titulo
from CV_APP.forms import PostulacionForm

def home(request):
    if request.user.is_authenticated:
        if request.user.is_coordinacion:
            return redirect('coordinacion:psicolaboral')
        if request.user.is_coordinacion2:
            return redirect('coordinacion:psicolaboral')
        if request.user.is_rector:
            return redirect('rectores:index')
        if request.user.is_psicologa:
            return redirect('psicologa:index')
        if request.user.is_monica:
            return redirect('monica:postulantes')
    return render(request, 'index.html')


def index(request):

    if request.method == 'POST':
        form = PostulacionForm(request.POST, request.FILES)
        if form.is_valid():
            postulacion = form.save(commit=False)
            if Postulacion.objects.filter(rut=postulacion.rut):
                messages.error(request, 'Tiene una postulación en proceso.')
            else:

                if postulacion.cargo.id == 6:

                    postulacion.valido = True
                    postulacion.save()
                    form.save_m2m()
                    subject = "Postulación recibida"
                    html_body = render_to_string("mail.html")
                    msg = EmailMultiAlternatives(subject=subject, from_email="postulaciones@bostoneduca.cl",
                        to=[postulacion.email], body=html_body)
                    msg.attach_alternative(html_body, "text/html")
                    msg.send()
                    messages.success(request, '¡Felicidades! Has completado exitosamente el formulario de postulación laboral online. Pronto serás notificado si cumples con el perfil que estamos buscando y si existen vacantes al cargo que postulaste.')

                    return redirect('index')
                else:
                    postulacion.valido = True
                    postulacion.save()
                    form.save_m2m()

                    subject = "Postulación Recibida"
                    html_body = render_to_string("mail.html")
                    msg = EmailMultiAlternatives(subject=subject, from_email="postulaciones@bostoneduca.cl",
                        to=[postulacion.email], body=html_body)
                    msg.attach_alternative(html_body, "text/html")
                    msg.send()
                    messages.success(request, '¡Felicidades! Has completado exitosamente el formulario de postulación laboral online. Pronto serás notificado si cumples con el perfil que estamos buscando y si existen vacantes al cargo que postulaste.')

                    return redirect('index')
    else:
        form = PostulacionForm()

    return render(request, "home.html",{
        'form':form,
       'submit':True,
    })


def load_indi(request):
    cargo_id = request.GET.get('cargo')
    titulo = Titulo.objects.filter(cargo__id=cargo_id).all
    return render(request, 'dropdown.html', {'titulo':titulo})


def user_profile(request):

    return render(request, "user_profile.html")
