
from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for,session

from python.models import db
from python.models.modelos import *
from python.services.system.authentication import *
from sqlalchemy.orm import joinedload
from sqlalchemy import String, Text, or_,func,desc
from datetime import date,timedelta
from python.services.system.helper_functions import *
from python.services.dynamic_functions.general_functions import *


pagos_administrativos_bp = Blueprint("pagos_administrativos", __name__,url_prefix="/pagos_administrativos")

@pagos_administrativos_bp.route("/aprobar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def aprobar(id):
    pago=PagosAdministrativos.query.get(id)
    if pago.estatus=='En revisión':
        if pago.importe==0:
            flash('El pago tiene importe 0. Favor de revisar','info')
            return redirect(url_for('dynamic.table_view', table_name='pagos_administrativos'))
        pago.estatus="Aprobado"
        db.session.commit()
        flash('El pago ha sido Aprobado.','success')
    return redirect(url_for('dynamic.table_view', table_name='pagos_administrativos'))

@pagos_administrativos_bp.route("/pagar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def pagar(id):
    pago=PagosAdministrativos.query.get(id)
    if pago.estatus=='Aprobado':
        # revisar balance
        cuenta=CuentasDeBanco.query.get(pago.id_cuenta_de_banco)
        if pago.importe>cuenta.balance:
            flash(f'El balance de la cuenta, {money_format(cuenta.balance)}, es menor al importe del pago. Favor de revisar.','info')
            return redirect(url_for('dynamic.table_view', table_name='pagos_administrativos'))
        pago.estatus="Pagado"
        compras_gastos=GastosYComprasEnPagos.query.filter_by(id_pago=pago.id)
        for record in compras_gastos:
            if record.id_gasto:
                gasto=Gastos.query.get(record.id_gasto)
                gasto.importe_pagado=(
                    db.session.query(func.sum(GastosYComprasEnPagos.importe))
                    .select_from(GastosYComprasEnPagos)
                    .join(PagosAdministrativos, isouter=True)
                    .filter(
                        GastosYComprasEnPagos.id_gasto == gasto.id,
                        PagosAdministrativos.estatus != 'Cancelado',
                    )
                    .scalar() or 0
                )
                if gasto.importe_pagado==gasto.importe:
                    gasto.estatus='Pagado'
                else:
                    gasto.estatus='Pagado parcial'
            else:
                compra=Compras.query.get(record.id_compra)
                compra.importe_pagado=(
                    db.session.query(func.sum(GastosYComprasEnPagos.importe))
                    .select_from(GastosYComprasEnPagos)
                    .join(PagosAdministrativos, isouter=True)
                    .filter(
                        GastosYComprasEnPagos.id_compra == compra.id,
                        PagosAdministrativos.estatus != 'Cancelado',
                    )
                    .scalar() or 0
                )
                if compra.importe_pagado==compra.importe_total:
                    compra.estatus_de_pago='Pagada'
                else:
                    compra.estatus_de_pago='Pagada parcial'
        cuadrar_balance(pago.id_cuenta_de_banco)
        db.session.commit()
        flash('El pago se ha marcado como Pagado.','success')
    return redirect(url_for('dynamic.table_view', table_name='pagos_administrativos'))


@pagos_administrativos_bp.route("/cancelar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def cancelar(id):
    pago=PagosAdministrativos.query.get(id)
    if pago.estatus in ('En revisión','Aprobado'):
        pago.estatus="Cancelado"
        compras_gastos=GastosYComprasEnPagos.query.filter_by(id_pago=pago.id)
        for record in compras_gastos:
            if record.id_gasto:
                gasto=Gastos.query.get(record.id_gasto)
                gasto.importe_pagado=(
                    db.session.query(func.sum(GastosYComprasEnPagos.importe))
                    .select_from(GastosYComprasEnPagos)
                    .join(PagosAdministrativos, isouter=True)
                    .filter(
                        GastosYComprasEnPagos.id_gasto == gasto.id,
                        PagosAdministrativos.estatus != 'Cancelado',
                        PagosAdministrativos.id!=pago.id
                    )
                    .scalar() or 0
                )
                if gasto.importe_pagado==0:
                    gasto.estatus='Aprobado'
                else:
                    gasto.estatus='Pagado parcial'
            else:
                compra=Compras.query.get(record.id_compra)

                compra.importe_pagado=(
                    db.session.query(func.sum(GastosYComprasEnPagos.importe))
                    .select_from(GastosYComprasEnPagos)
                    .join(PagosAdministrativos, isouter=True)
                    .filter(
                        GastosYComprasEnPagos.id_compra == compra.id,
                        PagosAdministrativos.estatus != 'Cancelado',
                        PagosAdministrativos.id!=pago.id
                    )
                    .scalar() or 0
                )
                if compra.importe_pagado==0:
                    compra.estatus_de_pago='Sin pagar'
                else:
                    compra.estatus_de_pago='Pagada parcial'
        db.session.commit()
        flash('El pago ha sido Cancelado.','success')
    return redirect(url_for('dynamic.table_view', table_name='pagos_administrativos'))
