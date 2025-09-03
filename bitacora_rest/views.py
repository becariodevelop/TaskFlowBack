from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import psycopg
import json
import dotenv
import os
from dotenv import dotenv_values


config = dotenv_values(".env")
dotenv.load_dotenv()
# Create your views here.
# Conexion a bd usando psycopg
def get_connection():
    return psycopg.connect(
        dbname=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
    )

# Para inicio de sesion, LOGIN
## ----------------------------------------------##
## --------------  Login Usuarios -------------- ##
## ----------------------------------------------##
@csrf_exempt
def obtener_usuario_registrado_ad(request):
    if request.method != 'POST':
        return JsonResponse({'error':'Metodo no permitido'}, status=405)
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            nombre_usuario = data.get('nombre_usuario')
            clave = data.get('clave')

            if not nombre_usuario or not clave:
                return JsonResponse({'error':'Credenciales incompletas'}, status=400)
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id_usuario, nombre_usuario, id_colaborador, id_tipo_rol_acceso FROM bitacora_agencia_digital.usuarios WHERE nombre_usuario = %s AND clave = %s", [nombre_usuario, clave])
                    row = cur.fetchone()
                    if row:
                        return JsonResponse({
                            "id_usuario":row[0],
                            "nombre_usuario":row[1],
                            "id_colaborador":row[2],
                            "id_tipo_rol_acceso": row[3]
                        })
                    else: 
                        return JsonResponse({"error":"Credenciales incorrectas"}, status=401)
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)

## -------------------------------------------##
## --------------  Roles de acceso -----------##
## -------------------------------------------##
## -------------------------------------------##

## -----------------------------------------------##
## -------------- Catalogo Actividades -----------##
## -----------------------------------------------##
#Retorna todas las actividades #Referenciar
def obtener_catalogo_actividades(request): 
    if request.method != 'GET':
        return JsonResponse({"error":"Metodo no permitido"}, status=405)
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM bitacora_agencia_digital.catalogo_actividades")
                rows = cur.fetchall()
                actividades = []
                for row in rows:
                    actividades.append({
                        "id_actividad": row[0],
                        "actividad": row[1],
                        "horas_actividad": row[2],
                        "celula": row[3],
                        "costo_unitario": row[4]
                    })
                return JsonResponse(actividades, safe=False)
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)

## Obtener actividad por su id
def obtener_actividad_por_id(request):
    if request.method != 'GET':
        return JsonResponse({"error":"Metodo no permitido"}, status=405)
    try:
        id_actividad = request.GET.get('id_actividad')
        if not id_actividad:
            return JsonResponse({"error": "Parametro id_actividad es requerido"}, status=400)
        
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM bitacora_agencia_digital.catalogo_actividades WHERE id_actividad = %s", [id_actividad])
                row = cur.fetchone()
                if row:
                    return JsonResponse({
                        "id_actividad": row[0],
                        "actividad": row[1],
                        "horas_actividad": row[2],
                        "celula": row[3],
                        "costo_unitario": row[4]
                    })
                else:
                    return JsonResponse({"error":str(e)}, status=500)
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)

#Crear actividad
def crear_actividad(request):
    if(request.method != 'POST'):
        return JsonResponse({"error":"Metodo no permitido"}, status=405)
    try:
        data = json.loads(request.body)
        actividad = data.get('actividad')
        horas_actividad = data.get('actividad')
        celula = data.get('horas_actividad')
        costo_unitario = data.get('costo_unitario')

        if not all([actividad, horas_actividad, celula, costo_unitario]):
            return JsonResponse({"error": "Todos los campos son requeridos"})
        
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO bitacora_agencia_digital.catalogo_actividades(actividad, horas_actividad, celula, costo_unitario) VALUES (%s, %s, %s, %s) RETURNING id_actividad", [actividad, horas_actividad, celula, costo_unitario])
                nuevo_id = cur.fetchone()[0]
                return JsonResponse({'mensaje':'Actividad creada exitosamente', 'id_actividad': nuevo_id})
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)
    
