import sys
import math
import random
from io import BytesIO
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from model_utils.managers import InheritanceManager
from django.utils.timezone import utc
from .validators import validate_file_extension
from django.core.validators import MinLengthValidator

# Create your models here..


class User(AbstractUser):
    is_administrador = models.BooleanField(default=False)
    is_coordinacion = models.BooleanField(default=False)
    is_coordinacion2 = models.BooleanField(default=False)
    is_rector = models.BooleanField(default=False)
    is_psicologa = models.BooleanField(default=False)
    is_monica = models.BooleanField(default=False)


class Aspectos_generales(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Competencias(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Criterios(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Comuna(models.Model):
    region = models.ForeignKey(Region,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


def colegios_images(instance, filename):
    return 'UserImages/user_{0}/{1}'.format(instance.user.id, filename)

class Colegios(models.Model):
    name = models.CharField(max_length=250)
    imagen = models.ImageField( null = True, upload_to='colegios_images',default=False, blank=True,verbose_name=('Imagen'), unique=True)

    def __str__(self):
        return self.name

class Colegios2(models.Model):
    name = models.CharField(max_length=250)
    imagen = models.ImageField( null = True, upload_to='colegios_images',default=False, blank=True,verbose_name=('Imagen'), unique=True)

    def __str__(self):
        return self.name

class Colegios3(models.Model):
    name = models.CharField(max_length=250)
    imagen = models.ImageField( null = True, upload_to='colegios_images',default=False, blank=True,verbose_name=('Imagen'), unique=True)

    def __str__(self):
        return self.name

class Cargo(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Disposicion(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Titulo(models.Model):
    name = models.CharField(max_length=250)
    cargo = models.ManyToManyField(Cargo, related_name='Titulo_cargo', null=True, blank=True, verbose_name=('cargo'))
    def __str__(self):
        return self.name

class Ingles(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Años(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Nivel_ingles(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Nivel_Tec(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class opcion(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Coordinacion2(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    colegio = models.ManyToManyField(Colegios, related_name='colegio_coordinacion2', blank=True)

    def __str__(self):
        return self.user.first_name

class Coordinacion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    colegio = models.ManyToManyField(Colegios, related_name='colegio_coordinacion', blank=True)

    def __str__(self):
        return self.user.first_name

class Rector(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    colegio = models.ManyToManyField(Colegios, related_name='colegio_rector', blank=True)
    def __str__(self):
        return self.user.first_name

class Monica(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    colegio = models.ManyToManyField(Colegios, related_name='colegio_monica', blank=True)
    def __str__(self):
        return self.user.first_name

class Psicologa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    colegio = models.ManyToManyField(Colegios, related_name='colegio_psicologa', blank=True)
    psicologa1 = models.BooleanField(null= False,default=False, verbose_name=("Psicologa1"))
    psicologa2 = models.BooleanField(null= False,default=False, verbose_name=("Psicologa2"))
    def __str__(self):
        return self.user.first_name

class Postulacion(models.Model):
   nombre = models.CharField(max_length=250)
   apellido_p = models.CharField(max_length=250, verbose_name=('Apellido Paterno'))
   apellido_m = models.CharField(max_length=250, verbose_name=('Apellido Materno'))
   rut = models.CharField(max_length=250, validators=[MinLengthValidator(8)])
   telefono = models.CharField(max_length=250, verbose_name=('Teléfono'), help_text=("El formato debe ser el siguiente +569xxxxxxxx"))
   email = models.EmailField(verbose_name=("Correo"))
   cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, help_text='Cargo al que postula')
   colegio1 = models.ForeignKey(Colegios, on_delete=models.CASCADE,related_name='colegio1' ,help_text=('Colegio al que postula'), verbose_name=('Preferencia 1'))
   colegio2 = models.ForeignKey(Colegios, on_delete=models.CASCADE,related_name='colegio2', help_text=('Colegio al que postula'), verbose_name=('Preferencia 2'), null=True, blank=True)
   colegio3 = models.ForeignKey(Colegios, on_delete=models.CASCADE,related_name='colegio3' ,help_text=('Colegio al que postula'), verbose_name=('Preferencia 3'), null=True, blank=True)
   años = models.ForeignKey(Años, on_delete=models.CASCADE, verbose_name=('Años de experiencia'))
   cv = models.FileField(null=False, upload_to='cv', blank=False,verbose_name=('Adjuntar CV'), validators=[validate_file_extension], help_text='Solo se permiten archivos PDF')
   otros_documentos = models.FileField(null=True, upload_to='cv', blank=True, verbose_name=('Otros Documentos'),validators=[validate_file_extension], help_text='Solo se permiten archivos PDF')
   ficha_fat = models.FileField(null=True, upload_to='FAT', blank=True,verbose_name=('Adjuntar Ficha FAT'))
   carta_oferta = models.FileField(null=True, upload_to='CARTA_OFERTA', blank=True,verbose_name=('Adjuntar carta oferta'))
   disponibilidad = models.ManyToManyField(Disposicion, related_name='disponibilidad', help_text=('Puede escoger más de una.'))
   titulo = models.ForeignKey(Titulo, on_delete=models.CASCADE, verbose_name=('Título'))
   nivel_ingles = models.ForeignKey(Nivel_ingles, on_delete=models.CASCADE, verbose_name=('Nivel De Ingles'))
   valido = models.BooleanField(null= False, default=False, verbose_name=('Aprobar'))
   email_send = models.BooleanField(null= False, default=False, verbose_name=('Email_enviado'))
   send = models.BooleanField(null= False, default=False, verbose_name=('Email_enviado_monica'))
   rechazar = models.BooleanField(null= False, default=False, verbose_name=('Rechazar psicolaboral'))
   rechazar_rector = models.BooleanField(null= False, default=False, verbose_name=('Rechazar'))
   rechazar_coordinador = models.BooleanField(null= False, default=False, verbose_name=('Rechazar Coordinador'))

   aceptada = models.BooleanField(null= False, default=False, verbose_name=('Aceptada'))
   rechazada = models.BooleanField(null= False, default=False, verbose_name=('Rechazada'))
   Siguiente = models.BooleanField(null= False, default=False, verbose_name=('Entrevistar'))
   liberar = models.BooleanField(null= False, default=False, verbose_name=('Liberar para todos'))
   aprobar_demos = models.BooleanField(null=False, default=False, verbose_name=('Aprobar'))
   rechazar_demos = models.BooleanField(null=False, default=False, verbose_name=('No aprobar'))
   entrevistado = models.BooleanField(null= False,default=False ,verbose_name=('Entrevistado'))
   entrevistado_demo = models.BooleanField(null= False,default=False ,verbose_name=('Entrevistado_demo'))
   psicologa = models.BooleanField(null= False,default=False, verbose_name=("Aprobar psicolaboral"))
   psicologa1 = models.BooleanField(null= False,default=False, verbose_name=("a Daisy Lasen"))
   psicologa2 = models.BooleanField(null= False,default=False, verbose_name=("a María Francisca Molina"))
   nivel_ingles = models.ForeignKey(Nivel_ingles, on_delete=models.CASCADE, verbose_name=("Nivel Inglés"))
   nivel_tec = models.ManyToManyField(Nivel_Tec, verbose_name=("Dominio de herramientas tecnológicas"), help_text=('Puede escoger más de una.'))
   enviada = models.DateField(auto_now_add=True)
   nombre_r = models.CharField(max_length=250, verbose_name=("Nombre"))
   cargo_r = models.CharField(max_length=250, verbose_name=("Cargo"))
   corre_r = models.EmailField(verbose_name=("Correo"))
   telefono_r = models.CharField(max_length=250, verbose_name=("Teléfono"), help_text=("El formato debe ser el siguiente +569xxxxxxxx"))
   relacion_r = models.CharField(max_length=250, verbose_name=("Relación laboral"))
   instituto_r = models.CharField(max_length=250, verbose_name=("Institución"))
   nombre_r_2 = models.CharField(max_length=250, verbose_name=("Nombre"))
   cargo_r_2 = models.CharField(max_length=250, verbose_name=("Cargo"))
   corre_r_2 = models.EmailField(verbose_name=("Correo"))
   telefono_r_2 = models.CharField(max_length=250, verbose_name=("Teléfono"), help_text=("El formato debe ser el siguiente +569xxxxxxxx"))
   relacion_r_2 = models.CharField(max_length=250, verbose_name=("Relación laboral"))
   instituto_r_2 = models.CharField(max_length=250, verbose_name=("Institución"))
   rector = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rector_cargo', null=True, blank=True)
   liberar_2 = models.BooleanField(null= False, default=False, verbose_name=('Liberar preferencia 2'))
   liberar_3 = models.BooleanField(null= False, default=False, verbose_name=('Liberar preferencia 3'))
   coordinador = models.BooleanField(null= False, default=False, verbose_name=('coordinador'))
   rechazar_index = models.BooleanField(null= False, default=False, verbose_name=('Rechazar'))
   liberar_coordinador = models.BooleanField(null= False, default=False, verbose_name=('Liberar'))
   liberar_equipomulti = models.BooleanField(null= False, default=False, verbose_name=('Liberar'))
   fecha_fat = models.DateField(auto_now_add=True)
   fecha_oferta = models.DateField(auto_now_add=True)
   carta_oferta_recibida = models.BooleanField(null= False, default=False, verbose_name=('carta oferta recibida'))
   finalizado = models.BooleanField(null= False, default=False, verbose_name=('Finalizar')) 
   coordinador_entrevisto = models.CharField(max_length=250, verbose_name=("Coordinador/a FFEBE que entrevistó"), null=True, blank=True)
   observaciones_c = models.TextField(max_length=250, verbose_name=("Observaciones Coordinador/a FEBE"), null=True, blank=True)
   aceptar_ficha = models.BooleanField(null= False, default=False, verbose_name=('Aceptar ficha F.A.T'))
   reemplazo = models.BooleanField(null=False, default=False, verbose_name=('Reemplazo'))
   menos15hrs = models.BooleanField(null=False, default=False, verbose_name=('-15 días'))
   mas15hrs = models.BooleanField(null=False, default=False, verbose_name=('+15 días'))
   fijo = models.BooleanField(null=False, default=False, verbose_name=('Fijo'))

   def __str__(self):
       return  '%s, %s, %s, %s' % (self.nombre, self.apellido_p, self.apellido_m,self.cargo.id)




class Rubrica(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Owner_postulacion')
    postulacion = models.ForeignKey(Postulacion, on_delete=models.CASCADE, related_name='postulacion')
    entrevistado = models.BooleanField(null= False, default=True, verbose_name=('Entrevistado'))
    puntos = models.IntegerField()
    puntos2 = models.IntegerField(verbose_name=('Puntos'))
    puntos3 = models.IntegerField(verbose_name=('Puntos'))
    puntos4 = models.IntegerField(verbose_name=('Puntos'))
    puntos5 = models.IntegerField(verbose_name=('Puntos'))
    puntos6 = models.IntegerField(verbose_name=('Puntos'))
    puntos7 = models.IntegerField(verbose_name=('Puntos'))
    puntos8 = models.IntegerField(verbose_name=('Puntos'))
    puntos9 = models.IntegerField(verbose_name=('Puntos'))
    puntos10 = models.IntegerField(verbose_name=('Puntos'))
    comentario = models.TextField(max_length=1000)
    comentario2 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario3 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario4 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario5 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario6 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario7 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario8 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario9 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario10 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    observaciones = models.CharField(max_length=1000, verbose_name=(''), null=True, blank=True)
    cargop = models.CharField(max_length=1000, verbose_name=(''))
    niveles = models.CharField(max_length=1000, verbose_name=(''))
    opcion = models.ForeignKey(opcion , on_delete=models.CASCADE, verbose_name='')
    Nombre_referencia_y_cargo_actual = models.CharField(max_length=1000, verbose_name='')
    Relación_laboral_con_postulante = models.CharField(max_length=1000, verbose_name='')
    cometarios_referencias = models.TextField(max_length=1000, verbose_name="", help_text=("fortalezas, áreas de mejora, asunto por qué dejó su trabajo"))
    renumeracion = models.CharField(max_length=250, verbose_name=(''))
    horas = models.CharField(max_length=15, verbose_name=(""))
    realizada = models.DateField(auto_now_add=True)



    def __str__(self):
        return self.postulacion.nombre

class Rubrica_coordinador(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Owner_postulacion_c')
    postulacion = models.ForeignKey(Postulacion, on_delete=models.CASCADE, related_name='postulacion_c')
    entrevistado = models.BooleanField(null= False, default=True, verbose_name=('Entrevistado_c'))
    puntos = models.IntegerField()
    puntos2 = models.IntegerField(verbose_name=('Puntos'))
    puntos3 = models.IntegerField(verbose_name=('Puntos'))
    puntos4 = models.IntegerField(verbose_name=('Puntos'))
    puntos5 = models.IntegerField(verbose_name=('Puntos'))
    puntos6 = models.IntegerField(verbose_name=('Puntos'))
    puntos7 = models.IntegerField(verbose_name=('Puntos'))

    comentario = models.TextField(max_length=1000)
    comentario2 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario3 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario4 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario5 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario6 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario7 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    rechazar = models.BooleanField(null= False, default=False, verbose_name=('rechazado'))
    observaciones = models.CharField(max_length=1000, verbose_name=(''), null=True, blank=True)
    liberar = models.BooleanField(null= False, default=False, verbose_name=('liberar'))
    cargop = models.CharField(max_length=1000, verbose_name=(''))
    niveles = models.CharField(max_length=1000, verbose_name=(''))
    opcion = models.ForeignKey(opcion , on_delete=models.CASCADE, verbose_name='')
    Nombre_referencia_y_cargo_actual = models.CharField(max_length=1000, verbose_name='')
    Relación_laboral_con_postulante = models.CharField(max_length=1000, verbose_name='')
    cometarios_referencias = models.TextField(max_length=1000, verbose_name="", help_text=("fortalezas, áreas de mejora, asunto por qué dejó su trabajo"))
    renumeracion = models.CharField(max_length=250, verbose_name=(''))
    horas = models.CharField(max_length=15, verbose_name=(""))

    realizada = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.postulacion.nombre


class Rubrica_equipomulti(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Owner_postulacion_em')
    postulacion = models.ForeignKey(Postulacion, on_delete=models.CASCADE, related_name='postulacion_em')
    entrevistado = models.BooleanField(null= False, default=True, verbose_name=('Entrevistado'))
    puntos = models.IntegerField()
    puntos2 = models.IntegerField(verbose_name=('Puntos'))
    puntos3 = models.IntegerField(verbose_name=('Puntos'))
    puntos4 = models.IntegerField(verbose_name=('Puntos'))
    puntos5 = models.IntegerField(verbose_name=('Puntos'))
    puntos6 = models.IntegerField(verbose_name=('Puntos'))
    puntos7 = models.IntegerField(verbose_name=('Puntos'))
    puntos8 = models.IntegerField(verbose_name=('Puntos'))
    puntos9 = models.IntegerField(verbose_name=('Puntos'))

    comentario = models.TextField(max_length=1000)
    comentario2 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario3 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario4 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario5 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario6 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario7 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario8 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    comentario9 = models.TextField(max_length=1000, verbose_name=('Comentario'))
    rechazar = models.BooleanField(null= False, default=False, verbose_name=('rechazado'))

    observaciones = models.CharField(max_length=1000, verbose_name=(''), null=True, blank=True)

    liberar = models.BooleanField(null= False, default=False, verbose_name=('liberar'))
    cargop = models.CharField(max_length=1000, verbose_name=(''))
    niveles = models.CharField(max_length=1000, verbose_name=(''))
    opcion = models.ForeignKey(opcion , on_delete=models.CASCADE, verbose_name='')
    Nombre_referencia_y_cargo_actual = models.CharField(max_length=1000, verbose_name='')
    Relación_laboral_con_postulante = models.CharField(max_length=1000, verbose_name='')
    cometarios_referencias = models.TextField(max_length=1000, verbose_name="", help_text=("fortalezas, áreas de mejora, asunto por qué dejó su trabajo"))
    renumeracion = models.CharField(max_length=250, verbose_name=(''))
    horas = models.CharField(max_length=15, verbose_name=(""))

    realizada = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.postulacion.nombre


OPCIONES =(
    ("1", "Bajo lo esperado"),
    ("2","Adecuado"),
    ("3","Sobre lo esperado")
)

class Conclusion(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Rubrica_psicologa(models.Model):
    postulantes = models.ForeignKey(Postulacion, on_delete=models.CASCADE, related_name='postulantes')
    aspecto = models.ForeignKey(Aspectos_generales, on_delete=models.CASCADE, verbose_name=(''),related_name=('aspectos_1'), null=True, blank=True)
    aspecto_2 = models.ForeignKey(Aspectos_generales, on_delete=models.CASCADE, verbose_name=(''), null=True, blank=True)
    competencia_1 = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name=(''), related_name=('competencia_1'), null=True, blank=True)
    competencia_2 = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name=(''), related_name=('competencia_2'), null=True, blank=True)
    competencia_3 = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name=(''), related_name=('competencia_3'), null=True, blank=True)
    competencia_4 = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name=(''), related_name=('competencia_4'), null=True, blank=True)
    competencia_5 = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name=(''), related_name=('competencia_5'), null=True, blank=True)
    competencia_6 = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name=(''), related_name=('competencia_6'), null=True, blank=True)
    competencia_7 = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name=(''), related_name=('competencia_7'), null=True, blank=True)
    competencia_8 = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name=(''), related_name=('competencia_8'), null=True, blank=True)
    competencia_9 = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name=(''), related_name=('competencia_9'), null=True, blank=True)
    competencia_10 = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name=(''), related_name=('competencia_10'), null=True, blank=True)
    competencia_11 = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name=(''), related_name=('competencia_11'), null=True, blank=True)
    competencia_12 = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name=(''), related_name=('competencia_12'), null=True, blank=True)
    competencia_13 = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name=(''), related_name=('competencia_13'), null=True, blank=True)
    competencia_14 = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name=(''), related_name=('competencia_14'), null=True, blank=True)
    competencia_15 = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name=(''), related_name=('competencia_15'), null=True, blank=True)
    competencia_16 = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name=(''), related_name=('competencia_16'), null=True, blank=True)
    competencia_17 = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name=(''), related_name=('competencia_17'), null=True, blank=True)
    competencia_18 = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name=(''), related_name=('competencia_18'), null=True, blank=True)
    competencia_19 = models.ForeignKey(Competencias, on_delete=models.CASCADE, verbose_name=(''), related_name=('competencia_19'), null=True, blank=True)
    conclusion = models.ForeignKey(Conclusion, on_delete=models.CASCADE, verbose_name=(''), null=True, blank=True)
    fortalezas = models.CharField(max_length=1000, verbose_name=(''), null=True, blank=True)
    fortalezas2 = models.CharField(max_length=1000, verbose_name=(''), null=True, blank=True)
    fortalezas3 = models.CharField(max_length=1000, verbose_name=(''), null=True, blank=True)
    posibilidades = models.CharField(max_length=1000, verbose_name=(''), null=True, blank=True)
    posibilidades2 = models.CharField(max_length=1000, verbose_name=(''), null=True, blank=True)
    posibilidades3 = models.CharField(max_length=1000, verbose_name=(''), null=True, blank=True)
    sugerencias = models.TextField(max_length=1000, verbose_name=(''), null=True, blank=True)
    realizada = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.postulantes.nombre

