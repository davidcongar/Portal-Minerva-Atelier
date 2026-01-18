
from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for,session

from python.models import db
from python.models.modelos import *
from python.services.system.authentication import *
from sqlalchemy.orm import joinedload
from sqlalchemy import String, Text, or_,func,desc
from datetime import date,timedelta
from python.services.system.helper_functions import *

actividades_bp = Blueprint("actividades", __name__,url_prefix="/actividades")

@actividades_bp.route("/asignar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def asignar(id):
    try:
        record=Actividades.query.get(id)
        if record.estatus in ('Sin iniciar'):
            session['return_url']=request.args.get("return_url", "")
            return redirect(url_for('dynamic.form', table_name='actividades',id=id,accion='Asignar'))
    except Exception as e:
        flash(f"Error al asignar la actividad: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='actividades'))