#Actualizar actividad
def actualizar_actividad(request):
    if(request.method != 'POST'):
        return JsonResponse({"error":"Metodo no permitido"}, status=405)
    try:
        data = json.loads(request.body)
        id_actividad = data.get('id_actividad')
        actividad = data.get('actividad')
        horas_actividad = data.get('actividad')
        celula = data.get('horas_actividad')
        costo_unitario = data.get('costo_unitario')

        if not id_actividad:
            return JsonResponse({"error": "Campo id_actividad no encontrado"}, status=400)
        
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE bitacora_agencia_digital.catalogo_actividades SET actividad = %s, horas_actividad = %s, celula = %s, costo_unitario = %s WHERE id_actividad = %s", [actividad, horas_actividad, celula, costo_unitario])
                if cur.rowcount == 0:
                    return JsonResponse({"error":"Actividad no encontrada"}, status=400)
                return JsonResponse({'mensaje':'Actividad actualizada exitosamente'})
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)
    


#Eliminar actividad
#No se usará 

## ------------------------------------------##
## -------------- Celulas Agencia -----------##
## ------------------------------------------##
#Obtener todas las celulas de la agencia
def obtener_celulas_agencia_digital(request):
    if request.method != 'GET':
        return JsonResponse({"error":"Metodo no permitido"}, status=405)
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM bitacora_agencia_digital.celulas_agencia_digital")
                rows = cur.fetchall()
                celulas = []
                for row in rows:
                    celulas.append({
                        "id_celula_agencia_digital": row[0],
                        "celula": row[1]
                    })
                return JsonResponse(celulas, safe=False)
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)
    
def obtener_celula_por_id(request):
    if request.method != 'GET':
        return JsonResponse({"error":"Metodo no permitido"}, status=405)
    
    try:
        id_celula_agencia_digital = request.GET.get('id_celula_agencia_digital')
        if not id_celula_agencia_digital:
            return JsonResponse({"error":"Parametro id_celula_agencia_digital requerido"})
        
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM bitacora_agencia_digital.celulas_agencia_digital WHERE id_celula_agencia_digital = %s", [id_celula_agencia_digital])
                row = cur.fetchone()
                
                if row:
                    return JsonResponse({
                        "id_celula_agencia_digital": row[0],
                        "celula": row[1]
                    })
                else:
                    return JsonResponse({"error": "Celula no encontrada"}, status = 404)
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)

#Crear celula
#Pentiende

#Actualzar nombre celula
#Pentiende

#Eliminar celula
#Pentiende

## --------------------------------------------------##
## --------------  Unidad Cliente Interno -----------##
## --------------------------------------------------##
def obtener_unidades_cliente_interno(request):
    if request.method != 'GET':
        return JsonResponse({"error":"Metodo no permitido"}, status=405)
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM bitacora_agencia_digital.unidad_cliente_interno")
                rows = cur.fetchall()
                unidades = []
                for row in rows:
                    unidades.append({
                        "id_unidad_cliente_interno": row[0],
                        "nombre_cliente_interno": row[1]
                    })
                return JsonResponse(unidades, safe=False)
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)

def obtener_unidades_cliente_interno_por_id(request):
    if request.method != 'GET':
        return JsonResponse({"error":"Metodo no permitido"}, status=405)
    
    try:
        id_unidad_cliente_interno = request.GET.get('id_unidad_cliente_interno')
        if not id_unidad_cliente_interno:
            return JsonResponse({"error":"Parametro id_unidad_cliente_interno requerido"})
        
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM bitacora_agencia_digital.unidad_cliente_interno WHERE id_unidad_cliente_interno = %s", [id_unidad_cliente_interno])
                row = cur.fetchone()
                
                if row:
                    return JsonResponse({
                        "id_unidad_cliente_interno": row[0],
                        "celula": row[1]
                    })
                else:
                    return JsonResponse({"error": "Unidad Organizativa no encontrada"}, status = 404)
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)

#Crear, actualzar y eliminar pendientes

## ---------------------------------------------##
## -------------- Puesto Colaborador -----------##
## ---------------------------------------------##
def obtener_puestos_colaboradores(request):
    if request.method != 'GET':
        return JsonResponse({"error":"Metodo no permitido"}, status=405)
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM bitacora_agencia_digital.puesto_colaborador")
                rows = cur.fetchall()
                puestos = []
                for row in rows:
                    puestos.append({
                        "id_puesto_colaborador": row[0],
                        "puesto_colaborador": row[1],
                        "celula": row[2],
                        "unidad_organizativa": row[3]
                    })
                return JsonResponse(puestos, safe=False)
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)

