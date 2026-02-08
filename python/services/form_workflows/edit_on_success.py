
from python.models.modelos import *
from sqlalchemy import String, Text, or_,func,Integer, Float, Numeric
from sqlalchemy.sql import case
from flask import session,flash
import re
import json
from datetime import date, datetime
from python.services.dynamic_functions.general_functions import *
from python.services.system.helper_functions import *
from python.services.system.email import *
from python.services.stripe import *

#####
# funciones de formularios
#####

HANDLERS = {}

def handler_edit_on_success(*tables):
    def wrapper(fn):
        for t in tables:
            HANDLERS[t] = fn
        return fn
    return wrapper

def edit_on_success(table_name, id,changed_fields):
    handler = HANDLERS.get(table_name)
    if not handler:
        return
    return handler(id,changed_fields)

@handler_edit_on_success('agenda')
def agenda(id,changed_fields):
    record=Agenda.query.get(id)
    if record.id_integrante and record.estatus=='Pendiente':
        fecha_changed, fecha_old, fecha_new = field_changed(changed_fields, "fecha")
        hora_changed, hora_old, hora_new = field_changed(changed_fields, "hora_inicio")
        if fecha_changed or hora_changed:
            send_html_email(
                subject="Minerva Atelier - Modificación de cita",
                recipient_email=record.cliente.correo_electronico,
                template="partials/system/email_template.html",
                sender_name="Minerva Atelier",
                body_content = (
                    "Se tuvo que modificar la cita previamente agendada; disculpa cualquier inconveniente que esto pueda causar.<br>"
                    "Para confirmar la nueva cita, por favor envía un correo al experto asignado.<br>"
                    "A continuación se encuentran los detalles de la nueva cita."
                ),
                details_list=[
                    f"Fecha: {record.fecha}",
                    f"Hora: {record.hora_inicio}",
                    f"Experto asignado: {record.integrante.nombre_completo}",
                    f"Correo: {record.integrante.correo_electronico}",
                ]
            )    
            flash(f"Se ha enviado un correo al cliente para confirmar la nueva fecha/horario.", "info")
        else:
            send_html_email(
                subject="Minerva Atelier - Confirmación de cita",
                recipient_email=record.cliente.correo_electronico,
                template="partials/system/email_template.html",
                sender_name="Minerva Atelier",
                body_content = (
                    "Se acaba de confirmar tu cita con uno de nuestros expertos de <strong>Minerva Atelier</strong>.<br>"
                    "Cualquier cambio que requieras, por favor envía un correo al experto asignado.<br>"
                    "A continuación se encuentran los detalles de la cita."
                ),
                details_list=[
                    f"Fecha: {record.fecha}",
                    f"Hora: {record.hora_inicio}",
                    f"Experto asignado: {record.integrante.nombre_completo}",
                    f"Correo: {record.integrante.correo_electronico}",
                ]
            )    
            record.estatus='Confirmada'          
            flash(f"La cita ha sido Confirmada.", "success")

@handler_edit_on_success('actividades')
def actividades(id,changed_fields):
    record=Actividades.query.get(id)
    integrante_changed= field_changed(changed_fields, "id_integrante")
    print(integrante_changed)
    if record.estatus in ('Sin iniciar','En proceso') and integrante_changed:
        record.estatus='En proceso'
        record.fecha_inicio=datetime.today()
        send_html_email(
            subject="Minerva Atelier - Asignación de actividad",
            recipient_email=record.integrante.correo_electronico,
            template="partials/system/email_template.html",
            sender_name="Minerva Atelier",
            body_content = (
                "Se acaba de asignar una actividad nueva en el portal de <strong>Minerva Atelier</strong>.<br>"
            ),
            details_list=[
                f"Cliente: {record.proyecto.cliente.nombre_completo} | "
                f"ID Proyecto: {record.proyecto.id_visualizacion} | "
                f"Actividad: {record.actividad_base.nombre} | "
                f"Inicio: {record.fecha_inicio} | "
                f"Entrega estimada: {record.fecha_estimada} | "
                f"Horas estimadas: {record.horas}"                
            ]
        )    

@handler_edit_on_success('precios_de_servicios')
def precios_de_servicios(id,changed_fields):
    precio_changed = field_changed(changed_fields, "precio_uhnitario")
    if precio_changed:
        modify_price(id)