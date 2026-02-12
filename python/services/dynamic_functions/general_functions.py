
from python.models.modelos import *
from sqlalchemy import String, Text, or_,func,Integer, Float, Numeric
from sqlalchemy.sql import case
from flask import session,flash,request
from datetime import date, datetime,timedelta
from config import *
from python.services.system.helper_functions import *

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
    record.subtotal=(db.session.query(func.sum(ServiciosEnVentas.subtotal)).filter(ServiciosEnVentas.id_venta == record.id).scalar()) or 0
    descuento_total=0
    if record.codigo_de_descuento:
        descuento=Descuentos.query.filter_by(estatus='Activo',codigo_de_descuento=record.codigo_de_descuento).first()
        if descuento.tipo_de_descuento=='Importe':
            if descuento.id_servicio and descuento.id_espacio:
                servicio=ServiciosEnVentas.query.filter_by(id_venta=record.id,id_servicio=descuento.id_servicio,id_espacio=descuento.id_espacio).first()
                if servicio:
                    servicio.descuento=descuento.valor
                    servicio.subtotal=servicio.subtotal-servicio.descuento
            descuento_total=descuento.valor
        elif descuento.tipo_de_descuento=='Porcentaje':
            if descuento.id_servicio and descuento.id_espacio:
                servicio=ServiciosEnVentas.query.filter_by(id_venta=record.id,id_servicio=descuento.id_servicio,id_espacio=descuento.id_espacio).first()
                if servicio:
                    servicio.descuento=servicio.subtotal*descuento.valor/100
                    servicio.importe_total=servicio.subtotal-servicio.descuento
                    descuento_total=servicio.descuento
            else:
                descuento_total=record.subtotal*descuento.valor/100
    record.importe_descuento=descuento_total
    record.importe=record.subtotal-record.importe_descuento
    record.iva=(record.importe)*.16
    record.importe_total=(record.importe)*1.16

tabla_isr_2026 = [
    (0.01, 844.59, 0.00, 0.0192),
    (844.60, 7168.51, 16.22, 0.0640),
    (7168.52, 12598.02, 420.95, 0.1088),
    (12598.03, 14644.64, 1011.68, 0.16),
    (14644.65, 17533.64, 1339.14, 0.1792),
    (17533.65, 35362.83, 1856.84, 0.2136),
    (35362.84, 55736.68, 5665.16, 0.2352),
    (55736.69, 106410.50, 10457.09, 0.30),
    (106410.51, 141880.66, 25659.23, 0.32),
    (141880.67, 425641.99, 37009.69, 0.34),
    (425642.00, float("inf"), 133488.54, 0.35),
]

def calcular_isr(sueldo_bruto):
    for inf_lim, sup_lim, cuota, pct in tabla_isr_2026:
        if inf_lim <= sueldo_bruto <= sup_lim:
            excedente = sueldo_bruto - inf_lim
            return round(cuota + excedente * pct, 2)
    return 0

def calcular_imss_basico(sueldo_bruto):
    # ejemplo uso de UMA (actualiza según valor oficial de 2026)
    UMA = 113.14  # debe actualizar al valor final 2026
    sueldo_diario = sueldo_bruto / 30
    excedente = max(0, sueldo_diario - (3 * UMA))
    em = excedente * 0.004 * 30
    iv = sueldo_bruto * 0.00625
    cv = sueldo_bruto * 0.01125
    return round(em + iv + cv, 2)

def calcular_nomina(sueldo_bruto):
    isr = calcular_isr(sueldo_bruto)
    imss = calcular_imss_basico(sueldo_bruto)
    deducciones = round(isr + imss, 2)
    neto = round(sueldo_bruto - deducciones, 2)
    return isr,imss,deducciones,neto