def obtener_puesto_colaborador_por_id(request):
    if request.method != 'GET':
        return JsonResponse({"error":"Metodo no permitido"}, status=405)
    
    try:
        id_puesto_colaborador = request.GET.get('id_puesto_colaborador')
        if not id_puesto_colaborador:
            return JsonResponse({"error":"Parametro id_puesto_colaborador requerido"})
        
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM bitacora_agencia_digital.puesto_colaborador WHERE id_puesto_colaborador = %s", [id_puesto_colaborador])
                row = cur.fetchone()
                
                if row:
                    return JsonResponse({
                        "id_puesto_colaborador": row[0],
                        "celula": row[1]
                    })
                else:
                    return JsonResponse({"error": "Puesto colaborador no encontrado"}, status = 404)
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)
    
#Crear, actualizar y eliminar puestos
#Pendiente

## ----------------------------------------------##
## -------------- Estatus Colaborador -----------##
## ----------------------------------------------##
#Solo se requiere estatus colaborador por id
def obtener_estatus_colaborador_por_id(request):
    if request.method != 'GET':
        return JsonResponse({"error":"Metodo no permitido"}, status=405)
    
    try:
        id_estatus_colaborador = request.GET.get('id_estatus_colaborador')
        if not id_estatus_colaborador:
            return JsonResponse({"error":"Parametro id_estatus_colaborador requerido"}, status = 405)
        
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM bitacora_agencia_digital.estatus_colaborador WHERE id_estatus_colaborador = %s", [id_estatus_colaborador])
                row = cur.fetchone()
                
                if row:
                    return JsonResponse({
                        "id_estatus_colaborador": row[0],
                        "estatus_colaborador": row[1],
                        "impacto_nomina": row[2]
                    })
                else:
                    return JsonResponse({"error": "No existe ese estatus para un colaborador"}, status = 404)
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)

## ----------------------------------------------##
## -------------- Colaborador Agencia -----------##
## ----------------------------------------------##
#Obtener todos los colaboradores de la agencia digital
def obtener_colaboradores_ad(request):
    if request.method != 'GET':
        return JsonResponse({'error':'Metodo no permitido'}, status=405)
    try:
        if request.method == 'GET':
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM bitacora_agencia_digital.colaborador_agencia_digital")
                    rows = cur.fetchall()
                    colaboradores = []
                    for row in rows:
                        colaboradores.append({
                            "id_colaborador":row[0], 
                            "celula":row[1], 
                            "id_puesto_colaborador":row[2], 
                            "puesto_colaborador":row[3], 
                            "nombre_colaborador":row[4], 
                            "horas_diarias":row[5], 
                            "horas_mes":row[6], 
                            "id_estatus_colaborador":row[7], 
                            "estatus_colaborador":row[8]
                            })
                    return JsonResponse(colaboradores, safe=False)
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)
    
def obtener_colaboradores_ad_activos(request):
    if request.method != 'GET':
        return JsonResponse({'error':'Metodo no permitido'}, status=405)
    try:
        if request.method == 'GET':
            with get_connection() as conn:
                with conn.cursor() as cur:
                    estado_colaborador = 'Activo'
                    cur.execute("SELECT * FROM bitacora_agencia_digital.colaborador_agencia_digital WHERE estatus_colaborador = %s",[estado_colaborador])
                    rows = cur.fetchall()
                    colaboradores = []
                    for row in rows:
                        colaboradores.append({
                            "id_colaborador":row[0], 
                            "celula":row[1], 
                            "id_puesto_colaborador":row[2], 
                            "puesto_colaborador":row[3], 
                            "nombre_colaborador":row[4], 
                            "horas_diarias":row[5], 
                            "horas_mes":row[6], 
                            "id_estatus_colaborador":row[7], 
                            "estatus_colaborador":row[8]
                            })
                    return JsonResponse(colaboradores, safe=False)
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)
            
