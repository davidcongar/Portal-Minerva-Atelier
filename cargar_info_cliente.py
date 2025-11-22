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

working_directory='/Users/davidcontreras/Documents/Repositorios_SS/nombre-app/'
os.chdir(working_directory)
from app import *
from python.models import *
from python.services.system.helper_functions import get_model_by_name

id_empresa=''

def cargar(path,table_name,id_empresa):
    df=pd.read_excel(path)
    with app.app_context():
        id_usuario = Usuarios.query.filter_by(nombre="Sistema").first().id
        empresa_id = Empresas.query.get(id_empresa).id
        model=get_model_by_name(table_name)
        for _, row in df.iterrows():
            record_data = row.to_dict()
            # inject the fixed values
            record_data["id_empresa"] = empresa_id
            record_data["id_usuario"] = id_usuario
            # create the model instance dynamically
            new_record = model(**record_data)
            db.session.add(new_record)

        db.session.commit()

cargar('./informacion_inicial/nikky_lab/comisiones_de_empleados.xlsx','comisiones_de_empleados',id_empresa)