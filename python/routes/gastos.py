
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


gastos_bp = Blueprint("gastos", __name__,url_prefix="/gastos")

@gastos_bp.route("/aprobar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def aprobar(id):
    record=Gastos.query.get(id)
    if record.estatus=='En revisión':
        record.estatus="Aprobado"        
        if record.id_cuenta_de_banco:
            # generar pago
            record.estatus="Pagado"
            new_pago=PagosAdministrativos(
                id_visualizacion=get_id_visualizacion('pagos_administrativos'),
                id_proveedor=record.id_proveedor,
                id_cuenta_de_banco=record.id_cuenta_de_banco,
                fecha_pago=record.fecha_de_gasto,
                importe=record.importe,
                estatus='Pagado'
            )
            db.session.add(new_pago)
            db.session.flush()
            new_record=GastosYComprasEnPagos(
                id_pago=new_pago.id,
                id_gasto=record.id,
                importe=record.importe
            )
            db.session.add(new_record)
            record.importe_pagado=record.importe
            cuadrar_balance(record.id_cuenta_de_banco)
            flash('El gasto ha sido Pagado.','success')
        else:
            flash('El gasto ha sido Aprobado.','success')
        db.session.commit()
    return redirect(url_for('dynamic.table_view', table_name='gastos'))

@gastos_bp.route("/cancelar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def cancelar(id):
    record=Gastos.query.get(id)
    if record.estatus=='En revisión':
        record.estatus="Cancelado"
        db.session.commit()
        flash('El gasto ha sido Cancelado.','success')
    return redirect(url_for('dynamic.table_view', table_name='gastos'))
