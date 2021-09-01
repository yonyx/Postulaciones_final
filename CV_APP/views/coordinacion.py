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
from ..decorators import coordinacion_required

from CV_APP.models import Coordinacion2, Rubrica_demo, Rubrica_equipomulti, Años, Cargo, Colegios, Disposicion, Postulacion ,User, Rubrica_coordinador, Rubrica, Rubrica_psicologa
from CV_APP.forms import Finalizar, Editar_r,CoordinadorSignUpForm2,PostulacionForm, Postulantes, CoordinadorSignUpForm, RubricaCForm,Entrevistado, Liberar_c, Liberar_em


class CoordinadorSignUpView(CreateView):
    model = User
    form_class = CoordinadorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Coordinador'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('coordinacion:index')


class CoordinadorSignUpView2(CreateView):
    model = User
    form_class = CoordinadorSignUpForm2
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Coordinador2'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('coordinacion:index')

#administrativo
@login_required
@coordinacion_required
def index_admin(request):
    postulante = Postulacion.objects.filter(valido=True, rechazar_index=False ,rechazar=False, rechazar_rector=False, rechazar_demos = False, send = False, cargo=11).order_by('id')
    return render(request, "coordinacion/Administrativos/index.html", {'postulante':postulante})

@login_required
@coordinacion_required
def psicolaboral_admin(request):
    postulante = Postulacion.objects.filter(entrevistado=True, rechazar_rector=False, rechazar=False, aceptada=False, rechazada=False).order_by('id')
    return render(request, "coordinacion/Administrativos/liberar.html", {'postulante':postulante})

@login_required
@coordinacion_required
def carta_oferta_admin(request):
    postulante = Postulacion.objects.filter(send = True, finalizado = False, rechazada=False,rechazar_coordinador=False, aceptar_ficha=True).order_by('id')

    return render(request, "coordinacion/Administrativos/carta_oferta.html",{'postulante':postulante})

#fin administrativo

#auxiliar
@login_required
@coordinacion_required
def index_aux(request):
    postulante = Postulacion.objects.filter(valido=True, rechazar_index=False ,rechazar=False, rechazar_rector=False, rechazar_demos = False, send = False, cargo=12).order_by('id')
    return render(request, "coordinacion/Auxiliares/index.html", {'postulante':postulante})


#fin auxiliar

#equipo multidiciplinario
@login_required
@coordinacion_required
def index_equipomulti(request):
    postulante = Postulacion.objects.filter(valido=False,rechazar=False,rechazar_coordinador=False, cargo=7).order_by('id')
    return render(request, "coordinacion/equipomulti/equipo_multi.html", {'postulante':postulante})


@login_required
@coordinacion_required
def estado_em(request):
    postulante = Postulacion.objects.filter(valido=True, rechazar_index=False ,rechazar=False, rechazar_rector=False, rechazar_demos = False, send = False).order_by('id')
    return render(request, "coordinacion/equipomulti/entrevistar.html", {'postulante':postulante})

@login_required
@coordinacion_required
def psicolaboral_em(request):
    postulante = Postulacion.objects.filter(entrevistado=True, rechazar_rector=False, rechazar=False, aceptada=False, rechazada=False).order_by('id')
    return render(request, "coordinacion/equipomulti/liberar.html", {'postulante':postulante})

@login_required
@coordinacion_required
def finalizados_em(request):
    postulante = Postulacion.objects.filter(valido=True, entrevistado=True, rechazar=False, finalizado=True).order_by('id')

    return render(request, "coordinacion/equipomulti/finalizados.html",{'postulante':postulante})


@login_required
@coordinacion_required
def carta_oferta_em(request):
    postulante = Postulacion.objects.filter(send = True, finalizado = False, rechazada=False,rechazar_coordinador=False, aceptar_ficha=True).order_by('id')

    return render(request, "coordinacion/equipomulti/carta_oferta.html",{'postulante':postulante})


#fin equipo multi


#coordinadores
@login_required
@coordinacion_required
def index_c(request):
    postulante = Postulacion.objects.filter(valido=False,rechazar=False,rechazar_coordinador=False, cargo=6).order_by('id')
    return render(request, "coordinacion/coordinadores/coordinadores.html", {'postulante':postulante})


@login_required
@coordinacion_required
def entrevistar_c(request):
    postulante = Postulacion.objects.filter(valido=True, rechazar_index=False ,rechazar=False, rechazar_rector=False, rechazar_demos = False, send = False).order_by('id')
    return render(request, "coordinacion/coordinadores/entrevistar.html", {'postulante':postulante})

