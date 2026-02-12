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

working_directory='/Users/davidcontrerasgarza/Documents/Repositorios_SS/Portal-Minerva-Atelier/'
os.chdir(working_directory)
from app import *
from python.models import *


def brief(nombre,servicio=None):
    data = [
        {'nombre':nombre},
    ]
    data = pd.DataFrame(data)
    with app.app_context():
        id_usuario=Usuarios.query.filter_by(nombre="Sistema").first().id
        for i in range(len(data)):
            if servicio:
                servicio=Servicios.query.filter_by(nombre=servicio).first().id
                new_record = Briefs(id_visualizacion=get_id_visualizacion('briefs'),nombre=data['nombre'][i],id_servicio=servicio,id_usuario=id_usuario)
            else:
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



brief_nombre='Brief funcional'
brief(brief_nombre)
data = [
    {'orden': '1', 'pregunta': '¿Qué espacio necesita tu atención?'},
    {'orden': '2', 'pregunta': '¿Qué tipo de vivienda habitas?'},
    {'orden': '3', 'pregunta': 'Estatus de Vivienda'},
    {'orden': '4', 'pregunta': 'Estado actual del espacio'},
    {'orden': '5', 'pregunta': '¿Para cuándo te gustaría disfrutar de tu espacio terminado?'},
    {'orden': '6', 'pregunta': '¿Cuentas con un presupuesto definido?'},
    {'orden': '7', 'pregunta': '¿Puedes prescindir del espacio en el momento de las modificaciones.'},
    {'orden': '8', 'pregunta': '¿Preséntanos a quienes vivirán en este espacio:'},
    #{'orden': '9', 'pregunta': '¿Quien es la responsable de las siguientes tareas en el hogar'},
    {'orden': '10', 'pregunta': '¿Quién es responsable de limpiar baños?'},
    {'orden': '11', 'pregunta': '¿Quién es responsable de hacer el súper?'},
    {'orden': '12', 'pregunta': '¿Quién es responsable de cocinar?'},
    {'orden': '13', 'pregunta': '¿Quién es responsable de lavar y planchar?'},
    {'orden': '14', 'pregunta': '¿Quién es responsable de aspirar y trapear?'},
    {'orden': '15', 'pregunta': '¿Quién es responsable de la organización del hogar?'},
    {'orden': '16', 'pregunta': '¿Quién es responsable de la limpieza profunda?'},
    {'orden': '17', 'pregunta': '¿Quién es responsable de pagar servicios?'},
    {'orden': '18', 'pregunta': '¿Quién es responsable de sacar la basura?'},
    {'orden': '19', 'pregunta': '¿Quién es responsable de regar plantas?'},
    {'orden': '20', 'pregunta': '¿Quién es responsable de las tareas de la mascota?'},
    {'orden': '21', 'pregunta': '¿Quién es responsable de decorar?'},
    {'orden': '22', 'pregunta': '¿Quién es responsable de la limpieza de exteriores?'},
    {'orden': '23', 'pregunta': '¿Quién es responsable de limpiar autos?'},    
    {'orden': '24', 'pregunta': '¿Tienes mascotas?'},
    {'orden': '25', 'pregunta': '¿Hay alguna condición de salud, neurodivergencia o discapacidad que te gustaría compartir con nosotros para diseñar de forma más empática y considerada?'},
    {'orden': '26', 'pregunta': 'Cuéntanos como y para que uses este espacio durante el día. ¿tiene otros usos?'},
    {'orden': '27', 'pregunta': 'Sientes hay cosas que estorban tu vida diaria en este espacio.'},
    {'orden': '28', 'pregunta': '¿Cuanto almacenamiento necesitas?'},
    {'orden': '29', 'pregunta': '¿Qué objetos debemos incluir sí o sí? No te olvides de mencionar recuerdos fotografías, arte, objetos religiosos, plantas, etc.'},
    {'orden': '30', 'pregunta': '¿Qué es lo que No te gustaría incluir en este proyecto?'},
    {'orden': '31', 'pregunta': 'Me preocupa que:'},
]
preguntas(data,brief_nombre)

