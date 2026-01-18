
from python.models.modelos import *
from sqlalchemy import String, Text, or_,func,Integer, Float, Numeric
from sqlalchemy.sql import case
from flask import session,flash
import re
import json
from datetime import date, datetime
from python.services.dynamic_functions.general_functions import *
from python.services.system.email import *
from python.services.system.helper_functions import *
from config import *

#####
# funciones de formulariosa
#####

HANDLERS = {}

def handler_on_success(*tables):
    def wrapper(fn):
        for t in tables:
            HANDLERS[t] = fn
        return fn
    return wrapper

def on_success(table_name, id):
    handler = HANDLERS.get(table_name)
    if not handler:
        return
    return handler(id)

@handler_on_success('compras')
def compras(id):
    record=Compras.query.get(id)
    actualizar_compra(record)

@handler_on_success('ajustes_de_inventario')
def ajustes_de_inventario(id):
    record=AjustesDeInventario.query.get(id)
    if record.tipo_de_ajuste=='Salida':
        inventario_salida=Inventario.query.filter_by(id_almacen=record.id_almacen,id_producto=record.id_producto).first()
        inventario_salida.cantidad=inventario_salida.cantidad-float(record.cantidad)
        inventario_salida.cantidad_en_transito=inventario_salida.cantidad_en_transito+float(record.cantidad)

@handler_on_success('clientes')
def clientes(id):
    briefs = Briefs.query.filter(Briefs.nombre.in_(BRIEFS_CREACION_CLIENTE)).all()
    for brief in briefs:
        new_record=BriefsDeClientes(
            id_visualizacion=get_id_visualizacion('briefs_de_clientes'),
            id_cliente=id,
            id_brief=brief.id
        )
        db.session.add(new_record)
        db.session.flush()
        preguntas=PreguntasDeBriefs.query.filter_by(id_brief=brief.id).all()
        for pregunta in preguntas:
            new_pregunta=RespuestasBriefsDeClientes(
                id_brief_de_cliente=new_record.id,
                id_pregunta_de_brief=pregunta.id
            )
            db.session.add(new_pregunta)

@handler_on_success('servicios_en_ventas')
def servicios_en_ventas(id):
    record=ServiciosEnVentas.query.get(id)
    precio = PreciosDeServicios.query.filter(
        PreciosDeServicios.id_servicio == record.id_servicio,
        PreciosDeServicios.id_espacio == record.id_espacio
    ).first()
    if precio:
        record.precio_unitario = precio.precio_unitario
        record.id_precio_stripe=precio.id_stripe
    record.importe=record.precio_unitario*record.cantidad
    venta=Ventas.query.get(record.id_venta)
    actualizar_venta(venta)    
