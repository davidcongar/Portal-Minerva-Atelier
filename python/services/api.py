from flask import Blueprint, render_template, jsonify, request, Response, session
from sqlalchemy import or_, and_, cast, String, func, text
from python.models.modelos import *
from python.services.system.authentication import *

import io
from PIL import Image, ImageDraw, ImageFont
from python.services.dynamic_functions.forms import *
from python.services.dynamic_functions.tables import *
import traceback
from python.services.stripe import checkout_session

api_bp = Blueprint("api", __name__, url_prefix="/api")

def api_basic_auth():
    auth = request.authorization
    if not auth:
        return {"message": "Missing Basic Auth credentials"}, False
    user = Usuarios.query.filter(Usuarios.correo_electronico == auth.username).first()
    if user and str(auth.password) == str(user.contrasena_api):
        return {"message": "Credenciales validas", "user": user}, True
    return {"message": "Credenciales no validas"}, False

# adquisicion de cliente
@api_bp.route('/get_brief_hacemos_match', methods=['GET'])
def get_brief_hacemos_match():
    auth_data, ok = api_basic_auth()
    if not ok:
        return {"status": "nok", "message": auth_data["message"]}, 401

    # Get all active briefs
    briefs = Briefs.query.filter_by(estatus='Activo',nombre='¿Hacemos match?').all()

    data = []
    for brief in briefs:
        brief_dict = {
            c.key: getattr(brief, c.key)
            for c in inspect(brief).mapper.column_attrs
        }
        preguntas = []
        for pregunta in brief.preguntas_de_briefs:
            if pregunta.estatus != "Activo":
                continue

            pregunta_dict = {
                c.key: getattr(pregunta, c.key)
                for c in inspect(pregunta).mapper.column_attrs
            }
            respuestas = [
                {
                    c.key: getattr(resp, c.key)
                    for c in inspect(resp).mapper.column_attrs
                }
                for resp in pregunta.respuestas_de_preguntas_de_briefs
                if resp.estatus == "Activo"
            ]
            pregunta_dict["respuestas"] = respuestas
            preguntas.append(pregunta_dict)
        brief_dict["preguntas"] = preguntas
        data.append(brief_dict)
    return jsonify(data)

# crear cliente
@api_bp.route('/new_client', methods=['POST'])
def new_client():
    try:
        auth_data, ok = api_basic_auth()
        if not ok:
            return {"status": "nok", "message": auth_data["message"]}, 401        
        json_data = request.json
        nombre_completo = json_data['nombre_completo']
        correo_electronico = json_data['correo_electronico']
        respuestas = json_data['respuestas']
        existe_cliente=Clientes.query.filter_by(correo_electronico=correo_electronico).first()
        if existe_cliente:
            return {"status": "nok", "message": "Cliente ya existe."}, 401        

        # Create client
        new = Clientes(
            id_visualizacion=get_id_visualizacion('clientes'),
            nombre_completo=nombre_completo,
            correo_electronico=correo_electronico.strip().lower()
        )
        db.session.add(new)
        db.session.flush()   # new.id now exists

        # Get brief
        brief = Briefs.query.filter_by(estatus='Activo',nombre='¿Hacemos match?').first()
        # Create relation brief ↔ cliente
        new_record = BriefsDeClientes(
            id_visualizacion=get_id_visualizacion('briefs_de_clientes'),
            id_cliente=new.id,
            id_brief=brief.id,
            fecha_cierre=date.today(),
            estatus='Contestado'
        )
        db.session.add(new_record)
        db.session.flush()

        # Questions in this brief
        preguntas = PreguntasDeBriefs.query.filter_by(id_brief=brief.id,estatus='Activo').all()

        for pregunta in preguntas:
            respuesta=''
            respuesta_opcion = respuestas.get(str(pregunta.id))
            if respuesta_opcion:
                respuesta_model = RespuestasDePreguntasDeBriefs.query.filter_by(id_pregunta_de_brief=pregunta.id,opcion_de_respuesta=respuesta_opcion).first()
                if respuesta_model:
                    respuesta=respuesta_model.respuesta
            # Save respuesta del cliente
            new_pregunta = RespuestasBriefsDeClientes(
                id_brief_de_cliente=new_record.id,
                id_pregunta_de_brief=pregunta.id,
                respuesta=respuesta
            )
            db.session.add(new_pregunta)
        db.session.flush()
        grade = 0
        score_map = {1: 3,2: 3,3: 2,4: 2,5: 3,6: 2,}
        respuestas = RespuestasBriefsDeClientes.query.filter_by(id_brief_de_cliente=new_record.id)
        for respuesta in respuestas:
            pregunta = PreguntasDeBriefs.query.get(respuesta.id_pregunta_de_brief)
            respuesta_brief=RespuestasDePreguntasDeBriefs.query.filter_by(id_pregunta_de_brief=respuesta.id_pregunta_de_brief,respuesta=respuesta.respuesta).first()
            grade += score_map.get(pregunta.orden, 0) if respuesta_brief.opcion_de_respuesta == 'A' else 0
        new.estatus='Perfect match' if grade>=8 else 'Swipe'            
        db.session.commit()
        return {"status": "ok", 'message': 'Cliente creado exitosamente.','id_cliente':new.id}
    except Exception as e:
        db.session.rollback()
        return {"status": "nok", "message": str(e)}, 400

@api_bp.route('/new_appointment',methods=['POST'])
def new_appointment():
    try:
        auth_data, ok = api_basic_auth()
        if not ok:
            return {"status": "nok", "message": auth_data["message"]}, 401
        json_data = request.json
        new_record=Agenda(
            id_visualizacion=get_id_visualizacion('agenda'),
            id_cliente=json_data['id_cliente'],
            fecha=json_data['fecha'],
            hora_inicio=json_data['hora']
        )
        db.session.add(new_record)
        db.session.commit()
        return {"status": "ok", 'message': 'Cita creada exitosamente.'}
    except Exception as e:
        db.session.rollback()
        return {"status": "nok", "message": str(e)}, 400

