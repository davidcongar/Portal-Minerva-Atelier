
from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for,session

from python.models import db
from python.models.modelos import *
from python.services.system.authentication import *
from sqlalchemy.orm import joinedload
from sqlalchemy import String, Text, or_,func,desc
from datetime import date,timedelta
from python.services.system.helper_functions import *
from python.services.general_functions import *

transferencias_de_dinero_bp = Blueprint("transferencias_de_dinero", __name__,url_prefix="/transferencias_de_dinero")

@transferencias_de_dinero_bp.route("/aprobar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def aprobar(id):
    try:
        record=TransferenciasDeDinero.query.get(id)
        if record.estatus=='En revisión':
            record.estatus="Aprobada"
            db.session.commit()
            flash('La transferencia de dinero ha sido Aprobada.','success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al aprobar la transferencia de dinero: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='transferencias_de_dinero'))

@transferencias_de_dinero_bp.route("/cancelar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def cancelar(id):
    try:
        record=TransferenciasDeDinero.query.get(id)
        if record.estatus in ('En revisión','Aprobada'):
            record.estatus="Cancelada"
            db.session.commit()
            flash('La transferencia de dinero ha sido Cancelada.','success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al cancelar la transferencia de dinero: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='transferencias_de_dinero'))

@transferencias_de_dinero_bp.route("/realizar/<id>", methods=["GET"])
@login_required
@roles_required()
def realizar(id):
    try:
        record=TransferenciasDeDinero.query.get(id)
        if record.estatus=='Aprobada':
            # revisar balance
            cuenta=CuentasDeBanco.query.get(record.id_cuenta_de_banco_salida)
            if record.importe>cuenta.balance:
                flash(f'El balance de la cuenta, {money_format(cuenta.balance)}, es menor al importe de transferencia. Favor de revisar.','info')
                return redirect(url_for('dynamic.table_view', table_name='transferencias_de_dinero'))
            record.estatus="Realizada"
            # funcion para cuadrar balance de la cuenta
            cuadrar_balance(record.id_cuenta_de_banco_salida)
            cuadrar_balance(record.id_cuenta_de_banco_entrada)
            db.session.commit()
            flash('La transferencia de dinero ha sido Realizada.','success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al realizar la transferencia de dinero: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='transferencias_de_dinero'))
