
from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for,session

from python.models import db
from python.models.modelos import *
from python.services.system.authentication import *
from sqlalchemy.orm import joinedload
from sqlalchemy import String, Text, or_,func,desc
from datetime import date,timedelta
from python.services.system.helper_functions import *
from python.services.general_functions import *
import stripe

stripe.api_key = ''
YOUR_DOMAIN = 'http://localhost:8000'

ventas_bp = Blueprint("ventas", __name__,url_prefix="/ventas")

@ventas_bp.route("/create-checkout-session/<id>", methods=["GET","POST"])
def create_checkout_session(id):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1SaUD1RVK73dTUTMhdw7t1x3',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


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
