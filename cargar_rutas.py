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


def rutas_inciales():
    # crear rutas iniciales
    data = [
        {'categoria':'Sistema','nombre': 'Acceso total', 'ruta': '/'},
        {'categoria':'Módulos','nombre': 'Archivos', 'ruta': '/files'},
        {'categoria':'Módulos','nombre': 'Auditoría', 'ruta': '/dynamic/logs_auditoria'},
        {'categoria':'Módulos','nombre': 'Dashboard operativo', 'ruta': '/dashboards/operative'},
        {'categoria':'Módulos','nombre': 'Dashboard estratégico', 'ruta': '/dashboards/strategic'},
        {'categoria':'Módulos','nombre': 'Reportes', 'ruta': '/dynamic/reportes'},
        {'categoria':'Módulos','nombre': 'Permisos', 'ruta': '/access_control'},
        {'categoria':'Tableros y reportes','nombre': 'SQL Reportes', 'ruta': '/report_queries'},
        {'categoria':'Tableros y reportes','nombre': 'SQL Tableros', 'ruta': '/dashboard_queries'},

    ]

    # Create the DataFrame
    rutas = pd.DataFrame(data)
    with app.app_context():
        id_usuario=Usuarios.query.filter_by(nombre="Sistema").first().id
        for i in range(len(rutas)):
            new_record = Rutas(categoria=rutas['categoria'][i],nombre=rutas['nombre'][i],ruta=rutas['ruta'][i],id_usuario=id_usuario)
            db.session.add(new_record)
        db.session.commit()

# funcion para crear rutas bases de tablas dinamicas
def crear_rutas_base(nombre_tabla):
    ruta='/dynamic/'+nombre_tabla.lower()
    data = [
        {'categoria':'Módulos','nombre': 'Acceso total '+nombre_tabla.replace('_',' '), 'ruta': ruta},
        {'categoria':'Acciones','nombre': 'Visualizar tabla de '+nombre_tabla.replace('_',' '), 'ruta': ruta+'/view'},
        {'categoria':'Acciones','nombre': 'Visualizar datos de '+nombre_tabla.replace('_',' '), 'ruta': ruta+'/data'},
        {'categoria':'Acciones','nombre': 'Visualizar formulario de '+nombre_tabla.replace('_',' '), 'ruta': ruta+'/form'},
        {'categoria':'Acciones','nombre': 'Registrar información en '+nombre_tabla.replace('_',' '), 'ruta': ruta+'/'+'add'},
        {'categoria':'Acciones','nombre': 'Editar información en '+nombre_tabla.replace('_',' '), 'ruta': ruta+'/edit'},
        {'categoria':'Acciones','nombre': 'Eliminar información en '+nombre_tabla.replace('_',' '), 'ruta': ruta+'/delete'},
        {'categoria':'Acciones','nombre': 'Acceso a visulizar archivos '+nombre_tabla.replace('_',' '), 'ruta': ruta+'/files'}
    ]
    rutas = pd.DataFrame(data)
    with app.app_context():
        id_usuario=Usuarios.query.filter_by(nombre="Sistema").first().id
        for i in range(len(rutas)):
            new_record = Rutas(categoria=rutas['categoria'][i],nombre=rutas['nombre'][i],ruta=rutas['ruta'][i],id_usuario=id_usuario)
            db.session.add(new_record)
        db.session.commit()

# funcion para crear flujos de modulos
def crear_ruta(blueprint,actions):
    ruta='/'+blueprint
    data=[{'categoria':'Flujos','nombre': 'Acceso a total a flujos: '+blueprint.replace('_',' '), 'ruta': ruta}]
    for i in actions:
        new_route={'categoria':'Flujos','nombre': 'Acceso a '+i+' en '+blueprint.replace('_',' '), 'ruta': ruta+'/'+i}
        data.append(new_route)

    rutas = pd.DataFrame(data)
    with app.app_context():
        id_usuario=Usuarios.query.filter_by(nombre="Sistema").first().id
        for i in range(len(rutas)):
            new_record = Rutas(categoria=rutas['categoria'][i],nombre=rutas['nombre'][i],ruta=rutas['ruta'][i],id_usuario=id_usuario)
            db.session.add(new_record)
        db.session.commit()

