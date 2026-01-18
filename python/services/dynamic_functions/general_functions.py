
from python.models.modelos import *
from sqlalchemy import String, Text, or_,func,Integer, Float, Numeric
from sqlalchemy.sql import case
from flask import session,flash,request
from datetime import date, datetime,timedelta

#####
# funciones auxiliares
#####

def get_all_models():
    """
    Retorna una lista de todos los modelos registrados en SQLAlchemy
    que tienen asignado el atributo __tablename__.
    """
    models = []
    for model in db.Model.registry._class_registry.values():
        if hasattr(model, "__tablename__"):
            models.append(model)
    return models

def cuadrar_balance(id_cuenta):
    cuenta=CuentasDeBanco.query.get(id_cuenta)
    pagos=(db.session.query(func.sum(PagosAdministrativos.importe)).filter(PagosAdministrativos.id_cuenta_de_banco == cuenta.id,PagosAdministrativos.estatus=='Pagado').scalar() or 0)
    ingresos=(db.session.query(func.sum(Ventas.importe)).filter(Ventas.id_cuenta_de_banco == cuenta.id,Ventas.estatus=='Cerrado').scalar() or 0)
    transferencia_salida=(db.session.query(func.sum(TransferenciasDeDinero.importe)).filter(TransferenciasDeDinero.id_cuenta_de_banco_salida == cuenta.id,TransferenciasDeDinero.estatus=='Realizada').scalar() or 0)
    transferencia_entrada = (db.session.query(func.sum(TransferenciasDeDinero.importe)).filter(TransferenciasDeDinero.id_cuenta_de_banco_entrada == cuenta.id,TransferenciasDeDinero.estatus == 'Realizada').scalar()or 0)
    ajustes_salida = (db.session.query(func.sum(AjustesDeDinero.importe)).filter(AjustesDeDinero.id_cuenta_de_banco == cuenta.id,AjustesDeDinero.estatus == 'Realizado',AjustesDeDinero.tipo_de_ajuste == 'Salida').scalar()or 0)
    ajustes_entrada = (db.session.query(func.sum(AjustesDeDinero.importe)).filter(AjustesDeDinero.id_cuenta_de_banco == cuenta.id,AjustesDeDinero.estatus == 'Realizado',AjustesDeDinero.tipo_de_ajuste == 'Entrada').scalar()or 0)

    cuenta.balance=ingresos+transferencia_entrada+ajustes_entrada-pagos-transferencia_salida-ajustes_salida


def actualizar_compra(record):
    productos=ProductosEnCompras.query.filter_by(id_compra=record.id)
    subtotal = 0
    descuento = 0
    for prod in productos:
        if record.estatus in ('En revisión', 'Aprobada', 'Recibida parcial'):
            cantidad = float(str(prod.cantidad_ordenada))
        else:
            cantidad = float(str(prod.cantidad_recibida))
        precio_unitario = float(str(prod.precio_unitario))
        descuento_porcentaje = float(str(prod.descuento_porcentaje))
        prod.subtotal = cantidad * precio_unitario
        descuento += prod.subtotal * descuento_porcentaje / float("100")
        prod.importe_total = prod.subtotal * (float("1") - descuento_porcentaje / float("100"))
        subtotal += prod.subtotal
    record.subtotal=float(subtotal)
    record.descuentos=float(descuento)
    record.importe_total=record.subtotal+float(record.costos_adicionales)-record.descuentos

def calcular_importe_pago(record):
    record.importe=(
                    db.session.query(
                        func.sum(GastosYComprasEnPagos.importe)
                    )
                    .filter(GastosYComprasEnPagos.id_pago == record.id)
                    .scalar()
                    or 0  
                    )
    gastos=Gastos.query.filter(Gastos.id_proveedor==record.id_proveedor,Gastos.estatus!='Pagado',Gastos.estatus!='Cancelado')
    for record in gastos:
        record.importe_pagado=(
                db.session.query(func.sum(GastosYComprasEnPagos.importe))
                .join(PagosAdministrativos, GastosYComprasEnPagos.id_pago == PagosAdministrativos.id)
                .filter(GastosYComprasEnPagos.id_gasto == record.id)
                .filter(PagosAdministrativos.estatus != "Cancelado")
                .scalar()
            ) or 0
    compras=Compras.query.filter(Compras.id_proveedor==record.id_proveedor,Compras.estatus_de_pago!='Pagado',Compras.estatus!='Cancelada')
    for record in compras:
        record.importe_pagado=(
                db.session.query(func.sum(GastosYComprasEnPagos.importe))
                .join(PagosAdministrativos, GastosYComprasEnPagos.id_pago == PagosAdministrativos.id)
                .filter(GastosYComprasEnPagos.id_compra == record.id)
                .filter(PagosAdministrativos.estatus != "Cancelado")
                .scalar()
            ) or 0
        
def actualizar_venta(record):
    record.importe=(db.session.query(func.sum(ServiciosEnVentas.importe)).filter(ServiciosEnVentas.id_venta == record.id).scalar()) or 0    
    record.iva=record.importe*.16
    record.importe_total=record.importe*1.16
