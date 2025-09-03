from django.urls import path
from . import views

urlpatterns = [

## ----------------------------------------------##
## --------------  Login Usuarios -------------- ##
## ----------------------------------------------##    
    path('login/', views.obtener_usuario_registrado_ad, name='obtener_usuario_registrado_ad'),
## -------------------------------------------##
## --------------  Roles de acceso -----------##
## -------------------------------------------##
##NO NECESARIO

## -----------------------------------------------##
## -------------- Catalogo Actividades -----------##
## -----------------------------------------------##
    path('actividades/', views.obtener_catalogo_actividades, name="obtener_catalogo_actividades"),
    path('actividad/', views.obtener_actividad_por_id, name="obtener_actividad_por_id"),
    path('crear-nueva-actividad', views.crear_actividad, name="crear_actividad"),
    path('actualizar-actividad', views.actualizar_actividad, name="actualizar_actividad"),

## ------------------------------------------##
## -------------- Celulas Agencia -----------##
## ------------------------------------------##
    path('celulas/', views.obtener_celulas_agencia_digital, name="obtener_celulas_agencia_digital"),
    path('celula/', views.obtener_celula_por_id, name="obtener_celula_por_id"),

## --------------------------------------------------##
## --------------  Unidad Cliente Interno -----------##
## --------------------------------------------------##

    path('unidades-cliente-interno/', views.obtener_unidades_cliente_interno, name="obtener_unidades_cliente_interno"),
    path('unidad-cliente-interno/', views.obtener_unidades_cliente_interno_por_id, name="obtener_unidades_cliente_interno_por_id"),

## ---------------------------------------------##
## -------------- Puesto Colaborador -----------##
## ---------------------------------------------##

    path('puestos-colaborador/', views.obtener_puestos_colaboradores, name="obtener_puestos_colaboradores"),
    path('puesto-colaborador/', views.obtener_puesto_colaborador_por_id, name="obtener_puesto_colaborador_por_id"),

## ----------------------------------------------##
## -------------- Estatus Colaborador -----------##
## ----------------------------------------------##

    path('estatus-colaborador/', views.obtener_estatus_colaborador_por_id, name="obtener_estatus_colaborador_por_id"),

## ----------------------------------------------##
## -------------- Colaborador Agencia -----------##
## ----------------------------------------------##

    path('colaboradores/', views.obtener_colaboradores_ad, name="obtener_colaboradores_ad"), ##Retorna todos los colaboradores registrados en la bd
    path('colaboradores-activos/', views.obtener_colaboradores_ad_activos, name="obtener_colaboradores_ad_activos"), ##Retorna todos los colaboradores registrados en la bd
    path('colaborador/', views.obtener_colaborador_ad_por_id, name='obtener_colaborador_ad_por_id'),
    path('crear-colaborador/', views.crear_colaborador_ad, name='crear_colaborador_ad'),
    path('baja-colaborador/', views.dar_baja_colaborador_ad_por_id, name='dar_baja_colaborador_ad_por_id'),
    path('alta-altacolaborador/', views.dar_alta_colaborador_ad_por_id, name='dar_alta_colaborador_ad_por_id'),

## --------------------------------------------##
## -------------- BITACORA REGISTRO -----------##
## --------------------------------------------##

    path('bitacora-registros/', views.obtener_bitacora_registros, name="obtener_bitacora_registros"),
    path('crear-bitacora-registro/', views.crear_bitacora_registros, name="crear_bitacora_registros"),
    path('bitacora-registros-fecha-celula/', views.obtener_registros_birtacora_por_fecha_y_celula, name="obtener_registros_birtacora_por_fecha_y_celula"),
    path('bitacora-registros-fecha/', views.obtener_registros_bitacora_por_fecha, name="obtener_registros_birtacora_por_fecha")



]