# 1. ¿Qué espacio necesita tu atención?
data = [
    {'opcion_de_respuesta':'A','respuesta':'Recibidor'},
    {'opcion_de_respuesta':'B','respuesta':'Sala'},
    {'opcion_de_respuesta':'C','respuesta':'Comedor'},
    {'opcion_de_respuesta':'D','respuesta':'Sala de TV'},
    {'opcion_de_respuesta':'E','respuesta':'Estudio'},
    {'opcion_de_respuesta':'F','respuesta':'Dormitorios'},
    {'opcion_de_respuesta':'G','respuesta':'Baño'},
    {'opcion_de_respuesta':'H','respuesta':'Terraza'},
    {'opcion_de_respuesta':'I','respuesta':'Lavandería'},
]
respuestas(data, brief_nombre, 1)

# 2. ¿Qué tipo de vivienda habitas?
data = [
    {'opcion_de_respuesta':'A','respuesta':'Casa'},
    {'opcion_de_respuesta':'B','respuesta':'Departamento'},
    {'opcion_de_respuesta':'C','respuesta':'Habitación'},
    {'opcion_de_respuesta':'D','respuesta':'Estudio'},
]
respuestas(data, brief_nombre, 2)

# 3. Estatus de Vivienda
data = [
    {'opcion_de_respuesta':'A','respuesta':'Rentada'},
    {'opcion_de_respuesta':'B','respuesta':'Comprada'},
]
respuestas(data, brief_nombre, 3)

# 4. Estado actual del espacio
data = [
    {'opcion_de_respuesta':'A','respuesta':'Vacío'},
    {'opcion_de_respuesta':'B','respuesta':'Parcialmente lleno'},
    {'opcion_de_respuesta':'C','respuesta':'Lleno'},
]
respuestas(data, brief_nombre, 4)

# 5. ¿Para cuándo te gustaría disfrutar de tu espacio terminado?
data = [
    {'opcion_de_respuesta':'A','respuesta':'Menos de un mes'},
    {'opcion_de_respuesta':'B','respuesta':'Entre un mes y seis meses'},
    {'opcion_de_respuesta':'C','respuesta':'Entre seis meses y un año'},
]
respuestas(data, brief_nombre, 5)

# 6. ¿Cuentas con un presupuesto definido?
data = [
    {'opcion_de_respuesta':'A','respuesta':'Sí, ¿cuál es?'},
    {'opcion_de_respuesta':'B','respuesta':'No, mientras pase la tarjeta'},
]
respuestas(data, brief_nombre, 6)

# 7. ¿Puedes prescindir del espacio en el momento de las modificaciones?
data = [
    {'opcion_de_respuesta':'A','respuesta':'Sí'},
    {'opcion_de_respuesta':'B','respuesta':'No'},
]
respuestas(data, brief_nombre, 7)


# 10. ¿Tienes mascotas?
data = [
    {'opcion_de_respuesta':'A','respuesta':'No'},
    {'opcion_de_respuesta':'B','respuesta':'Perros'},
    {'opcion_de_respuesta':'C','respuesta':'Peces'},
    {'opcion_de_respuesta':'D','respuesta':'Hámster'},
    {'opcion_de_respuesta':'E','respuesta':'Otros'},
]
respuestas(data, brief_nombre, 24)

# 13. ¿Sientes que hay cosas que estorban tu vida diaria en este espacio?
data = [
    {'opcion_de_respuesta':'A','respuesta':'Sí'},
    {'opcion_de_respuesta':'B','respuesta':'No'},
]
respuestas(data, brief_nombre, 27)

# 14. ¿Cuánto almacenamiento necesitas?
data = [
    {'opcion_de_respuesta':'A','respuesta':'Poco'},
    {'opcion_de_respuesta':'B','respuesta':'Medio'},
    {'opcion_de_respuesta':'C','respuesta':'Mucho'},
]
respuestas(data, brief_nombre, 28)

