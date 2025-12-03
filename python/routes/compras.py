
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

compras_bp = Blueprint("compras", __name__,url_prefix="/compras")

@compras_bp.route("/aprobar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def aprobar(id):
    try:
        record=Compras.query.get(id)
        if record.estatus=='En revisión' and record.id_proveedor:
            record.estatus="Aprobada"
            actualizar_compra(record)
            db.session.commit()
            flash('La compra ha sido Aprobada.','success')
        else:
            flash('Favor de registrar el proveedor y fecha de entrega estimada.')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al aprobar la compra: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='compras'))

@compras_bp.route("/cancelar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def cancelar(id):
    try:
        record=Compras.query.get(id)
        if record.estatus in ('En revisión','Aprobada') and record.estatus_pago=='Sin pagar':
            record.estatus="Cancelada"
            productos=ProductosEnCompras.query.filter_by(id_compra=id)
            for prod in productos:
                prod.estatus="Cancelado"
            record.subtotal=0
            record.descuentos=0
            record.importe_total=0
            db.session.commit()
            flash('La compra ha sido Cancelada.','success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al cancelar la compra: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='compras'))
