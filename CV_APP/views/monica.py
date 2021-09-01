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
from ..decorators import monica_required
from CV_APP.models import Rubrica_equipomulti,Rubrica_demo, Años, Cargo, Colegios, Disposicion, Postulacion, User,  Rubrica, Rubrica_psicologa, Rubrica_coordinador, Psicologa
from CV_APP.forms import PostulacionForm, PostulantesRector, RubricaForm, Entrevistado, Psicologa, Aprobado, PsicologaSignUpForm, Aceptar_fat

@login_required
@monica_required
def rubricas(request, pk):
    postulacion = get_object_or_404(Postulacion, pk=pk)
    postulantes = Rubrica.objects.filter(postulacion__id = postulacion.id)
    postulante_demo = Rubrica_demo.objects.filter(postulacion__id = postulacion.id)
    postulante_em = Rubrica_equipomulti.objects.filter(postulacion__id = postulacion.id)
    postulante_psicologa = Rubrica_psicologa.objects.filter(postulantes__id = postulacion.id)
    postulante_c = Rubrica_coordinador.objects.filter(postulacion__id = postulacion.id)

    return render(request, "monica/rubricas.html",{'postulantes':postulantes,'postulacion':postulacion,'postulante_demo':postulante_demo,'postulante_em':postulante_em, 'postulante_psicologa':postulante_psicologa,'postulante_c':postulante_c})

@login_required
@monica_required
def index(request):
    postulantes = Postulacion.objects.filter(psicologa=True)
    return render(request, "monica/index.html",{'postulantes':postulantes})

@login_required
@monica_required
def rechazados(request):
    postulante = Postulacion.objects.all()
    return render(request, "monica/rechazados.html", {'postulante':postulante})

@login_required
@monica_required
def vista_rubrica(request, pk):
    rubrica =get_object_or_404(Rubrica, pk=pk)
    puntos = Rubrica.objects.filter(id=rubrica.pk).values('puntos','puntos2','puntos3','puntos4','puntos5','puntos6','puntos7','puntos8','puntos9','puntos10').aggregate(suma=Sum('puntos') + Sum('puntos2') + Sum('puntos3') + Sum('puntos4') + Sum('puntos5') + Sum('puntos6') + Sum('puntos7') + Sum('puntos8') + Sum('puntos9') + Sum('puntos10'))

    return render(request, "monica/vista_rubrica.html", {'rubrica':rubrica,'puntos':puntos})

@login_required
@monica_required
def vista_rubricaC(request, pk):
    rubrica =get_object_or_404(Rubrica_coordinador, pk=pk)
    puntos = Rubrica_coordinador.objects.filter(id=rubrica.pk).values('puntos','puntos2','puntos3','puntos4','puntos5','puntos6','puntos7').aggregate(suma=Sum('puntos') + Sum('puntos2') + Sum('puntos3') + Sum('puntos4') + Sum('puntos5') + Sum('puntos6') + Sum('puntos7'))

    return render(request, "monica/vista_rubrica_coordinador.html", {'rubrica':rubrica,'puntos':puntos})

@login_required
@monica_required
def vista_rubrica_equipo(request, pk):
    rubrica =get_object_or_404(Rubrica_equipomulti, pk=pk)
    total = 30
    puntos = Rubrica_equipomulti.objects.filter(id=rubrica.pk).values('puntos','puntos2','puntos3','puntos4','puntos5','puntos6','puntos7','puntos8','puntos9').aggregate(suma=Sum('puntos') + Sum('puntos2') + Sum('puntos3') + Sum('puntos4') + Sum('puntos5') + Sum('puntos6') + Sum('puntos7') + Sum('puntos8') + Sum('puntos9') )
    return render(request, "monica/vista_rubrica_equipo.html", {'rubrica':rubrica,'puntos':puntos})

@login_required
@monica_required
def vista_rubrica_demo(request, pk):
    rubrica =get_object_or_404(Rubrica_demo, pk=pk)
    return render(request, "monica/vista_rubrica_demo.html", {'rubrica':rubrica})

@login_required
@monica_required
def vista_rubrica_psicologa(request, pk):
    rubrica =get_object_or_404(Rubrica_psicologa, pk=pk)
    return render(request, "monica/vista_rubrica_psicologica.html", {'rubrica':rubrica})

@login_required
@monica_required
def finalizados(request):
    postulante = Postulacion.objects.filter(valido=True, entrevistado=True, rechazar=False, finalizado=True, aceptada = True)

    return render(request, "monica/finalizados.html",{'postulante':postulante})

@login_required
@monica_required
def aceptar(request):
    postulante = Postulacion.objects.filter(send = True, finalizado = False, aceptar_ficha=False)

    return render(request, "monica/aceptar.html",{'postulante':postulante})

@login_required
@monica_required
def info(request, pk):
    postulante = get_object_or_404(Postulacion, pk=pk)
    return render(request, "psicologa/info.html",{'postulante':postulante})

@login_required
@monica_required
def postulantes(request):
    postulantes = Postulacion.objects.filter(liberar_coordinador=True, psicologa=False)
    return render(request, "monica/postulantes.html",{'postulantes':postulantes})

@login_required
@monica_required
def finalizar(request, pk):
    postulantes = get_object_or_404(Postulacion, pk=pk)
    if request.method == 'POST':
        form = Aceptar_fat(request.POST, request.FILES, instance=postulantes)
        if form.is_valid():
            with transaction.atomic():
                postulante = form.save(commit=False)
                postulante.save()

                subject = "Ficha FAT aceptada"
                html_body = render_to_string("monica/mail_aceptada.html", {'postulantes':postulantes})
                msg = EmailMultiAlternatives(subject=subject, from_email="postulaciones@bostoneduca.cl",
                    to=['yonyx.m.p@gmail.com'], cc=['ymartinez@bostoneduca.cl','yonyx.m.p@gmail.com'],body=html_body)
                msg.attach_alternative(html_body, "text/html")
                msg.send()
            
            return redirect('monica:aceptar')
    else:
        form = Aceptar_fat(instance=postulantes)
    return render(request, "monica/aceptar_ficha_view.html",{'postulantes':postulantes, 'form':form})