#Obtener un colaborador de la agencia
def obtener_colaborador_ad_por_id(request):
    if request.method != 'GET':
        return JsonResponse({'error':'Metodo no permitido'}, status=405)
    try:
        if request.method == 'GET':
            #data = json.loads(request.body)
            #id_colaborador = data.get('id_colaborador')
            id_colaborador = request.GET.get('id_colaborador')
            if not id_colaborador:
                return JsonResponse({'error': 'Parámetro id_colaborador requerido'}, status=400)
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM bitacora_agencia_digital.colaborador_agencia_digital WHERE id_colaborador = %s",[id_colaborador])
                    row = cur.fetchone()
                    if row:
                        return JsonResponse({
                            "id_colaborador":row[0], 
                            "celula":row[1], 
                            "id_puesto_colaborador":row[2], 
                            "puesto_colaborador":row[3], 
                            "nombre_colaborador":row[4], 
                            "horas_diarias":row[5], 
                            "horas_mes":row[6], 
                            "id_estatus_colaborador":row[7], 
                            "estatus_colaborador":row[8]
                        })
                    else:
                        return JsonResponse({"error":"Colaborador no encontrado"}, status = 404)
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)

@csrf_exempt
def crear_colaborador_ad(request):
    if request.method != 'POST':
        return JsonResponse({'error':'Metodo no permitido'}, status=405)
    try:
        data = json.loads(request.body)
        celula = data.get('celula')
        id_puesto_colaborador = data.get('id_puesto_colaborador')
        puesto_colaborador = data.get('puesto_colaborador')
        nombre_colaborador = data.get('nombre_colaborador')
        horas_diarias = data.get('horas_diarias')
        horas_mes = data.get('horas_mes')
        id_estatus_colaborador = data.get('id_estatus_colaborador', 1)
        estatus_colaborador = data.get('estatus_colaborador', 'Activo')

        if not all([celula, id_puesto_colaborador, puesto_colaborador, nombre_colaborador, horas_diarias, horas_mes, id_estatus_colaborador, estatus_colaborador]):
            return JsonResponse({'error': 'Todos los campos son requeridos'})
        
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                                INSERT INTO bitacora_agencia_digital.colaborador_agencia_digital(
	                                celula, 
	                                id_puesto_colaborador, 
	                                puesto_colaborador, 
	                                nombre_colaborador,
	                                horas_diarias,
	                                horas_mes,
	                                id_estatus_colaborador, 
	                                estatus_colaborador
	                                )
                                VALUES 
                                (%s,%s,%s, %s,%s,%s,%s,%s) RETURNING id_colaborador
                            """,
                            [celula, id_puesto_colaborador, puesto_colaborador, nombre_colaborador, horas_diarias, horas_mes, id_estatus_colaborador, estatus_colaborador])
                nuevo_id = cur.fetchone()[0]
                return JsonResponse({'mensaje':'colaborador agregado correctamente', 'id_colaborador': nuevo_id})
    except Exception as e:
        return JsonResponse({"error":str(e)}, status=500)

#Actualizar el estado del colaborador BAJA
@csrf_exempt
def dar_baja_colaborador_ad_por_id(request):
    if request.method != 'POST':
        return JsonResponse({'error':'Metodo no permitido'}, status=405)
    try:
        if request.method == 'POST':
            #data = json.loads(request.body)
            #id_colaborador = data.get('id_colaborador')
            data = json.loads(request.body)
            id_colaborador = data.get('id_colaborador')
            if not id_colaborador:
                return JsonResponse({'error': 'Parámetro id_colaborador requerido'}, status=400)
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("UPDATE bitacora_agencia_digital.colaborador_agencia_digital SET id_estatus_colaborador = 2, estatus_colaborador = 'Inactivo' WHERE id_colaborador = %s",[id_colaborador])
                    #res = cur.fetchone()
                    filas_afectadas = cur.rowcount
                    if filas_afectadas == 0:
                        return JsonResponse({"error":"Colaborador no encontrado"}, status = 404)
                    if filas_afectadas:
                        return JsonResponse({'mensaje':'Colaborador dado de baja exitosamente'})
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)
    
#Actualizar el estado del colaborador ALTA
@csrf_exempt
def dar_alta_colaborador_ad_por_id(request):
    if request.method != 'POST':
        return JsonResponse({'error':'Metodo no permitido'}, status=405)
    try:
        if request.method == 'POST':
            #data = json.loads(request.body)
            #id_colaborador = data.get('id_colaborador')
            data = json.loads(request.body)
            id_colaborador = data.get('id_colaborador')
            if not id_colaborador:
                return JsonResponse({'error': 'Parámetro id_colaborador requerido'}, status=400)
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("UPDATE bitacora_agencia_digital.colaborador_agencia_digital SET id_estatus_colaborador = 1, estatus_colaborador = 'Activo' WHERE id_colaborador = %s",[id_colaborador])
                    #res = cur.fetchone()
                    filas_afectadas = cur.rowcount
                    if filas_afectadas == 0:
                        return JsonResponse({"error":"Colaborador no encontrado"}, status = 404)
                    if filas_afectadas:
                        return JsonResponse({'mensaje':'Se cambió el estatus del colaborador a Activo exitosamente'})
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)

#Actualizar datos de colaborador y eliminar colaborador pendientes
#Pendientes

## --------------------------------------------##
## -------------- BITACORA REGISTRO -----------##
## --------------------------------------------##
#Obtener todos los registros de la bitacora
def obtener_bitacora_registros(request):
    if request.method != 'GET':
        return JsonResponse({'error':'Metodo no permitido'}, status=405)
    try:
        if request.method == 'GET':
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM bitacora_agencia_digital.bitacora_registro")
                    rows = cur.fetchall()
                    registros = []
                    for row in rows:
                        registros.append({
                            "id_bitacora_registro":row[0], 
                            "fecha_registro":row[1], 
                            "id_celula_agencia_digital":row[2], 
                            "celula":row[3], 
                            "id_colaborador":row[4], 
                            "nombre_colaborador":row[5], 
                            "id_actividad":row[6], 
                            "actividad":row[7], 
                            "cantidad":row[8],
                            "id_unidad_cliente_interno":row[9],
                            "nombre_cliente_interno":row[10]
                            })
                    return JsonResponse(registros, safe=False)
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)


@csrf_exempt
def crear_bitacora_registros(request):
    if request.method != 'POST':
        return JsonResponse({'error':'Metodo no permitido'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))

        fecha_registro = data.get('fecha_registro')
        id_celula_agencia_digital = data.get('id_celula_agencia_digital')
        celula = data.get('celula')
        id_colaborador = data.get('id_colaborador')
        nombre_colaborador = data.get('nombre_colaborador')
        id_actividad = data.get('id_actividad')
        actividad = data.get('actividad')
        cantidad = data.get('cantidad')
        id_unidad_cliente_interno = data.get('id_unidad_cliente_interno')
        nombre_cliente_interno = data.get('nombre_cliente_interno')

        print(cantidad, 'CANTIDAD')

        # fecha_registro = request.POST.get('fecha_registro')
        # id_celula_agencia_digital = request.POST.get('id_celula_agencia_digital')
        # celula = request.POST.get('celula')
        # id_colaborador = request.POST.get('id_colaborador')
        # nombre_colaborador = request.POST.get('nombre_colaborador')
        # id_actividad = request.POST.get('id_actividad')
        # actividad = request.POST.get('actividad')
        # cantidad = request.POST.get('cantidad')
        # id_unidad_cliente_interno = request.POST.get('id_unidad_cliente_interno')
        # nombre_cliente_interno = request.POST.get('nombre_cliente_interno')

        if not all([fecha_registro,id_celula_agencia_digital,celula,id_colaborador,nombre_colaborador,id_actividad,actividad,cantidad,id_unidad_cliente_interno,nombre_cliente_interno]):
            print('Error, campos requeridos')
            return JsonResponse({'error': 'Todos los campos son requeridos'})
        
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                                INSERT INTO bitacora_agencia_digital.bitacora_registro(
	                                fecha_registro, 
	                                id_celula_agencia_digital, 
	                                celula, 
	                                id_colaborador,
	                                nombre_colaborador,
	                                id_actividad,
	                                actividad, 
	                                cantidad,
                                    id_unidad_cliente_interno,
                                    nombre_cliente_interno
	                                )
                                VALUES 
                                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id_bitacora_registro
                            """,
                            [fecha_registro, id_celula_agencia_digital,celula,id_colaborador,nombre_colaborador,id_actividad,actividad,cantidad,id_unidad_cliente_interno,nombre_cliente_interno])
                nuevo_id = cur.fetchone()[0]
                conn.commit()
                return JsonResponse({'mensaje':'Actividad registrada correctamente', 'id_registro': nuevo_id})
    except Exception as e:
        return JsonResponse({"error":str(e)}, status=500)

