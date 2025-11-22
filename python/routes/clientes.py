
from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for,session

from python.models import db
from python.models.modelos import *
from python.services.system.authentication import *
from sqlalchemy.orm import joinedload
from sqlalchemy import String, Text, or_,func,desc
from datetime import date,timedelta
from python.services.system.helper_functions import *

clientes_bp = Blueprint("clientes", __name__,url_prefix="/clientes")

@clientes_bp.route("/en_proceso/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def en_proceso(id):
    try:
        record=Clientes.query.get(id)
        if record.estatus=='Contacto inicial':
            record.estatus="En proceso"
            db.session.commit()
            flash('El estatus del cliente se ha modificado a En proceso.','success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al modificar el cliente: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='clientes'))

@clientes_bp.route("/ganado/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def ganado(id):
    try:
        record=Clientes.query.get(id)
        if record.estatus=='En proceso':
            record.estatus="Activo"
            db.session.commit()
            flash('El estatus del cliente se ha modificado a Activo.','success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al modificar el cliente: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='clientes'))

@clientes_bp.route("/perdido/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def perdido(id):
    try:
        record=Clientes.query.get(id)
        if record.estatus in ('En proceso','Contacto inicial'):
            record.estatus="Perdido"
            db.session.commit()
            flash('El estatus del cliente se ha modificado a Perdido.','success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al modificar el cliente: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='clientes'))
