
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


pagos_de_nomina_bp = Blueprint("pagos_de_nomina", __name__,url_prefix="/pagos_de_nomina")

@pagos_de_nomina_bp.route("/aprobar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
@return_url_redirect
def aprobar(id):
    pago=PagosDeNomina.query.get(id)
    if pago.estatus=='En revisión':
        if pago.importe_total==0:
            flash('El pago tiene importe 0. Favor de revisar','info')
            return redirect(url_for('dynamic.table_view', table_name='pagos_de_nomina'))
        pago.estatus="Aprobado"
        db.session.commit()
        flash('El pago ha sido Aprobado.','success')
    return redirect(url_for('dynamic.table_view', table_name='pagos_de_nomina'))

@pagos_de_nomina_bp.route("/pagar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
@return_url_redirect
def pagar(id):
    pago=PagosDeNomina.query.get(id)
    if pago.estatus=='Aprobado':
        cuenta=CuentasDeBanco.query.get(pago.id_cuenta_de_banco)
        if pago.importe_total>cuenta.balance:
            flash(f'El balance de la cuenta, {money_format(cuenta.balance)}, es menor al importe del pago. Favor de revisar.','info')
            return redirect(url_for('dynamic.table_view', table_name='pagos_de_nomina'))
        pago.estatus="Pagado"
        cuadrar_balance(pago.id_cuenta_de_banco)
        db.session.commit()
        flash('El pago se ha marcado como Pagado.','success')
    return redirect(url_for('dynamic.table_view', table_name='pagos_de_nomina'))


@pagos_de_nomina_bp.route("/cancelar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
@return_url_redirect
def cancelar(id):
    pago=PagosDeNomina.query.get(id)
    if pago.estatus in ('En revisión','Aprobado'):
        pago.estatus="Cancelado"
        db.session.commit()
        flash('El pago ha sido Cancelado.','success')
    return redirect(url_for('dynamic.table_view', table_name='pagos_de_nomina'))

@pagos_de_nomina_bp.route("/confirm/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def confirm(id):
    return redirect(url_for('dynamic.table_view', table_name='pagos_de_nomina'))