#Obtener Registros de bitacora por AÑO, MES, DIA y Celula. 

def obtener_registros_birtacora_por_fecha_y_celula(request):
    if request.method != 'GET':
        return JsonResponse({'error':'Metodo no permitido'}, status=405)
    try:
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_termino')
        celula = request.GET.get('celula')
        print('Params: ', fecha_fin, fecha_fin, celula)

        if request.method == 'GET':
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM bitacora_agencia_digital.bitacora_registro WHERE fecha_registro BETWEEN %s AND %s AND celula ILIKE %s",[fecha_inicio, fecha_fin, celula])
                    rows = cur.fetchall()
                    registros = []
                    
                    for row in rows:
                        registros.append({
                            "id_bitacora_registro":row[0], 
                            "fecha_registro":row[1], 
                            "id_celula_agencia_digital":row[2], 
                            "celula":row[3], 
                            "id_colaborador":row[4], 
                            "nombre_colaborador":row[5], 
                            "id_actividad":row[6], 
                            "actividad":row[7], 
                            "cantidad":row[8],
                            "id_unidad_cliente_interno":row[9],
                            "nombre_cliente_interno":row[10]
                            })
                        print(registros)
                        
                    return JsonResponse(registros, safe=False)
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)

#Obtener Registros de bitacora por AÑO, MES y DIA. 