# funcion para crear rutas de formularios
def crear_admin_empresa():
    with app.app_context():
        if db.session.is_active:
            db.session.rollback()
        #rol
        rol = [
            {'id_visualizacion':int(1),'nombre': 'Sistema', 'estatus': 'Activo'}
        ]
        rol = pd.DataFrame(rol)
        for i in range(len(rol)):
            new_record = Roles(id_visualizacion=int(rol['id_visualizacion'][i]),nombre=rol['nombre'][i],estatus=rol['estatus'][i])
            db.session.add(new_record)
        # usuario admin
        usuario = [
            {'id_visualizacion':int(1),'nombre': 'Sistema','correo_electronico':'david.contreras@snappsolutions.com','contrasena':'123','ultimo_cambio_de_contrasena':'2025-10-09','estatus': 'Activo'}
        ]
        usuario = pd.DataFrame(usuario)
        for i in range(len(usuario)):
            new_record = Usuarios(id_visualizacion=int(usuario['id_visualizacion'][i]),ultimo_cambio_de_contrasena=usuario['ultimo_cambio_de_contrasena'][i],nombre=usuario['nombre'][i],correo_electronico=usuario['correo_electronico'][i],contrasena=usuario['contrasena'][i],estatus=usuario['estatus'][i])
            db.session.add(new_record)
        db.session.commit()

def agregar_acceso_admin():
    with app.app_context():
        id_rol=Roles.query.filter_by(nombre="Sistema").first().id
        id_ruta=Rutas.query.filter_by(ruta="/").first().id
        rol = Roles.query.get(id_rol)
        ruta = Rutas.query.get(id_ruta)
        rol.rutas.append(ruta)
        usuario=Usuarios.query.filter_by(nombre="Sistema").first()
        usuario.id_rol=rol.id
        db.session.commit()
'''

crear_admin_empresa()
rutas_inciales()
'''

agregar_acceso_admin()
'''

crear_rutas_base('usuarios')
crear_rutas_base('roles')
crear_rutas_base('archivos')
crear_rutas_base('proveedores')
crear_rutas_base('categorias_de_gastos')
crear_rutas_base('gastos')
crear_rutas_base('gastos_recurrentes')
crear_rutas_base('precios_de_proveedores')
crear_rutas_base('compras')
crear_rutas_base('productos_en_compras')
crear_rutas_base('servicios')
crear_rutas_base('precios_de_servicios')
crear_rutas_base('facturas')
crear_rutas_base('servicios_en_facturas')
crear_rutas_base('cotizaciones')
crear_rutas_base('detalle_de_cotizaciones')

crear_rutas_base('almacenes')
crear_rutas_base('categorias_de_productos')
crear_rutas_base('productos')
crear_rutas_base('inventario')
crear_rutas_base('recepciones_de_compras')
crear_rutas_base('productos_en_recepciones_de_ordenes_de_compra')
crear_rutas_base('ajustes_de_inventario')
crear_rutas_base('transferencias_de_inventario')
crear_rutas_base('productos_en_transferencias_de_inventario')
crear_rutas_base('envios')
crear_rutas_base('productos_en_envios')

crear_rutas_base('cuentas_de_banco')
crear_rutas_base('pagos_administrativos')
crear_rutas_base('gastos_y_compras_en_pagos')
crear_rutas_base('transferencias_de_dinero')
crear_rutas_base('ajustes_de_dinero')
crear_rutas_base('ingresos')
crear_rutas_base('facturas_en_ingresos')

crear_rutas_base('clientes')
crear_rutas_base('briefs')
crear_rutas_base('preguntas_de_briefs')
crear_rutas_base('agenda')

crear_rutas_base('proyectos')
crear_rutas_base('actividades_base')
crear_rutas_base('actividades')
crear_rutas_base('preguntas_de_calidad_de_servicio')
crear_rutas_base('calidad_de_servicio_de_proyectos')
crear_rutas_base('respuestas_calidad_de_servicio')
crear_rutas_base('preguntas_de_encuesta_de_satisfaccion')
crear_rutas_base('encuesta_de_satisfaccion_de_proyectos')
crear_rutas_base('respuestas_encuesta_de_satisfaccion')
crear_rutas_base('briefs_de_clientes')
crear_rutas_base('respuestas_briefs_de_clientes')

crear_rutas_base('puestos')
crear_rutas_base('integrantes')
crear_rutas_base('pagos_de_nomina')
crear_rutas_base('sueldos_pagados_en_nomina')
crear_rutas_base('sueldos_de_integrantes')

crear_rutas_base('ventas')

actions={'contacto_inicial','en_proceso','perdido','activo','finalizar','cancelar'}
crear_ruta('clientes',actions)
actions={'pendiente','cancelada','finalizada'}
crear_ruta('interaccion',actions)
actions={}
crear_ruta('user_guide',actions)
'''