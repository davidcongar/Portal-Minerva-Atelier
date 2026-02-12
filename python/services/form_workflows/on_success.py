
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
from python.services.stripe import *
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

@handler_on_success('precios_de_servicios')
def precios_de_servicios(id):
    create_product(id)
    create_price(id)

@handler_on_success('descuentos')
def descuentos(id):
    create_coupon(id)

@handler_on_success('comentarios_de_clientes_de_actividades')
def comentarios_de_clientes_de_actividades(id):
    record=ComentariosDeClientesDeActividades.query.get(id)
    actividad=Actividades.query.get(record.id_actividad)
    actividad.estatus='Con cambios'

@handler_on_success('sueldos_de_integrantes')
def sueldos_de_integrantes(id):
    record=SueldosDeIntegrantes.query.get(id)
    isr,imss,deducciones,neto=calcular_nomina(record.sueldo_bruto)
    record.deduccion_isr=isr
    record.deduccion_imss=imss
    record.total_deducciones=deducciones
    record.sueldo_neto=neto

@handler_on_success('pagos_de_nomina')
def pagos_de_nomina(id):
    pago=PagosDeNomina.query.get(id)
    sueldos=SueldosDeIntegrantes.query.filter_by(estatus='Activo').all()
    for sueldo in sueldos:
        new=SueldosPagadosEnNomina(
            id_visualizacion=get_id_visualizacion('sueldos_pagados_en_nomina'),
            id_pago_de_nomina=id,
            id_integrante=sueldo.id_integrante,
            sueldo_bruto=sueldo.sueldo_bruto,
            sueldo_bruto_real=sueldo.sueldo_bruto,
            deduccion_imss=sueldo.deduccion_imss,
            deduccion_isr=sueldo.deduccion_isr,
            total_deducciones=sueldo.total_deducciones,
            sueldo_neto=sueldo.sueldo_neto,
        )
        db.session.add(new)
    db.session.flush()
    pago.importe_total=(db.session.query(func.sum(SueldosPagadosEnNomina.sueldo_neto)).filter(SueldosPagadosEnNomina.id_pago_de_nomina == id).scalar() or 0)

@handler_on_success('sueldos_pagados_en_nomina')
def sueldos_pagados_en_nomina(id):
    record=SueldosPagadosEnNomina.query.get(id)
    pago=PagosDeNomina.query.get(record.id_pago_de_nomina)
    sueldo=SueldosDeIntegrantes.query.filter_by(estatus='Activo',id_integrante=record.id_integrante).first()
    if sueldo:
        record.sueldo_bruto=sueldo.sueldo_bruto
        record.sueldo_bruto_real=sueldo.sueldo_bruto
        record.deduccion_imss=sueldo.deduccion_imss
        record.deduccion_isr=sueldo.deduccion_isr
        record.total_deducciones=sueldo.total_deducciones
        record.sueldo_neto=sueldo.sueldo_neto
    db.session.flush()
    pago.importe_total=(db.session.query(func.sum(SueldosPagadosEnNomina.sueldo_neto)).filter(SueldosPagadosEnNomina.id_pago_de_nomina == pago.id).scalar() or 0)
