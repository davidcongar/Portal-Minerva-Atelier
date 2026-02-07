
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
@return_url_redirect
def contestar(id):
    try:
        record=BriefsDeClientes.query.get(id)
        if record.estatus=='En proceso':
            record.estatus="Contestado"
            current_time = datetime.today()-timedelta(hours=6)
            record.fecha_cierre=current_time.strftime("%Y-%m-%d")
            if record.brief.nombre=='¿Hacemos match?':
                # logica de perfect match
                cliente=Clientes.query.get(record.id_cliente)
                grade = 0
                score_map = {1: 3,2: 3,3: 2,4: 2,5: 3,6: 2,}
                respuestas = RespuestasBriefsDeClientes.query.filter_by(id_brief_de_cliente=record.id)
                for respuesta in respuestas:
                    pregunta = PreguntasDeBriefs.query.get(respuesta.id_pregunta_de_brief)
                    respuesta_brief=RespuestasDePreguntasDeBriefs.query.filter_by(id_pregunta_de_brief=respuesta.id_pregunta_de_brief,respuesta=respuesta.respuesta).first()
                    grade += score_map.get(pregunta.orden, 0) if respuesta_brief.opcion_de_respuesta == 'A' else 0
                cliente.estatus='Perfect match' if grade>=8 else 'Swipe'
            db.session.commit()
            flash('El Brief ha sido Contestado.','success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al contestar el Brief: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='briefs_de_clientes'))

@briefs_de_clientes_bp.route("/confirmar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
@return_url_redirect
def confirmar(id):
    return redirect(url_for('dynamic.table_view', table_name='briefs_de_clientes'))