def obtener_registros_bitacora_por_fecha(request):
    if request.method != 'GET':
        return JsonResponse({'error':'Metodo no permitido'}, status=405)
    try:
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_termino')

        if request.method == 'GET':
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM bitacora_agencia_digital.bitacora_registro WHERE fecha_registro BETWEEN %s AND %s ORDER BY fecha_registro DESC",[fecha_inicio, fecha_fin])
                    rows = cur.fetchall()
                    registros = []
                    for row in rows:
                        registros.append({
                            "id_bitacora_registro":row[0], 
                            "fecha_registro":row[1], 
                            "id_celula_agencia_digital":row[2], 
                            "celula":row[3], 
                            "id_colaborador":row[4], 
                            "nombre_colaborador":row[5], 
                            "id_actividad":row[6], 
                            "actividad":row[7], 
                            "cantidad":row[8],
                            "id_unidad_cliente_interno":row[9],
                            "nombre_cliente_interno":row[10]
                            })
                    return JsonResponse(registros, safe=False)
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)
    

def actualizar_registro_bitacora(request):
    if(request.method != 'POST'):
        return JsonResponse({"error":"Metodo no permitido"}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
        id_bitacora_registro = data.get('id_bitacora_registro')
        fecha_registro = data.get('fecha_registro')
        id_celula_agencia_digital = data.get('id_celula_agencia_digital')
        celula = data.get('celula')
        id_colaborador = data.get('id_colaborador')
        nombre_colaborador = data.get('nombre_colaborador')
        id_actividad = data.get('id_actividad')
        actividad = data.get('actividad')
        cantidad = data.get('cantidad')
        id_unidad_cliente_interno = data.get('id_unidad_cliente_interno')
        nombre_cliente_interno = data.get('nombre_cliente_interno')


        if not all([id_bitacora_registro, fecha_registro, id_celula_agencia_digital, celula, id_colaborador, nombre_colaborador, id_actividad, actividad, cantidad, id_unidad_cliente_interno, nombre_cliente_interno]):
            return JsonResponse({"error": "Campos para actualizar o registro no encontrado"}, status=400)
        
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE bitacora_agencia_digital.bitacora_registro SET fecha_registro = %s, id_celula_agencia_digital = %s, celula = %s, id_colaborador = %s, nombre_colaborador = %s, id_actividad = %s, actividad = %s, cantidad = %s, id_unidad_cliente_interno = %s, nombre_cliente_interno = %s  WHERE id_bitacora_registro = %s", [fecha_registro, id_celula_agencia_digital, celula, id_colaborador, nombre_colaborador, id_actividad, actividad, cantidad, id_unidad_cliente_interno, nombre_cliente_interno, id_bitacora_registro])
                if cur.rowcount == 0:
                    return JsonResponse({"error":f"Registro no encontrado con el id {id_bitacora_registro}"}, status=400)
                return JsonResponse({'mensaje':'Actividad actualizada exitosamente'})
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)