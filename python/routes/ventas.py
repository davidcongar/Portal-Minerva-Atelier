
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

import stripe
#4242424242424242
YOUR_DOMAIN = 'http://localhost:8000'

ventas_bp = Blueprint("ventas", __name__,url_prefix="/ventas")

@ventas_bp.route("/create-checkout-session/<id>", methods=["GET","POST"])
def create_checkout_session(id):
    try:
        venta=Ventas.query.get(id)
        if venta.estatus!='Cobrada':
            items=ServiciosEnVentas.query.filter_by(id_venta=id).all()
            line_items=[]
            for item in items:
                line_items.append({
                    "price": item.id_precio_stripe,
                    "quantity": int(item.cantidad)
                })
            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                mode='payment',
                success_url=f"{YOUR_DOMAIN}/ventas/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{YOUR_DOMAIN}/ventas/cancelar",
                payment_intent_data={'metadata':{'id_venta':id}},
                metadata={"id_venta": id}
            )
            return redirect(checkout_session.url, code=303)
        else:
            flash(f"La venta ya fue cobrada.", "info")
    except Exception as e:
        flash(f"Error al generar la compra: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='ventas'))

@ventas_bp.route("/success")
def success():
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
            "En el transcurso de las siguientes 24 horas un experto te contactara para agendar una cita y poder avanzar con tu proyecto.<br>"
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
            id_venta=venta.id,
            id_servicio=item.id_servicio,
            id_espacio_de_proyecto = item.id_espacio_de_proyecto,
            metros_cuadrados=item.metros_cuadrados,
            fecha_inicio = datetime.today()
        )
        db.session.add(new_record)
    db.session.commit()
    flash('La venta ha sido Completada.','success')
    return redirect(url_for('dynamic.table_view', table_name='ventas'))

'''
@ventas_bp.route("/webhook", methods=["POST"])
def stripe_webhook():

    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    endpoint_secret = "whsec_..."

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        return {"error": str(e)}, 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        venta_id = session["metadata"].get("venta_id")
        payment_intent_id = session["payment_intent"]

        print("Venta ID:", venta_id)
        print("PaymentIntent:", payment_intent_id)

        # 🔒 SAFELY UPDATE YOUR DB HERE
        venta = Venta.query.get(venta_id)
        venta.estado = "pagado"
        venta.stripe_payment_intent = payment_intent_id
        db.session.commit()

    return {"status": "ok"}
'''


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
