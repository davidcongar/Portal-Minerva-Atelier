# python/routes/home.py

from flask import Blueprint, render_template, jsonify, request, Response, session
from sqlalchemy import or_, and_, cast, String, func, text
from python.models.modelos import *
from python.services.system.authentication import *

import io
from PIL import Image, ImageDraw, ImageFont
from python.services.dynamic_functions.forms import *
from python.services.dynamic_functions.tables import *
import traceback

api_bp = Blueprint("api", __name__, url_prefix="/api")
def api_login(json_data):
    id_usuario = json_data['id_usuario']
    contrasena = json_data['contrasena']
    user = Usuarios.query.filter(Usuarios.id==id_usuario).first()
    if user!=None:
        if contrasena==user.contrasena_api:
            data={'message':'Credenciales validas'}
        else:
            data={'message':'Credenciales no validas'}
    else:
        data={'message':'Credenciales no validas'}
    return data  # Redirect back to the form

@api_bp.route('/<table_name>',methods=['GET', 'POST'])
def dynamic_data(table_name):
    json_data = request.json
    auth=api_login(json_data)
    if auth['message']=='Credenciales validas':
        model = get_model_by_name(table_name)
        if not model:
            data={'message':'La tabla no existe.'}
            return data
        data = [item.to_dict() for item in model.query.all()]
        return jsonify(data)
    else:
        data={'message':'Credenciales no validas'}
        return data

@api_bp.route("/cambios_actividades", methods=["POST"])
@login_required
@roles_required()
def cambios():
    try:
        json_data = request.json
        auth=api_login(json_data)
        if auth['message']=='Credenciales validas':
            id=json_data['id']
            comentario=json_data['comentario']
            record=Actividades.query.get(id)
            if record.estatus in ('Realizada'):
                record.estatus="Con cambios"
                new_record=ComentariosDeClientesDeActividades(
                    id_actividad=record.id,
                    comentario_cliente=comentario,
                    id_usuario=Usuarios.query.filter_by(nombre='Sistema').first()
                )
                proyecto=Proyectos.query.get(record.id_proyecto)
                integrante=Integrantes.query.get(record.id_integrante)
                # Enviar correo al cliente para aceptacion
                send_html_email(
                    subject="Portal Minerva Atelier - Comentario realiado por cliente",
                    recipient_email=integrante.correo_electronico,
                    template="partials/system/email_template.html",
                    body_content=f"Se acaba de dar de alta un comentario por el cliente {proyecto.cliente.nombre_completo}. A continuación se muestran los detalles.",
                    details_list=[
                        f"ID Proyecto: {proyecto.id_visualizacion}",
                        f"Espacio: {proyecto.espacio.nombre}",
                        f"Actividad: {record.actividad_base.nombre}",
                        f"Comentario: {comentario}",

                    ]
                )
                db.session.add(new_record)
                db.session.commit()    
                return {"status": "ok",'message':'Comentario creado exitosamente.'}
        else:
            return {"status": "nok", "message": 'Credenciales no válidas'}
    except Exception as e:
        db.session.rollback()
        return {"status": "nok", "message": e}
