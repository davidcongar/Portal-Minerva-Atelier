from python.services.api import api_bp
from python.services.api.auth import *

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
                importe=importe,
                id_usuario=Usuarios.query.filter_by(nombre='Sistema').first().id        
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