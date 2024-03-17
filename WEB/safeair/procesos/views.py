from django.shortcuts import render
from oauthlib.oauth2 import BackendApplicationClient
import psycopg2
from requests_oauthlib import OAuth2Session
import iot_api_client as iot
from iot_api_client.rest import ApiException
from iot_api_client.configuration import Configuration
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http import JsonResponse
import requests
from django.template.loader import render_to_string
from django.core import serializers
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from django.utils import timezone
import json
from pyfcm import FCMNotification
import datetime
from flask import Flask, render_template, send_file, request
import matplotlib.pyplot as plt
from io import BytesIO
import json


cred = credentials.Certificate('C:/Users/hp/Downloads/safeair-4fcf5-firebase-adminsdk-lizma-c321cbcfee.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://safeair-4fcf5-default-rtdb.firebaseio.com'
})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def procesos(request):
    oauth_client = BackendApplicationClient(
        client_id="LAK8blfDuPyuOUEmDAsGeww4UKW5WQRs")
    token_url = "https://api2.arduino.cc/iot/v1/clients/token"
    oauth = OAuth2Session(client=oauth_client)
    token = oauth.fetch_token(
        token_url=token_url,
        client_id="LAK8blfDuPyuOUEmDAsGeww4UKW5WQRs",
        client_secret="e3yboLMG1QVTLpFs52ZwCvVicrUK2qnm5iXAEiw4jzxqim3uis3vMqRsL9WDxdfZ",
        include_client_id=True,
        audience="https://api2.arduino.cc/iot",
    )
    access_token = token.get("access_token")

    # Configuración y creación del cliente de la API
    client_config = Configuration(host="https://api2.arduino.cc/iot")
    client_config.access_token = access_token
    client = iot.ApiClient(client_config)
    thing_id = "f5de57c0-6efc-4691-9eec-993ab529f9c9"
    thing_id2 = "8bed9bdf-e614-464d-8da6-52952338f2b9"

    # Interactuar con la API para obtener propiedades
    # print(client)
    api = iot.PropertiesV2Api(client)
    # api = iot.DevicesV2Api(client)
    try:
        resp = api.properties_v2_list(thing_id)
        resp1 = api.properties_v2_list(thing_id2)
        properties = resp  # Aquí obtienes las propiedades de Arduino Cloud
        properties2 = resp1
    except ApiException as e:
        properties = []  # Manejo de excepciones
    return render(request, 'procesos_prin.html', {'properties': properties, 'properties2': properties2})


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def actualizar_propiedades(request):
    oauth_client = BackendApplicationClient(
        client_id="LAK8blfDuPyuOUEmDAsGeww4UKW5WQRs")
    token_url = "https://api2.arduino.cc/iot/v1/clients/token"
    oauth = OAuth2Session(client=oauth_client)
    token = oauth.fetch_token(
        token_url=token_url,
        client_id="LAK8blfDuPyuOUEmDAsGeww4UKW5WQRs",
        client_secret="e3yboLMG1QVTLpFs52ZwCvVicrUK2qnm5iXAEiw4jzxqim3uis3vMqRsL9WDxdfZ",
        include_client_id=True,
        audience="https://api2.arduino.cc/iot",
    )
    access_token = token.get("access_token")

    # Configuración y creación del cliente de la API
    client_config = Configuration(host="https://api2.arduino.cc/iot")
    client_config.access_token = access_token
    client = iot.ApiClient(client_config)
    thing_id = "f5de57c0-6efc-4691-9eec-993ab529f9c9"
    thing_id2 = "8bed9bdf-e614-464d-8da6-52952338f2b9"

    # Interactuar con la API para obtener propiedades
    api = iot.PropertiesV2Api(client)
    try:
        resp = api.properties_v2_list(thing_id)
        resp1 = api.properties_v2_list(thing_id2)
        properties = resp  # Aquí obtienes las propiedades de Arduino Cloud
        properties2 = resp1
        properties_data = [{'last_value': property.last_value}
                           for property in properties]
        properties2_data = [{'last_value': property.last_value}
                            for property in properties2]

        last_value1 = properties[0].last_value if properties else None
        last_value2 = properties[1].last_value if properties else None
        # last_value3 = properties[2].last_value if properties else None
        last_value3 = round(float(properties[2].last_value), 2) if properties[2].last_value else None

        last_value4 = properties2[0].last_value if properties2 else None
        last_values2 = properties2[1].last_value if properties2 else None

        if last_value4 is not None and last_value4 > 500:
            enviar_notificacion_a_todos("🚨ALERTA🚨","El valor del dispositivo de cocina es: "+str(last_value4), "last_value4")
        if last_value1 is not None and last_value1 > 300:
                enviar_notificacion_a_todos("🚨ALERTA🚨","El la calidad del aire actual es de : "+str(last_value1), "last_value1")
        if last_value2 is not None and last_value2 > 90:
                    enviar_notificacion_a_todos("🚨ALERTA🚨","Se ha detectado humedad en el ambiente : "+str(last_value2) +" Se abrio la ventana", "last_value2")
        if last_value3 is not None and last_value3 > 30:
                        enviar_notificacion_a_todos("🚨☀ALERTA☀🚨","Se ha detectado una temperatura superior a : "+str(last_value3) +" Se encendió el ventilador", "last_value3")

        fecha_hora_actual = timezone.now()
        fecha_hora_formateada = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")

        enviar_a_firebase(last_value1, last_value2, last_value3, last_value4, last_values2, fecha_hora_formateada)
        
        if last_value4>500:
            descricion='¡Peligro! Se ha detecto anomalias en el dispositivo de la cocina'
            enviar_a_firebase_peligro(last_value1, last_value2, last_value3, last_value4, last_values2, descricion, fecha_hora_formateada)
        if last_value1>300:
            descricion='La calidad del aire no es muy buena'
            enviar_a_firebase_peligro(last_value1, last_value2, last_value3, last_value4, last_values2, descricion,fecha_hora_formateada)

        #print(properties_data[0])
        # print(properties)
        # print(properties2)
        print(last_values2)

        return JsonResponse({'last_value1': last_value1, 'last_value2': last_value2,
                              'last_value3': last_value3, 'last_value4': last_value4, 'last_values2': last_values2})
    except ApiException as e:
        return JsonResponse({'error': 'Error al obtener las propiedades'}, status=500)

