import json
import traceback
import time
from datetime import date
from datetime import datetime
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
from django.views.generic import (TemplateView,CreateView, DeleteView, DetailView, ListView, UpdateView, TemplateView, View)
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from ..decorators import rector_required
from CV_APP.models import Rubrica_coordinador,Rubrica_demo,Años, Cargo, Colegios, Disposicion, Postulacion, User,  Rubrica, Rubrica_equipomulti, Rubrica_psicologa
from CV_APP.forms import Editar_r, RubricaCForm,Oferta,FichaFatForm,EntrevistadoDemo,RubricaDemoForm,PostulacionForm, PostulantesRector,  PostulantesRectorLiberar ,RubricaForm, Entrevistado, RectorSignUpForm,RubricaEmForm


class RectorSignUpView(CreateView):
    model = User
    form_class = RectorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Rector'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('rectores:index')

@login_required
@rector_required
def index(request):
    usuario = request.user.rector
    colegio = usuario.colegio.all()[0]
    postulante = Postulacion.objects.filter(valido=True, Siguiente=False, liberar_2=False, liberar_3=False, rechazar_index=False )
    postulante2 = Postulacion.objects.filter(valido=True, Siguiente=False, liberar_2=True, liberar_3=False, rechazar_index=False )
    postulante3 = Postulacion.objects.filter(valido=True, Siguiente=False, liberar_2=True,liberar_3=True, rechazar_index=False)

    return render(request, "rector/index.html", {'usuario':usuario,'postulante':postulante,'postulante2':postulante2,'postulante3':postulante3,'colegio':colegio})

@login_required
@rector_required
def info(request, pk):
    postulante = get_object_or_404(Postulacion, pk=pk)
    postulantes = Postulacion.objects.all()
    if request.method == 'POST':
        form = PostulantesRector(request.POST, request.FILES, instance=postulante)
        if form.is_valid():
            with transaction.atomic():
                postulantes = form.save(commit=False)
                if postulantes.liberar_2 == True:
                    postulantes.colegio1 = postulante.colegio2
                    postulantes.colegio2 = postulante.colegio1 
                postulantes.save()
            messages.success(request, 'Postulación Aceptada')
            return redirect('rectores:index')
    else:
        form = PostulantesRector(instance=postulante)
    return render(request, "rector/info.html",{'postulante':postulante,'form':form,})



@login_required
@rector_required
def cargo(request):
    usuario = request.user.rector
    colegio = usuario.colegio.all()[0]
    postulante = Postulacion.objects.filter(liberar_2=False, liberar_3=False)
    postulante2 =  Postulacion.objects.filter(liberar_2=True, liberar_3=False)
    postulante3 =  Postulacion.objects.filter(liberar_2=True,liberar_3=True)
    return render(request, "rector/cargos.html", {'postulante':postulante, 'postulante2':postulante2, 'postulante3':postulante3, 'colegio':colegio})

@login_required
@rector_required
def entrevista(request):
    usuario = request.user.rector
    colegio = usuario.colegio.all()[0]
    postulantes =  Postulacion.objects.filter(Siguiente=True, entrevistado=False,email_send=False, liberar_2=False, liberar_3=False)
    postulantes2 =  Postulacion.objects.filter(Siguiente=True, entrevistado=False,email_send=False, liberar_2=True, liberar_3=False)
    postulantes3 =  Postulacion.objects.filter(Siguiente=True, entrevistado=False,email_send=False, liberar_2=True,liberar_3=True)

    return render(request, "rector/entrevistas.html",{'postulantes':postulantes,'postulantes2':postulantes2,'postulantes3':postulantes3,'colegio':colegio})

