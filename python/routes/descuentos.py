
from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for,session

from python.models import db
from python.models.modelos import *
from python.services.system.authentication import *
from sqlalchemy.orm import joinedload
from sqlalchemy import String, Text, or_,func,desc
from datetime import date,timedelta
from python.services.system.helper_functions import *

descuentos_bp = Blueprint("descuentos", __name__,url_prefix="/descuentos")

@descuentos_bp.route("/validate/<id_espacio>/<id_servicio>", methods=["GET","POST"])
@login_required
def validate(id_espacio,id_servicio):
    existe=PreciosDeServicios.query.filter_by(id_espacio=id_espacio,id_servicio=id_servicio).first()
    if existe==None:
        status='warning'
        message=f'No existe un Precio para la combinación seleccionada. Favor de registrar un precio antes de registrar el descuento.'
    else:
        status='success'
        message='ok'
    return jsonify({"status": status, "message": message})

@descuentos_bp.route("/validate_code/<codigo_de_descuento>", methods=["GET","POST"])
@login_required
def validate_code(codigo_de_descuento):
    existe = Descuentos.query.filter(func.upper(Descuentos.codigo_de_descuento) == codigo_de_descuento.upper()).first()    
    if existe:
        status='warning'
        message=f'Ya existe un desscuento con el código registrado.'
    else:
        status='success'
        message='ok'
    return jsonify({"status": status, "message": message})

