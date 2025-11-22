#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 10:41:10 2025a

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

def categorias_reportes():
    # crear rutas iniciales
    data = [
        {'nombre':'General'},
    ]

    # Create the DataFrame
    data = pd.DataFrame(data)
    with app.app_context():
        id_usuario=Usuarios.query.filter_by(nombre="Sistema").first().id
        for i in range(len(data)):
            new_record = CategoriasDeReportes(nombre=data['nombre'][i],id_usuario=id_usuario)
            db.session.add(new_record)
        db.session.commit()

def reportes(id_empresa):
    # crear rutas iniciales
    data = [
        {'categoria_de_reporte':'General','nombre':'Reporte de interacciones','descripcion': 'Detalla las interacciones realizadas por analistas','ruta_sql': 'interacciones'},
    ]

    # Create the DataFrame
    data = pd.DataFrame(data)
    with app.app_context():
        id_usuario=Usuarios.query.filter_by(nombre="Sistema").first().id
        for i in range(len(data)):
            categoria=CategoriasDeReportes.query.filter_by(nombre=data['categoria_de_reporte'][i]).first()
            new_record = Reportes(id_categoria_de_reporte=categoria.id,nombre=data['nombre'][i],descripcion=data['descripcion'][i],ruta_sql=data['ruta_sql'][i],id_usuario=id_usuario)
            db.session.add(new_record)
        db.session.commit()

categorias_reportes()
reportes()
