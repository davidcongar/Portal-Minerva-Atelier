#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 10:41:10 2025

@author: davidcontrerasgarza
"""

import pandas as pd 
import json
from datetime import datetime
import numpy as np
import os

working_directory='/Users/davidcontreras/Documents/Repositorios_SS/Portal-Minerva-Atelier/'
os.chdir(working_directory)
from app import *
from python.models import *


def brief(nombre):
    data = [
        {'nombre':nombre},
    ]
    data = pd.DataFrame(data)
    with app.app_context():
        id_usuario=Usuarios.query.filter_by(nombre="Sistema").first().id
        for i in range(len(data)):
            new_record = Briefs(id_visualizacion=get_id_visualizacion('briefs'),nombre=data['nombre'][i],id_usuario=id_usuario)
            db.session.add(new_record)
        db.session.commit()

def preguntas(data,nombre):
    data = pd.DataFrame(data)
    with app.app_context():
        id_brief=Briefs.query.filter_by(nombre=nombre).first().id
        id_usuario=Usuarios.query.filter_by(nombre="Sistema").first().id
        for i in range(len(data)):
            new_record = PreguntasDeBriefs(id_visualizacion=get_id_visualizacion('preguntas_de_briefs'),id_brief=id_brief,pregunta=data['pregunta'][i],orden=data['orden'][i],id_usuario=id_usuario)
            db.session.add(new_record)
        db.session.commit()

def respuestas(data,nombre,orden):
    data = pd.DataFrame(data)
    with app.app_context():
        id_brief=Briefs.query.filter_by(nombre=nombre).first().id
        id_pregunta=PreguntasDeBriefs.query.filter_by(id_brief=id_brief,orden=orden).first().id
        id_usuario=Usuarios.query.filter_by(nombre="Sistema").first().id
        for i in range(len(data)):
            new_record = RespuestasDePreguntasDeBriefs(id_visualizacion=get_id_visualizacion('respuestas_de_preguntas_de_briefs'),id_pregunta_de_brief=id_pregunta,opcion_de_respuesta=data['opcion_de_respuesta'][i],respuesta=data['respuesta'][i],id_usuario=id_usuario)
            db.session.add(new_record)
        db.session.commit()

brief_nombre='¿Hacemos match?'
brief(brief_nombre)
data = [
    {'orden': '1', 'pregunta': '¿Te esforzarías para que tu hogar sea un reflejo profundo de quién eres, en lugar de un espacio solo funcional y estético sin carga emocional?'},
    {'orden': '2', 'pregunta': 'Si diseñar tu hogar significara explorar tu propia historia para crear un espacio que realmente te represente. ¿Seguirías adelante en el proceso, aunque eso signifique salir de tu zona de confort?'},
    {'orden': '3', 'pregunta': '¿Consideras que un presupuesto en diseño de interiores es una inversión en tu bienestar y calidad de vida, más que un gasto superficial?'},
    {'orden': '4', 'pregunta': 'Si diseñar tu espacio de manera consciente y con calidad requiere de una inversión significativa, estarías dispuesto a priorizarlo, aunque eso signifique no optar por soluciones descartables y esperar más tiempo para obtener un resultado completo. '},
    {'orden': '5', 'pregunta': '¿Te sientes cómodo/a con la idea de ser tú quien implemente físicamente las recomendaciones y cambios en tu espacio, en lugar de recibir un producto final ya ejecutado?'},
    {'orden': '6', 'pregunta': 'Si te propusiéramos opciones de mobiliario y decoración que fomenten el comercio local o la sustentabilidad, ¿estarías dispuesto/a a priorizarlas sobre soluciones masivas y comerciales?'},
]
preguntas(data,brief_nombre)
data = [
    {'opcion_de_respuesta':'A','respuesta':'¡Claro!'},
    {'opcion_de_respuesta':'B','respuesta':'No tanto'},
]
respuestas(data,brief_nombre,1)
data = [
    {'opcion_de_respuesta':'A','respuesta':'Sin problema'},
    {'opcion_de_respuesta':'B','respuesta':'No, no me gusta este acercamiento'},
]
respuestas(data,brief_nombre,2)
data = [
    {'opcion_de_respuesta':'A','respuesta':'Sí, es una gran inversión'},
    {'opcion_de_respuesta':'B','respuesta':'No, es superficial'},
]
respuestas(data,brief_nombre,3)
data = [
    {'opcion_de_respuesta':'A','respuesta':'Totalmente!'},
    {'opcion_de_respuesta':'B','respuesta':'No realmente'},
]
respuestas(data,brief_nombre,4)
data = [
    {'opcion_de_respuesta':'A','respuesta':'Si, me siento bien con eso'},
    {'opcion_de_respuesta':'B','respuesta':'No, prefiero que alguien mas lo haga'},
]
respuestas(data,brief_nombre,5)
data = [
    {'opcion_de_respuesta':'A','respuesta':'Sin problema'},
    {'opcion_de_respuesta':'B','respuesta':'No, me gusta mas lo comercial'},
]
respuestas(data,brief_nombre,6)