@login_required
@coordinacion_required
def psicolaboral_c(request):
    postulante = Postulacion.objects.filter(entrevistado=True,psicologa=False,rechazar_rector=False, rechazar_demos = False, aceptada=False,rechazar=False).order_by('id')
    return render(request, "coordinacion/coordinadores/psicolaboral_c.html", {'postulante':postulante})

@login_required
@coordinacion_required
def finalizados_c(request):
    postulante = Postulacion.objects.filter(valido=True, entrevistado=True, rechazar=False, finalizado=True).order_by('id')

    return render(request, "coordinacion/coordinadores/finalizados.html",{'postulante':postulante})

@login_required
@coordinacion_required
def carta_oferta_c(request):
    postulante = Postulacion.objects.filter(send = True, finalizado = False, rechazada=False,rechazar_coordinador=False, aceptar_ficha=True).order_by('id')

    return render(request, "coordinacion/coordinadores/carta_oferta.html",{'postulante':postulante})

#fin coordinacion

@login_required
@coordinacion_required
def rechazados(request):
    postulante = Postulacion.objects.all().order_by('id')
    return render(request, "coordinacion/rechazados/rechazados.html", {'postulante':postulante})
#Docentes
@login_required
@coordinacion_required
def index(request):
    postulante = Postulacion.objects.filter(valido=False,rechazar=False, rechazar_coordinador=False,).order_by('id')
    return render(request, "coordinacion/index.html", {'postulante':postulante})

@login_required
@coordinacion_required
def activos(request):
    postulante = Postulacion.objects.filter(valido=True, Siguiente=False).order_by('id')
    return render(request, "coordinacion/activos.html", {'postulante':postulante})

@login_required
@coordinacion_required
def proceso(request):
    postulante = Postulacion.objects.filter(valido=True, rechazar_index=False ,rechazar=False, rechazar_rector=False, rechazar_demos = False, send = False).order_by('-enviada')
    return render(request, "coordinacion/proceso.html", {'postulante':postulante,})

@login_required
@coordinacion_required
def psicolaboral(request):
    postulante = Postulacion.objects.filter(valido=True, entrevistado=True, rechazar=False,rechazar_rector=False, aprobar_demos=True, aceptada=False, coordinador=True).order_by('id')
    return render(request, "coordinacion/psicolaboral.html", {'postulante':postulante})






@login_required
@coordinacion_required
def finalizados(request):
    postulante = Postulacion.objects.filter(valido=True, entrevistado=True, rechazar=False, finalizado=True, aceptada = True, reemplazo=False,).order_by('id')

    return render(request, "coordinacion/finalizado.html",{'postulante':postulante})


@login_required
@coordinacion_required
def finalizadosr(request):
    postulante = Postulacion.objects.filter(valido=True, entrevistado=True, rechazar=False, finalizado=True, aceptada = True, reemplazo=True).order_by('id')

    return render(request, "coordinacion/Remplazos/finalizados_r.html",{'postulante':postulante})



@login_required
@coordinacion_required
def liberar_c(request, pk):
    postulantes = get_object_or_404(Postulacion, pk=pk)
    if request.method == 'POST':
        form = Liberar_c(request.POST, request.FILES, instance=postulantes)
        if form.is_valid():
            with transaction.atomic():
                postulante = form.save(commit=False)
                postulante.save()
                if postulante.psicologa1 == True:
                    subject = "Postulación liberada"
                    html_body = render_to_string("coordinacion/mail.html", {'postulantes':postulantes})
                    msg = EmailMultiAlternatives(subject=subject, from_email="postulaciones@bostoneduca.cl",
                        to=['yonyx.m.p@gmail.com'], body=html_body)
                    msg.attach_alternative(html_body, "text/html")
                    msg.send()
                else:
                    if postulante.psicologa2 == True:
                        subject = "Postulación liberada"
                        html_body = render_to_string("coordinacion/mail.html", {'postulantes':postulantes})
                        msg = EmailMultiAlternatives(subject=subject, from_email="postulaciones@bostoneduca.cl",
                            to=['yonyx.m.p@gmail.com'], body=html_body)
                        msg.attach_alternative(html_body, "text/html")
                        msg.send()
            if postulante.cargo.id == 6:
                return redirect('coordinacion:psicolaboral_c')
            else:
                if postulante.cargo.id == 7:
                    return redirect('coordinacion:psicolaboral_em')
                else:
                    return redirect('coordinacion:psicolaboral')
    else:
        form = Liberar_c(instance=postulantes)
    return render(request, "coordinacion/liberar.html",{'postulantes':postulantes, 'form':form})



