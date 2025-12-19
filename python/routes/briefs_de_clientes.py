
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


briefs_de_clientes_bp = Blueprint("briefs_de_clientes", __name__,url_prefix="/briefs_de_clientes")

@briefs_de_clientes_bp.route("/contestar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def contestar(id):
    try:
        record=BriefsDeClientes.query.get(id)
        if record.estatus=='En proceso':
            record.estatus="Contestado"
            current_time = datetime.today() - timedelta(hours=6)
            record.fecha_cierre=current_time.strftime("%Y-%m-%d")
            db.session.commit()
            flash('El Brief ha sido Contestado.','success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al contestar el Brief: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='briefs_de_clientes'))

@briefs_de_clientes_bp.route("/confirmar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def confirmar(id):
    return redirect(url_for('dynamic.table_view', table_name='briefs_de_clientes'))
