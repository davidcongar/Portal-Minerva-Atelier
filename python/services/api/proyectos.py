from python.services.api import api_bp
from python.services.api.auth import *

@api_bp.route('/get_proyectos_cliente', methods=['GET'])
def get_proyectos_cliente():
    auth_data, ok = api_basic_auth()
    if not ok:
        return {"status": "nok", "message": auth_data["message"]}, 401

    json_data = request.json
    id_cliente = json_data['id_cliente']

    data = [
        {c.key: getattr(item, c.key) for c in inspect(item).mapper.column_attrs}
        for item in Proyectos.query.filter_by(id_cliente=id_cliente).all()

    ]
    return jsonify(data)

@api_bp.route('/get_briefs_proyecto', methods=['GET'])
def get_briefs_proyecto():
    auth_data, ok = api_basic_auth()
    if not ok:
        return {"status": "nok", "message": auth_data["message"]}, 401

    json_data = request.json
    id_proyecto = json_data['id_proyecto']

    # Get all active briefs belonging to this project
    briefs_proyecto= BriefsDeClientes.query.filter_by(
        id_proyecto=id_proyecto
    ).all()
    print(briefs_proyecto)

    data = []

    for brief_rel in briefs_proyecto:
        brief = brief_rel.brief  # The actual Briefs object

        # Serialize the BriefsDeClientes record (your original brief object)
        brief_dict = {
            c.key: getattr(brief_rel, c.key)
            for c in inspect(brief_rel).mapper.column_attrs
        }

        # 1️⃣ Add BRIEF info (from Briefs)
        brief_dict["brief_info"] = {
            c.key: getattr(brief, c.key)
            for c in inspect(brief).mapper.column_attrs
        }

        # If brief has a linked servicio, add its info
        if brief.servicio:
            brief_dict["servicio"] = {
                c.key: getattr(brief.servicio, c.key)
                for c in inspect(brief.servicio).mapper.column_attrs
            }
        else:
            brief_dict["servicio"] = None

        # 2️⃣ Add PREGUNTAS + RESPUESTAS
        preguntas_data = []
        for pregunta in brief.preguntas_de_briefs:
            if pregunta.estatus != "Activo":
                continue

            # Base data of pregunta
            pregunta_dict = {
                c.key: getattr(pregunta, c.key)
                for c in inspect(pregunta).mapper.column_attrs
            }

            # Add responses of pregunta
            respuestas_data = [
                {
                    c.key: getattr(resp, c.key)
                    for c in inspect(resp).mapper.column_attrs
                }
                for resp in pregunta.respuestas_de_preguntas_de_briefs
                if resp.estatus == "Activo"
            ]

            pregunta_dict["respuestas"] = respuestas_data
            preguntas_data.append(pregunta_dict)

        brief_dict["preguntas"] = preguntas_data

        data.append(brief_dict)

    return jsonify(data)

@api_bp.route('/answer_brief', methods=['POST'])
def answer_brief():
    try:
        auth_data, ok = api_basic_auth()
        if not ok:
            return {"status": "nok", "message": auth_data["message"]}, 401        
        json_data = request.json
        id_brief_de_cliente = json_data['id_brief_de_cliente']
        respuestas = json_data['respuestas']
        brief_de_cliente=BriefsDeClientes.query.get(id_brief_de_cliente)
        preguntas_brief_de_cliente=RespuestasBriefsDeClientes.query.filter_by(id_brief_de_cliente=id_brief_de_cliente).all()

        for pregunta in preguntas_brief_de_cliente:
            respuesta=''
            respuesta_opcion = respuestas.get(str(pregunta.id))
            if respuesta_opcion:
                respuesta_model = RespuestasDePreguntasDeBriefs.query.filter_by(id_pregunta_de_brief=pregunta.id,opcion_de_respuesta=respuesta_opcion).first()
                if respuesta_model:
                    respuesta=respuesta_model.respuesta
            pregunta.respuesta=respuesta
        brief_de_cliente.estatus='Contestado'
        db.session.commit()
        return {"status": "ok", 'message': 'Brief contestado exitosamente.'}
    except Exception as e:
        db.session.rollback()
        return {"status": "nok", "message": str(e)}, 400