# ventas
@api_bp.route('/get_servicios', methods=['GET'])
def get_servicios():
    auth_data, ok = api_basic_auth()
    if not ok:
        return {"status": "nok", "message": auth_data["message"]}, 401

    servicios = PreciosDeServicios.query.filter_by(estatus='Activo').all()
    data = []
    for item in servicios:
        item_dict = {
            c.key: getattr(item, c.key)
            for c in inspect(item).mapper.column_attrs
        }

        # Add the related names
        item_dict["nombre_servicio"] = item.servicio.nombre if item.servicio else None
        item_dict["descripcion_servicio"] = item.servicio.descripcion if item.servicio else None
        item_dict["nombre_espacio"] = item.espacio.nombre if item.espacio else None
        item_dict["descripcion_espacio"] = item.espacio.descripcion if item.espacio else None

        data.append(item_dict)

    return jsonify(data)

@api_bp.route('/new_venta', methods=['POST'])
def new_venta():
    try:
        auth_data, ok = api_basic_auth()
        if not ok:
            return {"status": "nok", "message": auth_data["message"]}, 401
        json_data = request.json
        new_record=Ventas(
            id_visualizacion=get_id_visualizacion('ventas'),
            id_cliente=json_data['id_cliente'],
            codigo_de_descuento=json_data['codigo_de_descuento'],
            fecha_de_venta=date.today()
        )
        db.session.add(new_record)
        servicios=json_data['servicios']
        for servicio in servicios:
            precio=PreciosDeServicios.query.get(servicio)
            importe=precio.precio_unitario
            new_servicio=ServiciosEnVentas(
                id_venta=new_record.id,
                id_servicio=precio.id_servicio,
                id_espacio=precio.id_espacio,
                id_stripe_precio=precio.id_stripe_precio,
                precio_unitario=precio.precio_unitario,
                cantidad=1,
                subtotal=importe,
                importe=importe        
            )
            db.session.add(new_servicio)
        db.session.flush()
        actualizar_venta(new_record)
        db.session.flush()
        stripe_url=checkout_session(new_record.id)
        db.session.commit()
        return {"status": "ok", 'stripe_url': stripe_url}
    except Exception as e:
        db.session.rollback()
        return {"status": "nok", "message": str(e)}, 400



@api_bp.route('/get_clientes',methods=['GET'])
def get_clientes():
    auth_data, ok = api_basic_auth()
    if not ok:
        return {"status": "nok", "message": auth_data["message"]}, 401
    data = [
        {c.key: getattr(item, c.key) for c in inspect(item).mapper.column_attrs}
        for item in Clientes.query.all()
    ]
    return jsonify(data)

@api_bp.route('/get_briefs',methods=['GET'])
def get_briefs():
    auth_data, ok = api_basic_auth()
    if not ok:
        return {"status": "nok", "message": auth_data["message"]}, 401
    data = [
        {c.key: getattr(item, c.key) for c in inspect(item).mapper.column_attrs}
        for item in Briefs.query.all()
    ]
    return jsonify(data)

@api_bp.route('/get_preguntas_briefs',methods=['GET'])
def get_preguntas_briefs():
    auth_data, ok = api_basic_auth()
    if not ok:
        return {"status": "nok", "message": auth_data["message"]}, 401
    json_data = request.get_json(silent=True) or {}    
    id_brief=json_data.get("id_brief")
    if not id_brief:
        return {"status": "nok", "message": "Falta id_brief"}, 400    
    data = []

    preguntas = PreguntasDeBriefs.query.filter_by(
        estatus='Activo',
        id_brief=id_brief
    ).order_by(PreguntasDeBriefs.orden).all()

    for pregunta in preguntas:
        pregunta_dict = {
            c.key: getattr(pregunta, c.key)
            for c in inspect(pregunta).mapper.column_attrs
        }
        # Add respuestas filtered by estatus = "Activo"
        respuestas = [
            {
                c.key: getattr(resp, c.key)
                for c in inspect(resp).mapper.column_attrs
            }
            for resp in pregunta.respuestas_de_preguntas_de_briefs
            if resp.estatus == "Activo"
        ]
        pregunta_dict["respuestas"] = respuestas
        data.append(pregunta_dict)

    return jsonify(data)


# crear cliente
@api_bp.route('/answer_briefs',methods=['GET', 'POST'])
def answer_briefs():
    try:
        json_data = request.json
        auth=api_basic_auth()
        if auth['message']=='Credenciales validas':
            id_cliente=json_data['id_cliente']
            id_brief=json_data['id_brief']
            respuestas=json_data['respuestas']
            cliente=Clientes.query.get(id_cliente)
            brief_cliente=BriefsDeClientes.query.filter_by(id_brief=id_brief,id_cliente=cliente.id).first()
            preguntas=RespuestasBriefsDeClientes.query.filter_by(id_brief_de_cliente=brief_cliente.id).all()
            for pregunta in preguntas:
                pregunta.respuesta=respuestas[pregunta.id_pregunta_de_brief]
            db.session.commit()
            return {"status": "ok",'message':'Brief contestado exitosamente.'}
        else:
            return {"status": "nok",'message':'Credenciales no válidas'}
    except Exception as e:
        db.session.rollback()
        return {"status": "nok", "message": e}

@api_bp.route("/cambios_actividades", methods=["POST"])
@login_required
@roles_required()
def cambios():
    try:
        json_data = request.json
        auth=api_basic_auth()
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