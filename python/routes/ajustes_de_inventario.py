
from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for,session

from python.models import db
from python.models.modelos import *
from python.services.system.authentication import *
from sqlalchemy.orm import joinedload
from sqlalchemy import String, Text, or_,func,desc
from datetime import date,timedelta
from python.services.system.helper_functions import *

ajustes_de_inventario_bp = Blueprint("ajustes_de_inventario", __name__,url_prefix="/ajustes_de_inventario")


@ajustes_de_inventario_bp.route("/aprobar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
@return_url_redirect
def aprobar(id):
    try:
        record=AjustesDeInventario.query.get(id)
        if record.estatus in ('En revisión'):
            record.estatus="Aprobado"
            db.session.commit()
            flash('El ajuste de inventario ha sido Aprobado.','success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al aprobar el ajuste de inventario: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='ajustes_de_inventario'))


@ajustes_de_inventario_bp.route("/finalizar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
@return_url_redirect
def finalizar(id):
    try:
        record=AjustesDeInventario.query.get(id)
        if record.estatus=='Aprobado':
            record.estatus="Finalizado"
            if record.tipo_de_ajuste=='Entrada':
                inventario=Inventario.query.filter_by(id_almacen=record.id_almacen,id_producto=record.id_producto).first()
                if inventario:
                    inventario.cantidad=inventario.cantidad+record.cantidad
                else:
                    new_record=Inventario(
                        id_almacen=record.id_almacen,
                        id_producto=record.id_producto,
                        cantidad=record.cantidad,
                        id_usuario=session['id_usuario']
                    )
                    db.session.add(new_record)
            elif record.tipo_de_ajuste=='Salida':
                inventario=Inventario.query.filter_by(id_almacen=record.id_almacen,id_producto=record.id_producto).first()
                inventario.cantidad_en_transito=inventario.cantidad_en_transito-record.cantidad
            db.session.commit()
            flash('El ajuste de inventario ha sido Finalizado.','success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al finalizar el ajuste de inventario: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='ajustes_de_inventario'))

@ajustes_de_inventario_bp.route("/cancelar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
@return_url_redirect
def cancelar(id):
    try:
        record=AjustesDeInventario.query.get(id)
        if record.estatus in ('En revisión'):
            record.estatus="Cancelado"
            if record.tipo_de_ajuste=='Salida':
                inventario=Inventario.query.filter_by(id_almacen=record.id_almacen,id_producto=record.id_producto).first()
                inventario.cantidad_en_transito=inventario.cantidad_en_transito-record.cantidad
                inventario.cantidad=inventario.cantidad+record.cantidad
            db.session.commit()
            flash('El ajuste de inventario ha sido Cancelado.','success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al cancelar el ajuste de inventario: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='ajustes_de_inventario'))

@ajustes_de_inventario_bp.route("/revision_salida/<id_almacen>/<id_producto>/<cantidad>", methods=["GET","POST"])
@login_required
def revision_salida(id_almacen,id_producto,cantidad):
    inventario=Inventario.query.filter_by(id_almacen=id_almacen,id_producto=id_producto).first()
    if inventario:
        if float(cantidad)>inventario.cantidad:
            status='warning'
            message="La cantidad disponible, "+str(inventario.cantidad)+", es menor a la cantidad ingresada, "+cantidad
        else:
            status='success'
            message='ok'
    else:
        status='warning'
        message="El producto seleccionado no existe en el almacén seleccionado. Favor de revisar."
    return jsonify({"status": status, "message": message})