class Rubrica_demo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Owner_postulacion_demo')
    postulacion = models.ForeignKey(Postulacion, on_delete=models.CASCADE, related_name='postulacion_demo')
    criterio_1 = models.ForeignKey(Criterios, on_delete=models.CASCADE, related_name=('criterio_1'))
    criterio_2 = models.ForeignKey(Criterios, on_delete=models.CASCADE,related_name=('criterio_2'))
    criterio_3 = models.ForeignKey(Criterios, on_delete=models.CASCADE,related_name=('criterio_3'))
    criterio_4 = models.ForeignKey(Criterios, on_delete=models.CASCADE,related_name=('criterio_4'))
    criterio_5 = models.ForeignKey(Criterios, on_delete=models.CASCADE,related_name=('criterio_5'))
    criterio_6 = models.ForeignKey(Criterios, on_delete=models.CASCADE,related_name=('criterio_6'))
    criterio_7 = models.ForeignKey(Criterios, on_delete=models.CASCADE,related_name=('criterio_7'))
    criterio_8 = models.ForeignKey(Criterios, on_delete=models.CASCADE,related_name=('criterio_8'))
    criterio_9 = models.ForeignKey(Criterios, on_delete=models.CASCADE,related_name=('criterio_9'))
    criterio_10 = models.ForeignKey(Criterios, on_delete=models.CASCADE,related_name=('criterio_10'))
    criterio_11 = models.ForeignKey(Criterios, on_delete=models.CASCADE,related_name=('criterio_11'))
    criterio_12 = models.ForeignKey(Criterios, on_delete=models.CASCADE,related_name=('criterio_12'))
    criterio_13 = models.ForeignKey(Criterios, on_delete=models.CASCADE,related_name=('criterio_13'))
    criterio_14 = models.ForeignKey(Criterios, on_delete=models.CASCADE,related_name=('criterio_14'))
    criterio_15 = models.ForeignKey(Criterios, on_delete=models.CASCADE,related_name=('criterio_15'))
    criterio_16 = models.ForeignKey(Criterios, on_delete=models.CASCADE,related_name=('criterio_16'))
    criterio_17 = models.ForeignKey(Criterios, on_delete=models.CASCADE,related_name=('criterio_17'))
    criterio_18 = models.ForeignKey(Criterios, on_delete=models.CASCADE,related_name=('criterio_18'))
    criterio_19 = models.ForeignKey(Criterios, on_delete=models.CASCADE,related_name=('criterio_19'))
    observaciones = models.CharField(max_length=1000, verbose_name=(''), null=True, blank=True)
    realizada = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.postulacion.nombre