@api_bp.route('/get_actividades_proyecto', methods=['GET'])
def get_actividades_proyecto():
    auth_data, ok = api_basic_auth()
    if not ok:
        return {"status": "nok", "message": auth_data["message"]}, 401
    json_data = request.json
    id_proyecto = json_data['id_proyecto']
    actividades = Actividades.query.filter_by(id_proyecto=id_proyecto).all()
    data = []
    for act in actividades:

        # Base actividad data
        act_dict = {
            c.key: getattr(act, c.key)
            for c in inspect(act).mapper.column_attrs
        }

        # 1️⃣ Join & serialize ActividadesBase
        if act.actividad_base:
            act_dict["actividad_base"] = {
                c.key: getattr(act.actividad_base, c.key)
                for c in inspect(act.actividad_base).mapper.column_attrs
            }

            # Optionally include the servicio info from ActividadesBase → Servicios
            if act.actividad_base.servicio:
                act_dict["servicio"] = {
                    c.key: getattr(act.actividad_base.servicio, c.key)
                    for c in inspect(act.actividad_base.servicio).mapper.column_attrs
                }
        else:
            act_dict["actividad_base"] = None
            act_dict["servicio"] = None

        data.append(act_dict)

    return jsonify(data)

@api_bp.route("/activity_change", methods=["POST"])
def activity_change():
    try:
        auth_data, ok = api_basic_auth()
        if not ok:
            return {"status": "nok", "message": auth_data["message"]}, 401   
        json_data = request.json
        id_actividad=json_data['id_actividad']
        comentario=json_data['comentario']
        record=Actividades.query.get(id_actividad)
        if record.estatus in ('Realizada'):
            record.estatus="Con cambios"
            new_record=ComentariosDeClientesDeActividades(
                id_visualizacion=get_id_visualizacion('comentarios_de_clientes_de_actividades'),
                id_actividad=record.id,
                comentario_cliente=comentario,
                id_usuario=Usuarios.query.filter_by(nombre='Sistema').first().id
            )
            proyecto=Proyectos.query.get(record.id_proyecto)
            integrante=Integrantes.query.get(record.id_integrante)
            print("HOLA")   
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
    except Exception as e:
        db.session.rollback()
        return {"status": "nok", "message": e}
    
@api_bp.route('/get_comentarios_actividad', methods=['GET'])
def get_comentarios_actividad():
    auth_data, ok = api_basic_auth()
    if not ok:
        return {"status": "nok", "message": auth_data["message"]}, 401
    json_data = request.json
    id_actividad = json_data['id_actividad']
    data = [
        {c.key: getattr(item, c.key) for c in inspect(item).mapper.column_attrs}
        for item in ComentariosDeClientesDeActividades.query.filter_by(id_actividad=id_actividad).all()
    ]
    return jsonify(data)

from python.services.system.boto3_s3 import S3Service
s3_service = S3Service()

@api_bp.route('/get_archivos_actividad', methods=['GET'])
def get_archivos_actividad():
    auth_data, ok = api_basic_auth()
    if not ok:
        return {"status": "nok", "message": auth_data["message"]}, 401

    json_data = request.json
    id_actividad = json_data['id_actividad']

    data = []
    archivos = Archivos.query.filter_by(tabla_origen="actividades",id_registro=id_actividad).all()
    archivos_list = []
    for archivo in archivos:
        archivo_dict = {
            c.key: getattr(archivo, c.key)
            for c in inspect(archivo).mapper.column_attrs
        }

        try:
            signed_url = s3_service.generate_presigned_url(
                archivo.ruta_s3,
                "view"
            )
        except Exception as e:
            signed_url = None  # avoid breaking the endpoint

        archivo_dict["presigned_url"] = signed_url
        archivos_list.append(archivo_dict)
    data.append(archivos_list)

    return jsonify(data)


@api_bp.route("/activity_acceptance", methods=["POST"])
def activity_acceptance():
    try:
        auth_data, ok = api_basic_auth()
        if not ok:
            return {"status": "nok", "message": auth_data["message"]}, 401      
        json_data = request.json
        id_actividad=json_data['id_actividad']
        record=Actividades.query.get(id_actividad)
        if record.estatus in ('Realizada'):
            record.aceptacion_de_cliente='Aceptada'
            db.session.commit()    
            return {"status": "ok",'message':'La actividad se acepto exitosamenta.'}
        else:
            return {"status": "nok", "message": 'Actividad no se encuentra Realizada'}
    except Exception as e:
        db.session.rollback()
        return {"status": "nok", "message": e}
    