brief_nombre='Pequeños detalles' # glowup
brief(brief_nombre,'Glow Up')
data = [
    {'orden': '1', 'pregunta': 'Mi Instagram es:'},
    {'orden': '2', 'pregunta': '¿Tienes algún platillo favorito o tipo de cocina que te apasione? ¿Qué te gusta de su sabor o estilo de preparación?'},
    {'orden': '3', 'pregunta': '¿Cómo describirías tu estilo de vestir en tu día a día y qué buscas expresar con él?'},
    {'orden': '4', 'pregunta': '¿Cuáles son tus tres películas favoritas? ¿Por qué?'},
    {'orden': '5', 'pregunta': 'Si pudieras despertar mañana en un lugar completamente nuevo, ¿cuál sería el hotel en el que abrirías los ojos y qué ciudad estaría esperándote al salir?'},
    {'orden': '6', 'pregunta': '¿Existe algún artista o movimiento artístico que te guste? ¿Qué te atrae de ese estilo o concepto?'},
    {'orden': '7', 'pregunta': '¿Qué te inspira más: la naturaleza, la ciudad o un equilibrio entre ambas?'},
    {'orden': '8', 'pregunta': '¿Cuáles son tus principales pasatiempos y qué es lo que más te apasiona de ellos?'},
    {'orden': '9', 'pregunta': '¿Cómo te sientes cuando tu entorno no está tan ordenado o limpio? ¿De qué manera reaccionas ante ese desorden?'},
    {'orden': '10', 'pregunta': 'Si pudieras diseñar tu propio parque temático basado en todo lo que te divierte, ¿qué atracciones o experiencias no podrían faltar?'},
    {'orden': '11', 'pregunta': 'Si tu vida fuera una serie, ¿cuál sería?'},
    {'orden': '12', 'pregunta': 'Si pudieras diseñar tu propio parque temático basado en todo lo que te divierte, ¿qué atracciones o experiencias no podrían faltar?'},
    {'orden': '13', 'pregunta': '¿De qué manera gestionas tus gastos e ingresos?'},
    {'orden': '14', 'pregunta': '¿Cómo te describirías trabajando en equipo y qué esperas de nosotros en ese proceso?'},
    {'orden': '15', 'pregunta': 'Menciona tres cosas que tú y MINERVA ATELIER tienen en común (valores, estilo, filosofía).'}
]
preguntas(data,brief_nombre)

