from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for,session

from python.models import db
from python.models.modelos import *
from python.services.system.authentication import *
from sqlalchemy.orm import joinedload
from sqlalchemy import String, Text, or_,func,desc
from datetime import date, timedelta
from python.services.system.helper_functions import *
import math

comentarios_de_clientes_de_actividades_bp = Blueprint("comentarios_de_clientes_de_actividades", __name__,url_prefix="/comentarios_de_clientes_de_actividades")

@comentarios_de_clientes_de_actividades_bp.route("/cerrar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def cerrar(id):
    try:
        record=ComentariosDeClientesDeActividades.query.get(id)
        if record.estatus in ('En proceso'):
            session['return_url']=request.args.get("return_url", "")
            return redirect(url_for('dynamic.form', table_name='comentarios_de_clientes_de_actividades',id=id,accion='Cerrar'))
    except Exception as e:
        flash(f"Error al cerrar el cometnario: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='comentarios_de_clientes_de_actividades'))
