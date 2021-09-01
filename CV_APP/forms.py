from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.forms.widgets import RadioSelect, Textarea, DateInput, DateTimeBaseInput, DateTimeInput, CheckboxInput
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from CV_APP.models import (opcion,Coordinacion2,Criterios,Rubrica_demo,Rubrica_equipomulti,Rubrica_coordinador,Años, Cargo, Titulo, Colegios, Disposicion, Postulacion, User, Rubrica, Rubrica_psicologa, Coordinacion, Rector,Nivel_ingles, Nivel_Tec, Psicologa)
from django.utils.safestring import mark_safe


class CoordinadorSignUpForm2(UserCreationForm):

    colegio = forms.ModelMultipleChoiceField(
        queryset=Colegios.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    es_coordinador = forms.BooleanField(required=False, widget=forms.CheckboxInput, label='Coordinador')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)


    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("El correo ya está registrado.")
        return email


    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]
        labels = {
            'first_name':'Nombre',
            'last_name':'Apellido',
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_coordinacion2 = True
        user.username = user.email
        user.save()
        coordinador = Coordinacion2.objects.create(user=user)
        coordinador.colegio.add(*self.cleaned_data.get('colegio'))
        coordinador.email = self.cleaned_data["email"]
        coordinador.password1 = self.cleaned_data["password1"]

        return user

class CoordinadorSignUpForm(UserCreationForm):

    colegio = forms.ModelMultipleChoiceField(
        queryset=Colegios.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    email = forms.EmailField(label="Correo Institucional", required=True, help_text="Debe ingresar el correo dado por la fundación o el colegio.")
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)


    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("El correo ya está registrado.")
        return email


    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]
        labels = {
            'first_name':'Nombre',
            'last_name':'Apellido',
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_coordinacion = True
        user.username = user.email
        user.save()
        coordinador = Coordinacion.objects.create(user=user)
        coordinador.colegio.add(*self.cleaned_data.get('colegio'))
        coordinador.email = self.cleaned_data["email"]
        coordinador.password1 = self.cleaned_data["password1"]

        return user

class RectorSignUpForm(UserCreationForm):

    colegio = forms.ModelMultipleChoiceField(
        queryset=Colegios.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    email = forms.EmailField(label="Correo Institucional", required=True, help_text="Debe ingresar el correo dado por la fundación o el colegio.")
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)


    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("El correo ya está registrado.")
        return email


    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'

        ]
        labels = {
            'first_name':'Nombre',
            'last_name':'Apellido',
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_rector = True
        user.username = user.email
        user.save()
        rector = Rector.objects.create(user=user)
        rector.colegio.add(*self.cleaned_data.get('colegio'))
        rector.email = self.cleaned_data["email"]
        rector.password1 = user.password

        return user

class PsicologaSignUpForm(UserCreationForm):

    colegio = forms.ModelMultipleChoiceField(
        queryset=Colegios.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    email = forms.EmailField(label="Correo Institucional", required=True, help_text="Debe ingresar el correo dado por la fundación o el colegio.")
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)


    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("El correo ya está registrado.")
        return email


    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]
        labels = {
            'first_name':'Nombre',
            'last_name':'Apellido',
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_psicologa = True
        user.username = user.email
        user.save()
        psicologa = Psicologa.objects.create(user=user)
        psicologa.colegio.add(*self.cleaned_data.get('colegio'))
        psicologa.email = self.cleaned_data["email"]
        psicologa.password1 = self.cleaned_data["password1"]
        return user

class PostulacionForm(forms.ModelForm):

    disponibilidad = forms.ModelMultipleChoiceField(
        queryset=Disposicion.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    nivel_tec = forms.ModelMultipleChoiceField(
        queryset=Nivel_Tec.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Dominio de herramientas tecnológicas'
    )


    class Meta:
        model = Postulacion
        fields = ('nombre','apellido_p','apellido_m','rut','telefono','email','cargo','colegio1','colegio2','colegio3','disponibilidad','nivel_ingles','titulo','años','cv','otros_documentos','nivel_ingles','nivel_tec','nombre_r','cargo_r','corre_r','telefono_r','relacion_r','instituto_r','nombre_r_2','cargo_r_2','corre_r_2','telefono_r_2','relacion_r_2','instituto_r_2')

    def __init__(self ,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].queryset = Titulo.objects.none()

        if 'cargo' in self.data:
            try:
                cargo_id = int(self.data.get('cargo'))
                self.fields['titulo'].queryset = Titulo.objects.filter(cargo__id=cargo_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['titulo'].queryset = self.instance.cargo.titulo_set

class Postulantes(forms.ModelForm):

    class Meta:
        model = Postulacion
        fields = ('valido','entrevistado','rechazar_coordinador',)

class PostulantesRector(forms.ModelForm):

    class Meta:
        model = Postulacion
        fields = ('Siguiente','liberar_2','liberar_3','rechazar_index')

class PostulantesRectorLiberar(forms.ModelForm):

    class Meta:
        model = Postulacion
        fields = ('liberar_2','liberar_3','rechazar_index',)

class Entrevistado(forms.ModelForm):
    CHOICES=[('menos15hrs','Menos 15 días'),
             ('mas15hrs','Más 15 días')]
    Días=forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    class Meta:
        model = Postulacion
        fields = ('entrevistado','email_send','rechazar_rector','reemplazo',)


class FichaFatForm(forms.ModelForm):

    class Meta:
        model = Postulacion
        fields = ('ficha_fat','send',)

class EntrevistadoDemo(forms.ModelForm):

    class Meta:
        model = Postulacion
        fields = ('aprobar_demos','rechazar_demos','entrevistado_demo',)


class Oferta(forms.ModelForm):

    class Meta:
        model = Postulacion
        fields = ('aceptada','rechazada','liberar_2','carta_oferta',)

class Finalizar(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = ('finalizado',)

class Aceptar_fat(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = ('aceptar_ficha',)

class Liberar_c(forms.ModelForm):

    class Meta:
        model = Postulacion
        fields = ('liberar_coordinador','psicologa1','psicologa2','coordinador_entrevisto','observaciones_c')


class Editar_r(forms.ModelForm):
    CHOICES=[('fijo','Fijo'),
             ('mas15hrs','Más 15 días')]
    Días=forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    class Meta:
        model = Postulacion
        fields = ('fijo','mas15hrs',)


class Liberar_em(forms.ModelForm):

    class Meta:
        model = Postulacion
        fields = ('liberar_equipomulti',)

class RubricaForm(forms.ModelForm):
    opcion = forms.ModelChoiceField(
        queryset=opcion.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    class Meta:
        model = Rubrica
        fields = ('puntos','puntos2','puntos3','puntos4','puntos5','puntos6','puntos7','puntos8','puntos9','puntos10','comentario','comentario2','comentario3','comentario4','comentario5','comentario6','comentario7','comentario8','comentario9','comentario10','observaciones','cargop','niveles','opcion','Nombre_referencia_y_cargo_actual','Relación_laboral_con_postulante','cometarios_referencias','renumeracion','horas',)

class RubricaCForm(forms.ModelForm):
    opcion = forms.ModelChoiceField(
        queryset=opcion.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    class Meta:
        model = Rubrica_coordinador
        fields = ('puntos','puntos2','puntos3','puntos4','puntos5','puntos6','puntos7','comentario','comentario2','comentario3','comentario4','comentario5','comentario6','comentario7','observaciones','cargop','niveles','opcion','Nombre_referencia_y_cargo_actual','Relación_laboral_con_postulante','cometarios_referencias','renumeracion','horas')

class RubricaEmForm(forms.ModelForm):
    opcion = forms.ModelChoiceField(
        queryset=opcion.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    class Meta:
        model = Rubrica_equipomulti
        fields = ('rechazar','puntos','puntos2','puntos3','puntos4','puntos5','puntos6','puntos7','puntos8','puntos9','comentario','comentario2','comentario3','comentario4','comentario5','comentario6','comentario7','comentario8','comentario9','observaciones','cargop','niveles','opcion','cometarios_referencias','Nombre_referencia_y_cargo_actual','Relación_laboral_con_postulante','renumeracion','horas')


class Aprobado(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = ('psicologa','rechazar')

OPCIONES =(
    ("1", "Bajo lo esperado"),
    ("2","Adecuado"),
    ("3","Sobre lo esperado")
)

class Psicologa(forms.ModelForm):

    class Meta:
        model = Rubrica_psicologa
        fields = ("aspecto","aspecto_2","competencia_1","competencia_2","competencia_3","competencia_4","competencia_5","competencia_6","competencia_7","competencia_8","competencia_9","competencia_10","competencia_11","competencia_12","competencia_13","competencia_14","competencia_15","competencia_16","competencia_17","competencia_18","competencia_19","fortalezas","fortalezas2","fortalezas3","posibilidades","posibilidades2","posibilidades3","sugerencias","conclusion")



class RubricaDemoForm(forms.ModelForm):
    criterio_1 = forms.ModelChoiceField(
        queryset=Criterios.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    criterio_2 = forms.ModelChoiceField(
        queryset=Criterios.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    criterio_3 = forms.ModelChoiceField(
        queryset=Criterios.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    criterio_4 = forms.ModelChoiceField(
        queryset=Criterios.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    criterio_5 = forms.ModelChoiceField(
        queryset=Criterios.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)

    criterio_6 = forms.ModelChoiceField(
        queryset=Criterios.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    criterio_7 = forms.ModelChoiceField(
        queryset=Criterios.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    criterio_8 = forms.ModelChoiceField(
        queryset=Criterios.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    criterio_9 = forms.ModelChoiceField(
        queryset=Criterios.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    criterio_10 = forms.ModelChoiceField(
        queryset=Criterios.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    criterio_11 = forms.ModelChoiceField(
        queryset=Criterios.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    criterio_12 = forms.ModelChoiceField(
        queryset=Criterios.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    criterio_13 = forms.ModelChoiceField(
        queryset=Criterios.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    criterio_14 = forms.ModelChoiceField(
        queryset=Criterios.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    criterio_15 = forms.ModelChoiceField(
        queryset=Criterios.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    criterio_16 = forms.ModelChoiceField(
        queryset=Criterios.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    criterio_17 = forms.ModelChoiceField(
        queryset=Criterios.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    criterio_18 = forms.ModelChoiceField(
        queryset=Criterios.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)
    criterio_19 = forms.ModelChoiceField(
        queryset=Criterios.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
        label='',
        required=True,
        empty_label=None)

    class Meta:
        model = Rubrica_demo
        fields = ("criterio_1","criterio_2","criterio_3","criterio_4","criterio_5","criterio_6","criterio_7","criterio_8","criterio_9","criterio_10","criterio_11","criterio_12","criterio_13","criterio_14","criterio_15","criterio_16","criterio_17","criterio_18","criterio_19","observaciones",)

