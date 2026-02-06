
from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for,session

from python.models import db
from python.models.modelos import *
from python.services.system.authentication import *
from sqlalchemy.orm import joinedload
from sqlalchemy import String, Text, or_,func,desc
from datetime import date,timedelta
from python.services.system.helper_functions import *

precios_de_servicios_bp = Blueprint("precios_de_servicios", __name__,url_prefix="/precios_de_servicios")

@precios_de_servicios_bp.route("/validate/<id_espacio>/<id_servicio>", methods=["GET","POST"])
@login_required
def revision_salida(id_espacio,id_servicio):
    existe=PreciosDeServicios.query.filter_by(id_espacio=id_espacio,id_servicio=id_servicio).first()
    if existe:
        status='warning'
        message=f'Ya esiste un precio del servicio y espacio ingresado. Favor de editar ese registro.'
    else:
        status='success'
        message='ok'
    return jsonify({"status": status, "message": message})

