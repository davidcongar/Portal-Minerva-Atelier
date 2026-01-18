
from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for,session

from python.models import db
from python.models.modelos import *
from python.services.system.authentication import *
from sqlalchemy.orm import joinedload
from sqlalchemy import String, Text, or_,func,desc
from datetime import date,timedelta
from python.services.system.helper_functions import *

clientes_bp = Blueprint("clientes", __name__,url_prefix="/clientes")

@clientes_bp.route("/activar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
@return_url_redirect
def activar(id):
    try:
        record=Clientes.query.get(id)
        if record.estatus in ('Perfect match','Swipe'):
            record.estatus='Activo'
            db.session.commit()
            alphabet = string.ascii_letters + string.digits
            contrasena = ''.join(secrets.choice(alphabet) for i in range(20))
            send_html_email(
                subject="Minerva Atelier - Activación de cuenta",
                recipient_email=record.correo_electronico,
                template="partials/system/email_template.html",
                sender_name="Minerva Atelier",
                body_content=f"Se acaba de activar tu cuenta en el portal de <strong>Minerva Atelier</strong>. <br>A continuación se detalla tus credenciales.",
                details_list=[
                    "URL Plataforma: clientes.minervaatelier.com",
                    f"Correo electrónico: {record.correo_electronico}",
                    f"Contraseña: {contrasena}"
                ]
            )  
            flash(f"El cliente fue Activado.", "success")
            return redirect(url_for('dynamic.table_view', table_name='clientes'))
    except Exception as e:
        db.session.rollback()
        flash(f"Error al activar el cliente: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='clientes'))

@clientes_bp.route("/perdido/<id>", methods=["GET","POST"])
@login_required
@roles_required()
@return_url_redirect
def perdido(id):
    try:
        record=Clientes.query.get(id)
        if record.estatus in ('Perfect match','Swipe'):
            record.estatus='Perdido'
            db.session.commit()
            flash(f"El cliente fue Perdido.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al cambiar estatus del cliente: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='clientes'))