brief_nombre='La casa que eres' # find your style
brief(brief_nombre,'Find Your Style')
data = [
    {'orden': '1', 'pregunta': 'Mi Instagram es:'},
    {'orden': '2', 'pregunta': '¿Tienes algún platillo favorito o tipo de cocina que te apasione? ¿Qué te gusta de su sabor o estilo de preparación?'},
    {'orden': '3', 'pregunta': '¿Cómo describirías tu estilo de vestir en tu día a día y qué buscas expresar con él?'},
    {'orden': '4', 'pregunta': '¿Cuáles son tus tres películas favoritas? ¿Por qué?'},
    {'orden': '5', 'pregunta': 'Si pudieras despertar mañana en un lugar completamente nuevo, ¿cuál sería el hotel en el que abrirías los ojos y qué ciudad estaría esperándote al salir?'},
    {'orden': '6', 'pregunta': '¿Existe algún artista o movimiento artístico que te guste? ¿Qué te atrae de ese estilo o concepto?'},
    {'orden': '7', 'pregunta': '¿Qué te inspira más: la naturaleza, la ciudad o un equilibrio entre ambas?'},
    {'orden': '8', 'pregunta': '¿Cuáles son tus principales pasatiempos y qué es lo que más te apasiona de ellos?'},
    {'orden': '9', 'pregunta': '¿Cómo te sientes cuando tu entorno no está tan ordenado o limpio? ¿De qué manera reaccionas ante ese desorden?'},
    {'orden': '10', 'pregunta': 'Si pudieras diseñar tu propio parque temático basado en todo lo que te divierte, ¿qué atracciones o experiencias no podrían faltar?'},
    {'orden': '11', 'pregunta': 'Si tu vida fuera una serie, ¿cuál sería?'},
    {'orden': '12', 'pregunta': 'Si pudieras diseñar tu propio parque temático basado en todo lo que te divierte, ¿qué atracciones o experiencias no podrían faltar?'},
    {'orden': '13', 'pregunta': '¿De qué manera gestionas tus gastos e ingresos?'},
    {'orden': '14', 'pregunta': '¿Cómo te describirías trabajando en equipo y qué esperas de nosotros en ese proceso?'},
    {'orden': '15', 'pregunta': 'Menciona tres cosas que tú y MINERVA ATELIER tienen en común (valores, estilo, filosofía).'},
    {'orden': '16', 'pregunta': '¿Qué te emociona más: dominar una rutina o entrar a algo nuevo?'},
    {'orden': '17', 'pregunta': '¿Qué tan cómodo/a te sientes diciendo “no” sin explicar demasiado?'},
    {'orden': '18', 'pregunta': '¿Qué te hace sentir orgulloso/a de ti? Compártenos 2 ejemplos.'},
    {'orden': '19', 'pregunta': 'Piensa en el momento del día en que te sientes más conectado/a contigo mismo/a. ¿Qué estás haciendo y cómo se siente?'},
    {'orden': '20', 'pregunta': '¿Qué relación quieres tener con el disfrute: más disciplina, más libertad o más equilibrio?'},
    {'orden': '21', 'pregunta': '¿Qué te frustra más: que no te escuchen o que no te entiendan? ¿Por qué?'},
    {'orden': '22', 'pregunta': '¿Quiénes consideras tu mayor apoyo? ¿Qué crees que hace especial esa conexión?'},
    {'orden': '23', 'pregunta': 'Si pudieras elegir a cualquier persona famosa en el mundo, viva o muerta, ¿a quién invitarías a cenar? ¿Y qué le preguntarías?'},
    {'orden': '24', 'pregunta': '¿Qué tipo de cambios te entusiasman y cuáles te asustan?'},
    {'orden': '25', 'pregunta': 'Si supieras que en un año vas a morir repentinamente, ¿cambiarías algo en tu forma de vivir? ¿Por qué?'},
    {'orden': '26', 'pregunta': '¿Hay algo que sueñes con hacer desde hace mucho tiempo? ¿Por qué no lo has hecho todavía?'},
    {'orden': '27', 'pregunta': '¿Cómo ves tu rutina diaria en 5 años?'},
    {'orden': '28', 'pregunta': '¿Tu familia es cercana? Cuéntanos un poco sobre la dinámica actual.'},
    {'orden': '29', 'pregunta': '¿Cuándo fue la última vez que cambiaste algo de ti solo para sentirte aceptado/a?'},
    {'orden': '30', 'pregunta': '¿Te gustaría ser famoso/a? ¿De qué forma?'},
    {'orden': '31', 'pregunta': 'Tu casa, que contiene todo lo que posees, se incendia. Salvas a tus seres queridos y mascotas; te queda tiempo para salvar un solo objeto. ¿Cuál sería? ¿Por qué?'},
    {'orden': '32', 'pregunta': '¿Cuáles son tus tres principales razones para vivir en este momento?'},
    {'orden': '33', 'pregunta': '¿Qué opinas del fast fashion y sus consecuencias?'},
    {'orden': '34', 'pregunta': '¿Qué costumbre de tu familia o cultura te gustaría mantener viva en tu vida? Cuéntanos un poco más.'},
    {'orden': '35', 'pregunta': 'Es tu turno de organizar una reunión con tus amigos, ¿qué haces más naturalmente?'},
]
preguntas(data,brief_nombre)

data = [
    {'opcion_de_respuesta':'A','respuesta':'Ok, hacemos esto, aquí, a tal hora. ¿Quién se apunta?'},
    {'opcion_de_respuesta':'B','respuesta':'¿Qué les late más? Va a estar buenísimo.'},
    {'opcion_de_respuesta':'C','respuesta':'Yo me ajusto a lo que decidan; con que estemos a gusto y sin drama, perfecto.'},
    {'opcion_de_respuesta':'D','respuesta':'Ordeno todo: confirmo detalles, hago lista y dejo claro el plan para que no falle.'},
]
respuestas(data, brief_nombre, 35)

