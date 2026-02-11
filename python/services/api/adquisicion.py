from python.services.api import api_bp
from python.services.api.auth import *

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
            correo_electronico=correo_electronico.strip().lower(),
            id_usuario=Usuarios.query.filter_by(nombre='Sistema').first().id            
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
            estatus='Contestado',
            id_usuario=Usuarios.query.filter_by(nombre='Sistema').first().id
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
                respuesta=respuesta,
                id_usuario=Usuarios.query.filter_by(nombre='Sistema').first().id
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
        hora_inicio = datetime.strptime(json_data['hora'], "%H:%M")   # example format
        hora_fin = hora_inicio + timedelta(minutes=45)        
        new_record=Agenda(
            id_visualizacion=get_id_visualizacion('agenda'),
            id_cliente=json_data['id_cliente'],
            fecha=json_data['fecha'],
            hora_inicio=json_data['hora'],
            hora_fin=hora_fin,
            id_usuario=Usuarios.query.filter_by(nombre='Sistema').first().id
        )
        db.session.add(new_record)
        db.session.commit()
        return {"status": "ok", 'message': 'Cita creada exitosamente.'}
    except Exception as e:
        db.session.rollback()
        return {"status": "nok", "message": str(e)}, 400