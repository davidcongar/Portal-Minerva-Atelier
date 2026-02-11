
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
from config import *
import stripe
from dotenv import load_dotenv
load_dotenv()

#4242424242424242
DOMAIN = os.getenv('DOMAIN')
stripe.api_key = os.getenv('STRIPE_API_KEY')

ventas_bp = Blueprint("ventas", __name__,url_prefix="/ventas")

@ventas_bp.route("/success")
def success():
    try:
        session_id = request.args.get("session_id")
        if not session_id:
            flash("Missing session ID. Payment cannot be verified.", "danger")
            return redirect(url_for('dynamic.table_view', table_name='ventas'))
        session = stripe.checkout.Session.retrieve(session_id)
        id_venta = session.metadata.get("id_venta")
        venta=Ventas.query.get(id_venta)
        venta.id_stripe=session.payment_intent
        venta.estatus='Cobrada'
        db.session.commit()
        send_html_email(
            subject="Minerva Atelier - Confirmación de pago",
            recipient_email=venta.cliente.correo_electronico,
            template="partials/system/email_template.html",
            sender_name="Minerva Atelier",
            body_content = (
                "Se acaba de confirmar tu pago a través de Stripe.<br>"
                "Favor de acceder a su cuenta en el portal de clientes para contestar los cuestionarios que requerimos para avanzar.<br>"
                "Muchas gracias por la confianza."
            ),
            details_list=[
                f"Importe total: {money_format(venta.importe_total)}"
            ]
        )
        # crear proyectos
        items=ServiciosEnVentas.query.filter_by(id_venta=venta.id).all()
        for item in items:
            new_record=Proyectos(
                id_visualizacion=get_id_visualizacion('proyectos'),
                id_cliente=venta.id_cliente,
                id_venta=venta.id,
                id_servicio=item.id_servicio,
                id_espacio = item.id_espacio,
                metros_cuadrados=item.metros_cuadrados,
                fecha_inicio = datetime.today()
            )
            db.session.add(new_record)
            db.session.flush()
            # generar briefs
            briefs = Briefs.query.filter(Briefs.nombre.in_(BRIEFS_GLOW_UP)).all()
            for brief in briefs:
                new_brief=BriefsDeClientes(
                    id_visualizacion=get_id_visualizacion('briefs_de_clientes'),
                    id_cliente=venta.id_cliente,
                    id_brief=brief.id,
                    id_proyecto=new_record.id
                )
                db.session.add(new_brief)
                db.session.flush()
                preguntas=PreguntasDeBriefs.query.filter_by(id_brief=brief.id)
                for pregunta in preguntas:
                    new_pregunta=RespuestasDePreguntasDeBriefs(
                        id_visualizacion=get_id_visualizacion('respuestas_briefs_de_clientes'),
                        id_brief_de_cliente=new_brief.id,
                        id_pregunta_de_brief=pregunta.id
                    )
                    db.session.add(new_pregunta)
            # generar actividades generales
            actividades=ActividadesBase.query.filter_by(id_servicio=item.id_servicio)
            for actividad in actividades:
                new_actividad=Actividades(
                    id_visualizacion=get_id_visualizacion('actividades'),
                    id_actividad_base=actividad.id,
                    id_proyecto=new_record.id
                )
                db.session.add(new_actividad)
        db.session.commit()
        flash('La venta ha sido Completada.','success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al cobrar la Venta: {str(e)}", "danger")        
    return redirect(url_for('dynamic.table_view', table_name='ventas'))

@ventas_bp.route("/cancelar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
def cancelar(id):
    record=Ventas.query.get(id)
    if record.estatus=='En revisión':
        record.estatus="Cancelada"
        db.session.commit()
        flash('La venta ha sido Cancelada.','success')
    return redirect(url_for('dynamic.table_view', table_name='ventas'))