brief_nombre='La casa que eres +' # find your style
brief(brief_nombre,'Find Your Style')
data = [
    {'orden': '1', 'pregunta': '¿Qué te emociona más: dominar una rutina o entrar a algo nuevo?'},
    {'orden': '2', 'pregunta': '¿Qué tan cómodo/a te sientes diciendo “no” sin explicar demasiado?'},
    {'orden': '3', 'pregunta': '¿Qué te hace sentir orgulloso/a de ti? Compártenos 2 ejemplos.'},
    {'orden': '4', 'pregunta': 'Piensa en el momento del día en que te sientes más conectado/a contigo mismo/a. ¿Qué estás haciendo y cómo se siente?'},
    {'orden': '5', 'pregunta': '¿Qué relación quieres tener con el disfrute: más disciplina, más libertad o más equilibrio?'},
    {'orden': '6', 'pregunta': '¿Qué te frustra más: que no te escuchen o que no te entiendan? ¿Por qué?'},
    {'orden': '7', 'pregunta': '¿Quiénes consideras tu mayor apoyo? ¿Qué crees que hace especial esa conexión?'},
    {'orden': '8', 'pregunta': 'Si pudieras elegir a cualquier persona famosa en el mundo, viva o muerta, ¿a quién invitarías a cenar? ¿Y qué le preguntarías?'},
    {'orden': '9', 'pregunta': '¿Qué tipo de cambios te entusiasman y cuáles te asustan?'},
    {'orden': '10', 'pregunta': 'Si supieras que en un año vas a morir repentinamente, ¿cambiarías algo en tu forma de vivir? ¿Por qué?'},
    {'orden': '11', 'pregunta': '¿Hay algo que sueñes con hacer desde hace mucho tiempo? ¿Por qué no lo has hecho todavía?'},
    {'orden': '12', 'pregunta': '¿Cómo ves tu rutina diaria en 5 años?'},
    {'orden': '13', 'pregunta': '¿Tu familia es cercana? Cuéntanos un poco sobre la dinámica actual.'},
    {'orden': '14', 'pregunta': '¿Cuándo fue la última vez que cambiaste algo de ti solo para sentirte aceptado/a?'},
    {'orden': '15', 'pregunta': '¿Te gustaría ser famoso/a? ¿De qué forma?'},
    {'orden': '16', 'pregunta': 'Tu casa, que contiene todo lo que posees, se incendia. Salvas a tus seres queridos y mascotas; te queda tiempo para salvar un solo objeto. ¿Cuál sería? ¿Por qué?'},
    {'orden': '17', 'pregunta': '¿Cuáles son tus tres principales razones para vivir en este momento?'},
    {'orden': '18', 'pregunta': '¿Qué opinas del fast fashion y sus consecuencias?'},
    {'orden': '19', 'pregunta': '¿Qué costumbre de tu familia o cultura te gustaría mantener viva en tu vida? Cuéntanos un poco más.'},
    {'orden': '20', 'pregunta': 'Es tu turno de organizar una reunión con tus amigos, ¿qué haces más naturalmente?'},
]
preguntas(data,brief_nombre)

data = [
    {'opcion_de_respuesta':'A','respuesta':'Ok, hacemos esto, aquí, a tal hora. ¿Quién se apunta?'},
    {'opcion_de_respuesta':'B','respuesta':'¿Qué les late más? Va a estar buenísimo.'},
    {'opcion_de_respuesta':'C','respuesta':'Yo me ajusto a lo que decidan; con que estemos a gusto y sin drama, perfecto.'},
    {'opcion_de_respuesta':'D','respuesta':'Ordeno todo: confirmo detalles, hago lista y dejo claro el plan para que no falle.'},
]
respuestas(data, brief_nombre, 20)