@login_required
@coordinacion_required
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
                if postulante.cargo.id == 6:
                    return redirect('coordinacion:psicolaboral_c')
                else:
                    if postulante.cargo.id == 7:
                        return redirect('coordinacion:psicolaboral_em')
                    else:
                        return redirect('coordinacion:psicolaboral')
    else:
        form = Editar_r(instance=postulantes)
    return render(request, "coordinacion/Remplazos/editar.html",{'postulantes':postulantes, 'form':form})



@login_required
@coordinacion_required
def info(request, pk):
    postulante = get_object_or_404(Postulacion, pk=pk)
    if request.method == 'POST':
        form = Postulantes(request.POST, request.FILES, instance=postulante)
        if form.is_valid():
            with transaction.atomic():
                form.save()

            messages.success(request, 'Postulacion Aceptada')
            if postulante.cargo.id == 6:
                return redirect('coordinacion:coordinadores')
            else:
                if postulante.cargo.id == 7:
                    return redirect('coordinacion:equipo_multi')
                else:
                    return redirect('coordinacion:proceso')
    else:
        form = Postulantes(instance=postulante)
    return render(request, "coordinacion/info.html",{'postulante':postulante,'form':form})

@method_decorator([login_required, coordinacion_required] , name='dispatch')
class PostulanteDeleteView(DeleteView):
    model = Postulacion
    template_name = 'coordinacion/eliminar.html'
    success_url = reverse_lazy('coordinacion:index')

    def delete(self, request, *args, **kwargs):
        postulante = self.get_object()
        messages.success(request, 'La postulación fue borrada')
        return super().delete(request, *args, **kwargs)

