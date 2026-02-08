from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for,session

from python.models import db
from python.models.modelos import *
from python.services.system.authentication import *
from sqlalchemy.orm import joinedload
from sqlalchemy import String, Text, or_,func,desc
from datetime import date, timedelta
from python.services.system.helper_functions import *
import math

actividades_bp = Blueprint("actividades", __name__,url_prefix="/actividades")

@actividades_bp.route("/asignar", methods=["POST"])
@login_required
@csrf.exempt
def asignar():
    try:
        data = request.get_json()
        ids = data.get("ids", [])
        result = assign_activities(ids, db.session)
        db.session.commit()
        return jsonify({"success": True, "message": f"Se han asignado {result['assigned']} actividades."})

    except Exception as e:
        db.session.rollback()
        return jsonify({"danger": True, "message": f"Error al revisar: {str(e)}"}), 500

def assign_activities(ids, session):
    """
    Assign actividades grouped by project.
    Process:
        1. Group actividades by id_proyecto
        2. Assign all actividades for project A, then project B, etc.
        3. Greedy: assign to integrante with lowest workload
        4. Max 40 hours weekly
        5. No reassignment allowed
    """
    asignaciones_por_integrante = {}
    # ---- Step 1: Load actividades and integrantes ----
    actividades = (
        session.query(Actividades)
        .filter(Actividades.id.in_(ids),Actividades.estatus=='Sin iniciar')
        .all()
    )

    integrantes = (
        session.query(Integrantes)
        .filter(Integrantes.estatus == "Activo")
        .all()
    )

    if not integrantes:
        raise ValueError("No active integrantes available for assignment.")

    # ---- Step 2: Group actividades by project ----
    actividades_por_proyecto = {}
    for act in actividades:
        actividades_por_proyecto.setdefault(act.id_proyecto, []).append(act)

    # ---- Preload workload ----
    workload = {}  # integrante.id -> total hours
    for i in integrantes:
        hours = (
            session.query(db.func.coalesce(db.func.sum(Actividades.horas), 0))
            .filter(
                Actividades.id_integrante == i.id,
                Actividades.estatus != "Finalizada",
                Actividades.estatus != "Cancelada",
            )
            .scalar()
        )
        workload[i.id] = hours

    # ---- Helper: estimated end date ----
    def add_work_days(start_date, hours):
        days_needed = math.ceil(hours / 8)
        d = start_date
        while days_needed > 0:
            d += timedelta(days=1)
            if d.weekday() < 5:  # Mon–Fri
                days_needed -= 1
        return d

    today = date.today()
    assigned_count = 0

    # ---- Step 3: Assign activities project by project ----
    for project_id, acts in actividades_por_proyecto.items():

        # preserve original order inside each project
        for act in acts:

            # Skip already assigned activities
            if act.id_integrante is not None:
                continue

            horas_est = act.actividad_base.horas_estimadas

            # Find eligible integrante (greedy)
            eligible = sorted(
                [
                    i for i in integrantes
                    if workload[i.id] + horas_est <= 40
                ],
                key=lambda i: workload[i.id]
            )

            if not eligible:
                raise ValueError(
                    f"No integrante can take more work in project {project_id} "
                    "without exceeding 40h/week."
                )

            chosen = eligible[0]

            # Estimate dates
            fecha_inicio = today
            fecha_estimada = add_work_days(fecha_inicio, horas_est)

            # Assign activity
            act.id_integrante = chosen.id
            act.horas = horas_est
            act.fecha_inicio = fecha_inicio
            act.fecha_estimada = fecha_estimada
            act.estatus='En proceso'
            asignaciones_por_integrante.setdefault(chosen, []).append(act)
            workload[chosen.id] += horas_est
            assigned_count += 1
    if asignaciones_por_integrante:
        send_assignment_summary_emails(asignaciones_por_integrante)  
    return {"status": "ok", "assigned": assigned_count}

def send_assignment_summary_emails(asignaciones_por_integrante):
    """
    Recibe un diccionario:
    {
        integrante_obj: [actividad1, actividad2, ...],
        integrante_obj2: [...],
        ...
    }

    Envía un correo por integrante con el resumen de actividades asignadas.
    """
    for integrante, actividades in asignaciones_por_integrante.items():
        if not integrante.correo_electronico:
            continue  # Skip if integrante has no email
        # Build summary list
        try:
            details_list = []
            for act in actividades:
                details_list.append(
                    f"Cliente: {act.proyecto.cliente.nombre_completo} | "
                    f"ID Proyecto: {act.proyecto.id_visualizacion} | "
                    f"Actividad: {act.actividad_base.nombre} | "
                    f"Inicio: {act.fecha_inicio} | "
                    f"Entrega estimada: {act.fecha_estimada} | "
                    f"Horas estimadas: {act.horas}"
                )
            # Email body message
            body_content = (
                f"Hola {integrante.nombre_completo},<br><br>"
                "Se te han asignado nuevas actividades en el Portal Minerva Atelier.<br>"
                "Aquí tienes un resumen de tus tareas:"
            )
            send_html_email(
                subject="Nuevas actividades asignadas",
                recipient_email=integrante.correo_electronico,
                template="partials/system/email_template.html",
                body_content=body_content,
                details_list=details_list
            )
        except Exception as e:
            print(e)
            raise Exception(f"Error enviando correo a {integrante.nombre_completo}: {e}")