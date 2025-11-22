
from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for,session

from python.models import db
from python.models.modelos import *
from python.services.system.authentication import *
from sqlalchemy.orm import joinedload
from sqlalchemy import String, Text, or_,func,desc
from datetime import date,timedelta
from python.services.system.helper_functions import *
from python.services.system.extensions import csrf

interacciones_bp = Blueprint("interacciones", __name__,url_prefix="/interacciones")

@interacciones_bp.route("/finalizar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def finalizar(id):
    try:
        record=Interacciones.query.get(id)
        if record.estatus=='Pendiente':
            if record.duracion_minutos not in (None,0):
                record.estatus="Finalizada"
                db.session.commit()
                flash('El estatus de la interacción se ha modificado a Finalizada.','success')
            else:
                flash('Favor de registrar la duración de la interacción.','info')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al modificar la interacción: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='interacciones'))

@interacciones_bp.route("/cancelar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def cancelar(id):
    try:
        record=Interacciones.query.get(id)
        if record.estatus in ('Pendiente'):
            record.estatus="Cancelar"
            db.session.commit()
            flash('El estatus de la interacción se ha modificado a Cancelado.','success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al modificar la interacción: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='interacciones'))

@interacciones_bp.route("/api/cliente/<id>", methods=["GET","POST"])
@login_required
@csrf.exempt
def api_cliente(id):
    record=Interacciones.query.get(id)       
    return jsonify({'id_cliente':record.id_cliente})