@login_required
@rector_required
def rubricas(request, pk):
    usuario = request.user.rector
    colegio = usuario.colegio.all()[0]
    postulacion = get_object_or_404(Postulacion, pk=pk)
    postulantes = Rubrica.objects.filter(postulacion__id = postulacion.id, postulacion__colegio1=colegio)
    postulante_demo = Rubrica_demo.objects.filter(postulacion__id = postulacion.id,postulacion__colegio1=colegio,postulacion__entrevistado_demo=True)
    postulante_em = Rubrica_equipomulti.objects.filter(postulacion__id = postulacion.id,postulacion__colegio1=colegio)
    postulante_psicologa = Rubrica_psicologa.objects.filter(postulantes__id = postulacion.id, postulantes__colegio1=colegio)
    postulante_c = Rubrica_coordinador.objects.filter(postulacion__id = postulacion.id)
    return render(request, "rector/rubricas.html",{'postulantes':postulantes,'postulacion':postulacion,'postulante_demo':postulante_demo,'postulante_em':postulante_em, 'postulante_psicologa':postulante_psicologa,'postulante_c':postulante_c})


@login_required
@rector_required
def clasedemo(request):
    usuario = request.user.rector
    colegio = usuario.colegio.all()[0]
    postulantes = Rubrica.objects.filter(postulacion__Siguiente=True, entrevistado=True,postulacion__aprobar_demos=False, postulacion__rechazar_demos=False, postulacion__rechazar_rector=False, postulacion__liberar_2=False, postulacion__liberar_3=False)
    postulantes2 = Rubrica.objects.filter(postulacion__Siguiente=True, entrevistado=True,postulacion__aprobar_demos=False, postulacion__rechazar_demos=False, postulacion__rechazar_rector=False, postulacion__liberar_2=True, postulacion__liberar_3=False)
    postulantes3 = Rubrica.objects.filter(postulacion__Siguiente=True, entrevistado=True,postulacion__aprobar_demos=False, postulacion__rechazar_demos=False, postulacion__rechazar_rector=False, postulacion__liberar_2=True, postulacion__liberar_3=True)


    return render(request, "rector/clase_demostrativa.html",{'postulantes':postulantes,'postulantes2':postulantes2,'postulantes3':postulantes3,'colegio':colegio})


@login_required
@rector_required
def aprobados(request):
    usuario = request.user.rector
    colegio = usuario.colegio.all()[0]
    postulante = Postulacion.objects.filter( Siguiente=True,psicologa=False,rechazar_rector=False, rechazar=False, liberar_2=False, liberar_3=False )
    postulante2 = Postulacion.objects.filter( Siguiente=True,psicologa=False,rechazar_rector=False, rechazar=False, liberar_2=True, liberar_3=False )
    postulante3 = Postulacion.objects.filter( Siguiente=True,psicologa=False,rechazar_rector=False, rechazar=False, liberar_2=True,liberar_3=True )

    return render(request, "rector/aprobados_psicologica.html", {'postulante':postulante,'postulante2':postulante2,'postulante3':postulante3,'colegio':colegio})

