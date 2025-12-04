
from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for,session

from python.models import db
from python.models.modelos import *
from python.services.system.authentication import *
from sqlalchemy.orm import joinedload
from sqlalchemy import String, Text, or_,func,desc
from datetime import date,timedelta
from python.services.system.helper_functions import *

agenda_bp = Blueprint("agenda", __name__,url_prefix="/agenda")

@agenda_bp.route("/finalizar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def finalizar(id):
    try:
        record=Agenda.query.get(id)
        if record.estatus in ('Pendiente'):
            record.estatus='Finalizada'
            db.session.commit()
            flash(f"La Agenda fue Finalizada.", "success")
            return redirect(url_for('dynamic.table_view', table_name='agenda'))
    except Exception as e:
        db.session.rollback()
        flash(f"Error al finalizar la Agenda: {str(e)}", "danger")
        return redirect(url_for('dynamic.table_view', table_name='agenda'))

@agenda_bp.route("/cancelar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def cancelar(id):
    try:
        record=Agenda.query.get(id)
        if record.estatus in ('Pendiente','Confirmada'):
            record.estatus='Cancelada'
            db.session.commit()
            flash(f"La Agenda fue Cancelada.", "success")
            return redirect(url_for('dynamic.table_view', table_name='agenda'))
    except Exception as e:
        db.session.rollback()
        flash(f"Error al cerrar la Agenda: {str(e)}", "danger")
        return redirect(url_for('dynamic.table_view', table_name='agenda'))


@agenda_bp.route("/validate_availability/<fecha>/<hora_inicio>", methods=["GET","POST"])
@login_required
def validate_before_submit(id_empleado,fecha,hora_inicio):
    cita = Agenda.query.filter(
        Agenda.id_empleado == id_empleado,
        Agenda.fecha == fecha,
        Agenda.hora_inicio <= hora_inicio,
        Agenda.hora_fin >= hora_inicio,
        Agenda.estatus.in_(('Pendiente'))
    ).first()
    if cita:
        status=0
    else:
        status=1
    return jsonify({"status": status})
