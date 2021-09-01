from django.urls import include, path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from .views import cv, coordinacion, rectores, psicologa, monica
urlpatterns = [
    path('postulacion', cv.index, name='index'),
    path('', cv.home, name='home'),
    path('user_profile', cv.user_profile, name='user'),
    path('ajax/load-indi/', cv.load_indi, name='ajax_load_indi'),

    path('coordinacion/', include(([
        path('postulantes', coordinacion.index, name='index'),
        path('rechazados', coordinacion.rechazados, name='rechazados'),
        path('finalizado', coordinacion.finalizados, name='fin'),
        path('reemplazo_finalizado', coordinacion.finalizadosr, name='finr'),

        path('finalizados', coordinacion.finalizados_c, name='fin_c'),
        path('finalizados_em', coordinacion.finalizados_em, name='fin_em'),
        path('ficha_fat', coordinacion.carta_oferta, name='ficha_fat'),
        path('ficha_fat_c', coordinacion.carta_oferta_c, name='ficha_fat_c'),
        path('ficha_fat_em', coordinacion.carta_oferta_em, name='ficha_fat_em'),
        path('ficha_fat_admin', coordinacion.carta_oferta_admin, name='ficha_fat_admin'),


        path('postulante/<int:pk>/liberar_c/', coordinacion.liberar_c, name='liberar_c'),
        path('postulante/<int:pk>/editar/', coordinacion.editar_r, name='editar'),


        path('coordinadores', coordinacion.index_c, name='coordinadores'),
        path('coordinadores/entrevistar', coordinacion.entrevistar_c, name='entrevistar'),
        path('coordinadores/<int:pk>/rubrica/', coordinacion.rubrica, name='rubrica'),
        path('postulantes/<int:pk>/rubricas/', coordinacion.rubricas, name='rubricas'),
        path('equipomulti/estado_em', coordinacion.estado_em, name='estado_em'),
        path('administrativos/index_admin', coordinacion.index_admin, name='index_admin'),

        path('equipomulti', coordinacion.index_equipomulti, name='equipo_multi'),


        path('postulantes/<int:pk>/rubrica_rector/', coordinacion.vista_rubrica, name='vista_rubrica'),
        path('coordinadores/<int:pk>/rubrica_coordinador/', coordinacion.vista_rubricaC, name='vista_rubrica_coordinador'),
        path('postulantes/<int:pk>/vista_rubrica_equipo/', coordinacion.vista_rubrica_equipo, name='vista_rubrica_equipo'),
        path('postulantes/<int:pk>/vista_rubrica_psicologa/', coordinacion.vista_rubrica_psicologa, name='vista_rubrica_psicologa'),
        path('postulantes/<int:pk>/vista_rubrica_demo/', coordinacion.vista_rubrica_demo, name='vista_rubrica_demo'),
        path('postulantes/<int:pk>/vista_rubrica_coordinador/', coordinacion.vista_rubricaC, name='vista_rubrica_coordinador'),

        path('activos', coordinacion.activos, name='activos'),
        path('proceso', coordinacion.proceso, name='proceso'),
        path('psicolaboral', coordinacion.psicolaboral, name='psicolaboral'),
        path('psicolaboral_coordinador', coordinacion.psicolaboral_c, name='psicolaboral_c'),
        path('psicolaboral_equipomulti', coordinacion.psicolaboral_em, name='psicolaboral_em'),
        path('psicolaboral_admin', coordinacion.psicolaboral_admin, name='psicolaboral_admin'),

        path('postulante/<int:pk>/finalizar', coordinacion.finalizar, name='finalizar'),
        path('postulantes/<int:pk>/', coordinacion.info, name='info'),
        path('postulantes/<int:pk>/delete', coordinacion.PostulanteDeleteView.as_view(), name='borrar'),
    ], 'CV_APP'), namespace='coordinacion')),

    path('rectores/', include(([

        path('postulante/<int:pk>/editar/', rectores.editar_r, name='editar'),
        path('reemplazo_finalizado', rectores.finalizadosr, name='finr'),



        path('postulantes', rectores.index, name='index'),
        path('postulantes/<int:pk>/', rectores.info, name='info'),
        path('postulantes/rechazados/', rectores.cargo, name='rechazados'),
        path('postulantes/clasedemo/', rectores.clasedemo, name='clasedemo'),
        path('postulantes/oferta/', rectores.oferta_view, name='oferta_view'),

        path('postulantes/entrevistas/', rectores.entrevista, name='entrevistas'),
        path('postulantes/<int:pk>/rubricas/', rectores.rubricas, name='rubricas'),
        path('postulantes/<int:pk>/rubrica/', rectores.rubrica, name='rubrica'),
        path('postulantes/<int:pk>/vista_rubrica/', rectores.vista_rubrica, name='vista_rubrica'),
        path('postulantes/<int:pk>/vista_rubrica_equipo/', rectores.vista_rubrica_equipo, name='vista_rubrica_equipo'),
        path('postulantes/<int:pk>/vista_rubrica_demo/', rectores.vista_rubrica_demo, name='vista_rubrica_demo'),
        path('postulantes/<int:pk>/vista_rubrica_psicologa/', rectores.vista_rubrica_psicologa, name='vista_rubrica_psicologa'),
        path('postulantes/<int:pk>/vista_rubrica_coordinador/', rectores.vista_rubricaC, name='vista_rubrica_coordinador'),

        path('postulantes/<int:pk>/rubrica_equipo/', rectores.rubricaem, name='rubrica_em'),
        path('postulantes/<int:pk>/rubrica_demo/', rectores.rubricademo, name='rubrica_demo'),
        path('postulantes/<int:pk>/rubrica_coordinador/', rectores.rubrica_coordinador, name='rubrica_coordinador'),
        path('postulantes/<int:pk>/send/', rectores.send, name='send'),
        path('postulantes/<int:pk>/reportar/', rectores.reportar, name='reportar'),
        path('postulantes/<int:pk>/ficha/', rectores.subirficha, name='ficha'),
        path('postulantes/<int:pk>/oferta_laboral/', rectores.oferta, name='oferta'),
        path('finalizado', rectores.finalizados, name='fin'),

        path('postulantes/aprobados/',rectores.aprobados, name='aprobados'),
    ], 'CV_APP'), namespace='rectores')),

    path('psicologa/', include(([
        path('postulantes', psicologa.index, name='index'),
        path('postulantes/<int:pk>/vista_rubrica/', psicologa.vista_rubrica, name='vista_rubrica'),
        path('postulantes/<int:pk>/rubrica_coordinador/',psicologa.vista_rubricaC, name='vista_rubrica_coordinador'),
        path('postulantes/<int:pk>/rubrica_psicologica/', psicologa.rubrica, name='rubrica'),
        path('postulantes/<int:pk>/rubrica_psicologica_edit/', psicologa.rubrica_edit, name='rubrica_edit'),

        path('postulantes/entrevistados/',psicologa.entrevistados, name='entrevistados'),
        path('postulantes/<int:pk>/vista_rubrica_psicologa/', psicologa.vista_rubrica_psicologa, name='vista_rubrica_psicologa'),
        path('postulantes/<int:pk>/rubricas/', psicologa.rubricas, name='rubricas'),
        path('postulantes/<int:pk>/vista_rubrica_equipo/', psicologa.vista_rubrica_equipo, name='vista_rubrica_equipo'),
        path('postulantes/<int:pk>/vista_rubrica_demo/', psicologa.vista_rubrica_demo, name='vista_rubrica_demo'),
        path('rechazados', psicologa.rechazados, name='rechazados'),
        path('postulantes/<int:pk>/', psicologa.info, name='info'),

    ], 'CV_APP'), namespace='psicologa')),

    path('monica/', include(([
        path('postulantes/', monica.postulantes, name='postulantes'),
        path('postulantes/index/', monica.index, name='index'),
        path('postulantes/<int:pk>/vista_rubrica/', monica.vista_rubrica, name='vista_rubrica'),
        path('postulantes/<int:pk>/rubrica_coordinador/',monica.vista_rubricaC, name='vista_rubrica_coordinador'),
        path('postulantes/<int:pk>/vista_rubrica_psicologa/', monica.vista_rubrica_psicologa, name='vista_rubrica_psicologa'),
        path('postulantes/<int:pk>/rubricas/', monica.rubricas, name='rubricas'),
        path('postulantes/<int:pk>/vista_rubrica_equipo/', monica.vista_rubrica_equipo, name='vista_rubrica_equipo'),
        path('postulantes/<int:pk>/vista_rubrica_demo/', monica.vista_rubrica_demo, name='vista_rubrica_demo'),
        path('rechazados', monica.rechazados, name='rechazados'),
        path('postulantes/<int:pk>/', monica.info, name='info'),
        path('aceptar', monica.aceptar, name='aceptar'),
        path('postulante/<int:pk>/aceptar_ficha', monica.finalizar, name='aceptar_ficha'),
        path('finalizado', monica.finalizados, name='fin'),
    ], 'CV_APP'), namespace='monica')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)