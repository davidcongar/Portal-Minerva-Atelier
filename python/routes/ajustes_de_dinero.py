
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


ajustes_de_dinero_bp = Blueprint("ajustes_de_dinero", __name__,url_prefix="/ajustes_de_dinero")

@ajustes_de_dinero_bp.route("/realizar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
@return_url_redirect
def realizar(id):
    try:
        record=AjustesDeDinero.query.get(id)
        if record.estatus=='En revisión':
            # revisar balance
            if record.tipo_de_ajuste=='Salida':
                cuenta=CuentasDeBanco.query.get(record.id_cuenta_de_banco)
                if record.importe>cuenta.balance:
                    flash(f'El balance de la cuenta, {money_format(cuenta.balance)}, es menor al importe de transferencia. Favor de revisar.','info')
                    return redirect(url_for('dynamic.table_view', table_name='ajustes_de_dinero'))
            record.estatus="Realizado"
            cuadrar_balance(record.id_cuenta_de_banco)
            db.session.commit()
            flash('El ajuste de dinero ha sido Realizado.','success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al realizar el ajuste de dinero: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='ajustes_de_dinero'))

@ajustes_de_dinero_bp.route("/cancelar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
@return_url_redirect
def cancelar(id):
    try:
        record=AjustesDeDinero.query.get(id)
        if record.estatus in ('En revisión'):
            record.estatus="Cancelado"
            db.session.commit()
            flash('El ajuste de dinero ha sido Cancelado.','success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al cancelar el ajuste de dinero: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='ajustes_de_dinero'))