@login_required
@coordinacion_required
def rubrica(request, pk):
    postulantes = get_object_or_404(Postulacion, pk=pk)
    rubrica = Rubrica_coordinador.objects.filter(postulacion=postulantes)
    if request.method == 'POST':
        form = Entrevistado(request.POST, request.FILES, instance=postulantes)
        formset = RubricaCForm(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                postulante = form.save(commit=False)
                postulante.entrevistado = True
                rubrica = formset.save(commit=False)
                rubrica.owner = request.user

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
                    messages.success(request, 'Rubrica rechazada puesto que ah evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos7 == 1:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rubrica rechazada puesto que ah evaluado con 0 o 1 en algún segmento.')

                if rubrica.puntos == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rubrica rechazada puesto que ah evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos2 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rubrica rechazada puesto que ah evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos3 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rubrica rechazada puesto que ah evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos4 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rubrica rechazada puesto que ah evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos5 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rubrica rechazada puesto que ah evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos6 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rubrica rechazada puesto que ah evaluado con 0 o 1 en algún segmento.')
                if rubrica.puntos7 == 0:
                    postulante.rechazar_rector = True
                    messages.success(request, 'Rubrica rechazada puesto que ah evaluado con 0 o 1 en algún segmento.')

                if rubrica.puntos + rubrica.puntos2 + rubrica.puntos3 + rubrica.puntos4 + rubrica.puntos5 + rubrica.puntos6 + rubrica.puntos7 <= 15:
                    postulantes.rechazar_coordinador = True
                    messages.success(request, 'Rubrica rechazada el resultado es menos que 15 pts')

                postulante.save()
                rubrica.save()
            messages.success(request, 'Rúbrica creada')
            return redirect('coordinacion:psicolaboral_c')
    else:
        form = Entrevistado(instance=postulantes)
        formset = RubricaCForm(instance=postulantes)
    return render(request, "coordinacion/coordinadores/rubrica_coordinador.html",{'postulantes':postulantes, 'form':form,'formset':formset})

@login_required
@coordinacion_required
def vista_rubricaC(request, pk):
    rubrica =get_object_or_404(Rubrica_coordinador, pk=pk)
    puntos = Rubrica_coordinador.objects.filter(id=rubrica.pk).values('puntos','puntos2','puntos3','puntos4','puntos5','puntos6','puntos7').aggregate(suma=Sum('puntos') + Sum('puntos2') + Sum('puntos3') + Sum('puntos4') + Sum('puntos5') + Sum('puntos6') + Sum('puntos7'))

    return render(request, "coordinacion/coordinadores/vista_rubrica_coordinador.html", {'rubrica':rubrica,'puntos':puntos})

@login_required
@coordinacion_required
def vista_rubrica(request, pk):
    rubrica =get_object_or_404(Rubrica, pk=pk)
    puntos = Rubrica.objects.filter(id=rubrica.pk).values('puntos','puntos2','puntos3','puntos4','puntos5','puntos6','puntos7','puntos8','puntos9','puntos10').aggregate(suma=Sum('puntos') + Sum('puntos2') + Sum('puntos3') + Sum('puntos4') + Sum('puntos5') + Sum('puntos6') + Sum('puntos7') + Sum('puntos8') + Sum('puntos9') + Sum('puntos10'))

    return render(request, "coordinacion/rubrica_rector.html", {'rubrica':rubrica,'puntos':puntos})

@login_required
@coordinacion_required
def vista_rubrica_equipo(request, pk):
    rubrica =get_object_or_404(Rubrica_equipomulti, pk=pk)
    total = 30
    puntos = Rubrica_equipomulti.objects.filter(id=rubrica.pk).values('puntos','puntos2','puntos3','puntos4','puntos5','puntos6','puntos7','puntos8','puntos9').aggregate(suma=Sum('puntos') + Sum('puntos2') + Sum('puntos3') + Sum('puntos4') + Sum('puntos5') + Sum('puntos6') + Sum('puntos7') + Sum('puntos8') + Sum('puntos9') )
    return render(request, "coordinacion/rubrica_equipo.html", {'rubrica':rubrica,'puntos':puntos})

@login_required
@coordinacion_required
def vista_rubrica_demo(request, pk):
    rubrica =get_object_or_404(Rubrica_demo, pk=pk)
    return render(request, "coordinacion/vista_rubrica_demo.html", {'rubrica':rubrica})

@login_required
@coordinacion_required
def vista_rubrica_psicologa(request, pk):
    rubrica =get_object_or_404(Rubrica_psicologa, pk=pk)
    return render(request, "coordinacion/vista_rubrica_psicologa.html", {'rubrica':rubrica})

@login_required
@coordinacion_required
def rubricas(request, pk):
    postulacion = get_object_or_404(Postulacion, pk=pk)
    postulantes = Rubrica.objects.filter(postulacion__id = postulacion.id)
    postulante_demo = Rubrica_demo.objects.filter(postulacion__id = postulacion.id)
    postulante_em = Rubrica_equipomulti.objects.filter(postulacion__id = postulacion.id)
    postulante_psicologa = Rubrica_psicologa.objects.filter(postulantes__id = postulacion.id)
    postulante_c = Rubrica_coordinador.objects.filter(postulacion__id = postulacion.id)
    return render(request, "coordinacion/rubricas.html",{'postulantes':postulantes,'postulacion':postulacion,'postulante_demo':postulante_demo,'postulante_em':postulante_em,'postulante_psicologa':postulante_psicologa,'postulante_c':postulante_c,})

@login_required
@coordinacion_required
def carta_oferta(request):
    postulante = Postulacion.objects.filter(send = True, finalizado = False, rechazada=False,rechazar_coordinador=False, aceptar_ficha=True).order_by('id')

    return render(request, "coordinacion/carta_oferta.html",{'postulante':postulante})



@login_required
@coordinacion_required
def finalizar(request, pk):
    postulantes = get_object_or_404(Postulacion, pk=pk)
    if request.method == 'POST':
        form = Finalizar(request.POST, request.FILES, instance=postulantes)
        if form.is_valid():
            with transaction.atomic():
                postulante = form.save(commit=False)
                postulante.save()

                subject = "Postulación finalizada"
                html_body = render_to_string("coordinacion/mail_finalizado.html", {'postulantes':postulantes})
                msg = EmailMultiAlternatives(subject=subject, from_email="postulaciones@bostoneduca.cl",
                    to=['yonyx.m.p@gmail.com'], cc=['ymartinez@bostoneduca.cl','yonyx.m.p@gmail.com'],body=html_body)
                msg.attach_alternative(html_body, "text/html")
                msg.send()
            if postulante.cargo.id == 6:
                return redirect('coordinacion:ficha_fat_c')
            else:
                if postulante.cargo.id == 7:
                    return redirect('coordinacion:ficha_fat_em')
                else:
                    return redirect('coordinacion:ficha_fat')
    else:
        form = Finalizar(instance=postulantes)
    return render(request, "coordinacion/carta_oferta_view.html",{'postulantes':postulantes, 'form':form})