@login_required
@rector_required
def rubrica_coordinador(request, pk):
    postulantes = get_object_or_404(Postulacion, pk=pk)
    rubrica = Rubrica_coordinador.objects.filter(postulacion=postulantes)
    if request.method == 'POST':
        form = Entrevistado(request.POST, request.FILES, instance=postulantes)
        formset = RubricaCForm(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                postulante = form.save(commit=False)
                rubrica = formset.save(commit=False)
                rubrica.owner = request.user
                postulante.rector = request.user
                postulante.coordinador = True

                rubrica.postulacion = postulantes
                if rubrica.puntos == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos2 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos3 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos4 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos5 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos6 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos7 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')

                if rubrica.puntos == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos2 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos3 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos4 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos5 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos6 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos7 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')

                if rubrica.puntos + rubrica.puntos2 + rubrica.puntos3 + rubrica.puntos4 + rubrica.puntos5 + rubrica.puntos6 + rubrica.puntos7 <= 14:
                    postulantes.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada el resultado es menos que 15 pts')
                postulante.entrevistado = True

                postulante.save()
                rubrica.save()

                if postulante.rechazar_rector == False:
                    subject = "Postulante entrevistado"

                    html_body = render_to_string("rector/mail_liberar.html",{'postulantes':postulantes})
                    msg = EmailMultiAlternatives(subject=subject, from_email="postulaciones@bostoneduca.cl",
                        to=["ymartinez@bostoneduca.cl"], body=html_body)
                    msg.attach_alternative(html_body, "text/html")
                    msg.send()

            messages.success(request, 'Rúbrica creada')
            return redirect('rectores:entrevistas')
    else:
        form = Entrevistado(instance=postulantes)
        formset = RubricaCForm(instance=postulantes)
    return render(request, "rector/rubrica_coordinador.html",{'postulantes':postulantes, 'form':form,'formset':formset})


@login_required
@rector_required
def rubrica(request, pk):
    postulantes = get_object_or_404(Postulacion, pk=pk)
    rubrica = Rubrica.objects.filter(postulacion=postulantes)
    if request.method == 'POST':
        form = Entrevistado(request.POST, request.FILES, instance=postulantes)
        formset = RubricaForm(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                postulante = form.save(commit=False)
                postulante.entrevistado = True
                postulante.rector = request.user
                postulante.coordinador = True
                dias = form.cleaned_data.get('Días')
                rubrica = formset.save(commit=False)
                rubrica.postulacion = postulante
                rubrica.owner = request.user
                if rubrica.puntos == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos2 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos3 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos4 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos5 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos6 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos7 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos8 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos9 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos10 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')

                if rubrica.puntos == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos2 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos3 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos4 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos5 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos6 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos7 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos8 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos9 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos10 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')

                if rubrica.puntos + rubrica.puntos2 + rubrica.puntos3 + rubrica.puntos4 + rubrica.puntos5 + rubrica.puntos6 + rubrica.puntos7 + rubrica.puntos8 + rubrica.puntos9 + rubrica.puntos10 <= 20:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada el resultado es menos que 21 pts')
               
                if dias == 'menos15hrs' and postulantes.reemplazo== True :
                    postulante.menos15hrs = True
                    postulante.aprobar_demos = True
                    postulante.psicologa = True
                    subject = "Postulación reemplazo liberada"
                    html_body = render_to_string("rector/mail_liberar.html", {'postulantes':postulantes})
                    msg = EmailMultiAlternatives(subject=subject, from_email="postulaciones@bostoneduca.cl",
                        to=['ymartinez@bostoneduca.cl'], body=html_body)
                    msg.attach_alternative(html_body, "text/html")
                    msg.send()
                    
                else:
                    if dias == 'mas15hrs':
                        postulante.mas15hrs = True
                    else:
                        if postulante.reemplazo== False:
                            postulante.mas15hrs = False
                            postulante.menos15hrs = False
                postulante.save()
                rubrica.save()
            messages.success(request, 'Rúbrica generada')
            return redirect('rectores:entrevistas')
    else:
        form = Entrevistado(instance=postulantes)
        formset = RubricaForm(instance=postulantes)
    return render(request, "rector/rubrica.html",{'postulantes':postulantes, 'form':form,'formset':formset})


@login_required
@rector_required
def rubricaem(request, pk):
    postulantes = get_object_or_404(Postulacion, pk=pk)
    rubrica = Rubrica_equipomulti.objects.filter(postulacion=postulantes)
    if request.method == 'POST':
        form = Entrevistado(request.POST, request.FILES, instance=postulantes)
        formset = RubricaEmForm(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                postulante = form.save(commit=False)
                postulante.entrevistado = True
                postulante.coordinador = True
                postulante.rector = request.user
                rubrica = formset.save(commit=False)
                rubrica.postulacion = postulantes
                rubrica.owner = request.user
                if rubrica.puntos == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos2 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos3 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos4 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos5 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos6 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos7 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos8 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos9 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')

                if rubrica.puntos == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos2 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos3 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos4 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos5 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos6 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos7 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos8 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos9 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada puesto que ha evaluado con 0 o 1 en algún segmento.')

                if rubrica.puntos + rubrica.puntos2 + rubrica.puntos3 + rubrica.puntos4 + rubrica.puntos5 + rubrica.puntos6 + rubrica.puntos7 + rubrica.puntos8 + rubrica.puntos9 <= 20:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rúbrica rechazada el resultado es menos que 21 pts')

                if postulante.rechazar_rector == False:
                    subject = "Postulante entrevistado"

                    html_body = render_to_string("rector/mail_liberar.html",{'postulantes':postulantes})
                    msg = EmailMultiAlternatives(subject=subject, from_email="postulaciones@bostoneduca.cl",
                        to=["ymartinez@bostoneduca.cl"], body=html_body)
                    msg.attach_alternative(html_body, "text/html")
                    msg.send()
                postulante.save()
                rubrica.save()
            messages.success(request, 'Rúbrica creada')
            return redirect('rectores:entrevistas')
    else:
        form = Entrevistado(instance=postulantes)
        formset = RubricaEmForm(instance=postulantes)
    return render(request, "rector/rubrica_equipo.html",{'postulantes':postulantes, 'form':form,'formset':formset})


@login_required
@rector_required
def rubricademo(request, pk):
    postulantes = get_object_or_404(Postulacion, pk=pk)
    rubrica = Rubrica_demo.objects.filter(postulacion=postulantes)
    if request.method == 'POST':
        form = EntrevistadoDemo(request.POST, request.FILES, instance=postulantes)
        formset = RubricaDemoForm(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                postulante = form.save(commit=False)
                rubrica = formset.save(commit=False)
                rubrica.postulacion = postulantes
                rubrica.owner = request.user
                postulante.entrevistado_demo = True


                postulante.save()
                rubrica.save()
                if postulante.aprobar_demos == True and postulante.reemplazo ==True:

                    subject = "Potulación reemplazo liberada"
                    html_body = render_to_string("rector/reemplazos/correo.html", {'postulantes':postulantes})
                    msg = EmailMultiAlternatives(subject=subject, from_email="postulaciones@bostoneduca.cl",
                        to=['ymartinez@bostoneduca.cl'], body=html_body)
                    msg.attach_alternative(html_body, "text/html")
                    msg.send()
                else:
                    subject = "Postulación liberada"
                    html_body = render_to_string("rector/mail_liberar.html", {'postulantes':postulantes})
                    msg = EmailMultiAlternatives(subject=subject, from_email="postulaciones@bostoneduca.cl",
                        to=['yonyx.m.p@gmail.com'], body=html_body)
                    msg.attach_alternative(html_body, "text/html")
                    msg.send()
            messages.success(request, 'Rúbrica creada')
            return redirect('rectores:clasedemo')
    else:
        form = EntrevistadoDemo(instance=postulantes)
        formset = RubricaDemoForm(instance=postulantes)
    return render(request, "rector/rubrica_demo.html",{'postulantes':postulantes, 'form':form,'formset':formset})


@login_required
@rector_required
def vista_rubricaC(request, pk):
    rubrica =get_object_or_404(Rubrica_coordinador, pk=pk)
    puntos = Rubrica_coordinador.objects.filter(id=rubrica.pk).values('puntos','puntos2','puntos3','puntos4','puntos5','puntos6','puntos7').aggregate(suma=Sum('puntos') + Sum('puntos2') + Sum('puntos3') + Sum('puntos4') + Sum('puntos5') + Sum('puntos6') + Sum('puntos7'))

    return render(request, "rector/vista_rubrica_coordinador.html", {'rubrica':rubrica,'puntos':puntos})


@login_required
@rector_required
def vista_rubrica(request, pk):
    rubrica =get_object_or_404(Rubrica, pk=pk)
    total = 30
    puntos = Rubrica.objects.filter(id=rubrica.pk).values('puntos','puntos2','puntos3','puntos4','puntos5','puntos6','puntos7','puntos8','puntos9','puntos10').aggregate(suma=Sum('puntos') + Sum('puntos2') + Sum('puntos3') + Sum('puntos4') + Sum('puntos5') + Sum('puntos6') + Sum('puntos7') + Sum('puntos8') + Sum('puntos9') + Sum('puntos10'))
    return render(request, "rector/vista_rubrica.html", {'rubrica':rubrica,'puntos':puntos})


@login_required
@rector_required
def vista_rubrica_equipo(request, pk):
    rubrica =get_object_or_404(Rubrica_equipomulti, pk=pk)
    total = 30
    puntos = Rubrica_equipomulti.objects.filter(id=rubrica.pk).values('puntos','puntos2','puntos3','puntos4','puntos5','puntos6','puntos7','puntos8','puntos9').aggregate(suma=Sum('puntos') + Sum('puntos2') + Sum('puntos3') + Sum('puntos4') + Sum('puntos5') + Sum('puntos6') + Sum('puntos7') + Sum('puntos8') + Sum('puntos9') )
    return render(request, "rector/vista_rubrica_equipo.html", {'rubrica':rubrica,'puntos':puntos})

@login_required
@rector_required
def vista_rubrica_demo(request, pk):
    rubrica =get_object_or_404(Rubrica_demo, pk=pk)
    return render(request, "rector/vista_rubrica_demo.html", {'rubrica':rubrica})

@login_required
@rector_required
def vista_rubrica_psicologa(request, pk):
    rubrica =get_object_or_404(Rubrica_psicologa, pk=pk)
    return render(request, "rector/vista_rubrica_psicologa.html", {'rubrica':rubrica})

@login_required
@rector_required
def finalizados(request):
    usuario = request.user.rector
    colegio = usuario.colegio.all()[0]
    postulante = Postulacion.objects.filter(valido=True, entrevistado=True, rechazar=False, finalizado=True, email_send=False, liberar_2=False, liberar_3=False, reemplazo=False)
    postulante2 =  Postulacion.objects.filter(valido=True, entrevistado=True, rechazar=False, finalizado=True, email_send=False, liberar_2=True, liberar_3=False, reemplazo=False)
    postulante3 =  Postulacion.objects.filter(valido=True, entrevistado=True, rechazar=False, finalizado=True, email_send=False, liberar_2=True,liberar_3=True, reemplazo=False)

    return render(request, "rector/finalizado.html",{'postulante':postulante,'postulante2':postulante2,'postulante3':postulante3,'colegio':colegio})




@login_required
@rector_required
def send(request, pk):
    postulante = get_object_or_404(Postulacion, pk=pk)
    subject = "Postulación Rechazada"
    html_body = render_to_string("rector/mail.html", {'postulante':postulante})
    msg = EmailMultiAlternatives(subject=subject, from_email="postulaciones@bostoneduca.cl",
                                to=["ymartinez@bostoneduca.cl"], body=html_body)
    msg.attach_alternative(html_body, "text/html")
    msg.send()
    messages.success(request, 'Mensaje Enviado')

    return redirect('rectores:aprobados')


@login_required
@rector_required
def reportar(request, pk):
    postulantes = get_object_or_404(Postulacion, pk=pk)
    rector = request.user.rector

    if request.method == 'POST':
        form = Entrevistado(request.POST, request.FILES, instance=postulantes)
        if form.is_valid():
            with transaction.atomic():
                postulante = form.save(commit=False)
                postulante.email_send =True
                postulante.rector = request.user
                postulante.save()
                subject = "Estado de postulación"
                html_body = render_to_string("rector/mail.html", {'postulantes':postulantes})
                msg = EmailMultiAlternatives(subject=subject, from_email="postulaciones@bostoneduca.cl",
                    to=["ymartinez@bostoneduca.cl"], body=html_body)
                msg.attach_alternative(html_body, "text/html")
                msg.send()
            return redirect('rectores:rechazados')
    else:
        form = Entrevistado(instance=postulantes)
    return render(request, "rector/reportar_rechazado.html",{'postulantes':postulantes, 'form':form})


@login_required
@rector_required
def subirficha(request, pk):
    postulantes = get_object_or_404(Postulacion, pk=pk)
    rector = request.user.rector

    if request.method == 'POST':
        form = FichaFatForm(request.POST, request.FILES, instance=postulantes)
        if form.is_valid():
            with transaction.atomic():
                postulante = form.save(commit=False)
                postulante.rector = request.user
                postulante.send =True
                postulante.fecha_fat = datetime.now()
                postulante.save()
                subject = "Ficha FAT"
                html_body = render_to_string("rector/mail_2.html", {'postulantes':postulantes})
                msg = EmailMultiAlternatives(subject=subject, from_email="postulaciones@bostoneduca.cl",
                    to=["ymartinez@bostoneduca.cl"], body=html_body)
                msg.attach_alternative(html_body, "text/html")
                msg.send()
            messages.success(request, 'Mensaje enviado')
            return redirect('rectores:rechazados')
    else:
        form = FichaFatForm(instance=postulantes)
    return render(request, "rector/subir_ficha.html",{'postulantes':postulantes, 'form':form, 'rector':rector})


@login_required
@rector_required
def oferta_view(request):
    usuario = request.user.rector
    colegio = usuario.colegio.all()[0]
    postulantes = Postulacion.objects.filter(Siguiente=True, entrevistado=True,  rechazar_rector=False,psicologa=True,rechazada=False,finalizado=False, liberar_2=False, liberar_3=False)
    postulantes2 = Postulacion.objects.filter(Siguiente=True, entrevistado=True,  rechazar_rector=False,psicologa=True,rechazada=False,finalizado=False, liberar_2=True, liberar_3=False)
    postulantes3 = Postulacion.objects.filter(Siguiente=True, entrevistado=True,  rechazar_rector=False,psicologa=True,rechazada=False,finalizado=False, liberar_2=True,liberar_3=True)

    return render(request, "rector/oferta_view.html",{'postulantes':postulantes, 'postulantes2':postulantes2, 'postulantes3':postulantes3, 'colegio':colegio})

@login_required
@rector_required
def oferta(request, pk):
    postulantes = get_object_or_404(Postulacion, pk=pk)
    if request.method == 'POST':
        form = Oferta(request.POST, request.FILES, instance=postulantes)
        if form.is_valid():
            with transaction.atomic():
                postulante = form.save(commit=False)
                postulante.fecha_oferta = datetime.now()

                postulante.save()
                form.save()
            return redirect('rectores:oferta_view')
    else:
        form = Oferta(instance=postulantes)
    return render(request, "rector/oferta_laboral.html",{'postulantes':postulantes, 'form':form})

@method_decorator([login_required, rector_required] , name='dispatch')
class PostulanteDeleteView(DeleteView):
    model = Postulacion
    template_name = 'rector/eliminar.html'
    success_url = reverse_lazy('rectores:index')

    def delete(self, request, *args, **kwargs):
        postulante = self.get_object()
        messages.success(request, 'La postulación fue borrada')
        return super().delete(request, *args, **kwargs)



@login_required
@rector_required
def finalizadosr(request):
    postulante = Postulacion.objects.filter(valido=True, entrevistado=True, rechazar=False, finalizado=True, aceptada = True, reemplazo=True).order_by('id')

    return render(request, "rector/reemplazos/finalizados_r.html",{'postulante':postulante})

@login_required
@rector_required
def editar_r(request, pk):
    postulantes = get_object_or_404(Postulacion, pk=pk)
    if request.method == 'POST':
        form = Editar_r(request.POST, request.FILES, instance=postulantes)
        if form.is_valid():
            with transaction.atomic():
                dias = form.cleaned_data.get('Días')
    
                if dias == 'fijo':
                    postulantes.fijo = True
                    postulantes.finalizado= False 
                    postulantes.aceptada = False 
                    postulantes.reemplazo= False
                    postulantes.menos15hrs= False
                    postulantes.mas15hrs= False
                    postulantes.carta_oferta_recibida= False
                    postulantes.liberar_coordinador= False
                    postulantes.psicologa= False
                    postulantes.psicologa1= False
                    postulantes.psicologa2= False
                    postulantes.send= False
                    postulantes.aceptar_ficha= False

                else:
                    if dias == 'mas15hrs':
                        postulantes.fijo = False
                        postulantes.finalizado= False 
                        postulantes.aceptada = False 
                        postulantes.reemplazo= True
                        postulantes.menos15hrs= False
                        postulantes.mas15hrs= True
                        postulantes.carta_oferta_recibida= False
                        postulantes.liberar_coordinador= False
                        postulantes.psicologa= False
                        postulantes.psicologa1= False
                        postulantes.psicologa2= False
                        postulantes.send= False
                        postulantes.aceptar_ficha= False

                postulante = form.save(commit=False)
                postulante.save()
                return redirect('rectores:aprobados')
    else:
        form = Editar_r(instance=postulantes)
    return render(request, "rector/reemplazos/editar.html",{'postulantes':postulantes, 'form':form})