def enviar_a_firebase(value1, value2, value3, value4, value5, fecha):
    try:
        # Obtén una referencia a la base de datos de Firebase
        ref = db.reference('/lecturas_sensor')  # Ruta en la base de datos de Firebase

        # Envía los datos a la base de datos de Firebase
        ref.push({
            'last_value1': value1,
            'last_value2': value2,
            'last_value3': value3,
            'last_value4': value4,
            'last_values2': value5,
            'fecha_hora': fecha
        })
    except Exception as e:
        print(f'Error al enviar datos a Firebase: {e}')

def enviar_a_firebase_peligro(value1, value2, value3, value4, value5, descripcion, fecha):
    try:
        # Obtén una referencia a la base de datos de Firebase
        ref = db.reference('/lecturas_peligrosas')  # Ruta en la base de datos de Firebase

        # Envía los datos a la base de datos de Firebase
        ref.push({
            'last_value1': value1,
            'last_value2': value2,
            'last_value3': value3,
            'last_value4': value4,
            'last_values2': value5,
            'descripcion': descripcion,
            'fecha_hora': fecha
        })
    except Exception as e:
        print(f'Error al enviar datos a Firebase: {e}')
# @login_required
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def obtener_datos_de_firebase():
    try:
        ref = db.reference('/lecturas_sensor')
        datos = ref.get()
        return datos
    except Exception as e:
        print(f'Error al obtener datos de Firebase: {e}')
        return None
    
def datos_sensores(request):
    datos_firebase = obtener_datos_de_firebase()
    datos_json=json.dumps(datos_firebase)
    return render(request, 'datos_sensores.html', {'datos_json': datos_json})

def enviar_notificacion_a_todos(titulo, descripcion, tipo_notificacion):
    # Verificar si se ha enviado una notificación recientemente para el mismo tipo
    conn = psycopg2.connect(
        dbname='safeair',
        user='postgres',
        password='root',
        host='localhost',
        port='5432'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT fecha_hora FROM notificaciones_enviadas WHERE titulo = %s AND tipo_notificacion = %s ORDER BY fecha_hora DESC LIMIT 1",
                   (titulo, tipo_notificacion))
    ultimo_envio = cursor.fetchone()

    if ultimo_envio is not None:
        tiempo_transcurrido = timezone.now() - ultimo_envio[0]
        if tiempo_transcurrido < datetime.timedelta(minutes=1):
            print("Ya se envió una notificación del mismo tipo recientemente. Ignorando el nuevo envío.")
            cursor.close()
            conn.close()
            return

    # Tu código para obtener tokens de la base de datos
    cursor.execute("SELECT token FROM usuarios_dispositivo")
    tokens = cursor.fetchall()

    push_service = FCMNotification(api_key="AAAADYvaoJg:APA91bHFyBzKIUnYStu7861SBt4wHgKBmX3pc6cuG6puNSEv0yuKcUcH82GQ3OvdGEr-V_XjfSXWls-puSRTuBfFOX9LYDvd6_sX978WBd-xxPZCfB6aXR5yv8XQzaInDVa2YEs-g6yq")

    for token in tokens:
        try:
            push_service.notify_single_device(
                registration_id=token[0],
                message_title=titulo,
                message_body=descripcion
            )
        except Exception as e:
            print("Error al enviar notificación al token:", token[0], "-", e)

    fecha_hora_actual = timezone.now()
    fecha_hora_formateada = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")
    enviar_notificaciones_firebase(titulo, descripcion, fecha_hora_formateada)
    # Registro de la marca de tiempo de la notificación enviada
    cursor.execute("INSERT INTO notificaciones_enviadas (titulo, descripcion, fecha_hora, tipo_notificacion) VALUES (%s, %s, %s, %s)",
                   (titulo, descripcion, datetime.datetime.now(), tipo_notificacion))
    conn.commit()

    cursor.close()
    conn.close()

def enviar_notificaciones_firebase(titulo, descripcion, fecha):
    try:
        ref = db.reference('/notificaciones') 
        ref.push({
            'titulo': titulo,
            'descripcion': descripcion,
            'fecha_hora': fecha
        })
    except Exception as e:
        print(f'Error al enviar datos a Firebase: {e}')