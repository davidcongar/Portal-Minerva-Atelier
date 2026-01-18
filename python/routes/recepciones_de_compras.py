
from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for,session

from python.models import db
from python.models.modelos import *
from python.services.system.authentication import *
from sqlalchemy.orm import joinedload
from sqlalchemy import String, Text, or_,func,desc
from datetime import date,timedelta
from python.services.system.helper_functions import *

recepciones_de_compras_bp = Blueprint("recepciones_de_compras", __name__,url_prefix="/recepciones_de_compras")

@recepciones_de_compras_bp.route("/aprobar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
@return_url_redirect
def aprobar(id):
    try:
        record=RecepcionesDeCompras.query.get(id)
        if record.estatuss=='En revisión':
            record.estatus="Aprobada"
            db.session.commit()
            flash('La recepción de recepcion de compra ha sido Aprobada.','success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al aprobar la recepción de recepcion de compra: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='recepciones_de_compras'))

@recepciones_de_compras_bp.route("/cancelar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
@return_url_redirect
def cancelar(id):
    try:
        record=RecepcionesDeCompras.query.get(id)
        if record.estatus in ('En revisión','Aprobada'):
            record.estatus="Cancelada"
            db.session.flush()
            productos=ProductosEnCompras.query.filter_by(id_compra=record.id_compra)
            for prod in productos:
                prod.cantidad_recibida = (db.session.query(func.sum(ProductosEnRecepcionesDeCompras.cantidad)).join(ProductosEnRecepcionesDeCompras.recepcion_de_compra).filter(RecepcionesDeCompras.id_compra == record.id_compra,RecepcionesDeCompras.estatus != 'Cancelada').scalar()or 0)
            db.session.commit()
            flash('La recepción de compra ha sido Cancelada.','success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al cancelar la recepción de compra: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='recepciones_de_compras'))

@recepciones_de_compras_bp.route("/finalizar/<id>", methods=["GET","POST"])
@login_required
@roles_required()
@return_url_redirect
def finalizar(id):
    try:
        record=RecepcionesDeCompras.query.get(id)
        if record.estatus in ('Aprobada'):
            record.estatus="Finalizada"
            productos=ProductosEnRecepcionesDeCompras.query.filter_by(id_recepcion_de_compra=id)
            for prod in productos:
                if prod.producto.inventariable=='Si':
                    inventario=Inventario.query.filter_by(id_almacen=record.id_almacen,id_producto=prod.id_producto).first()
                    if inventario:
                        inventario.cantidad=inventario.cantidad+prod.cantidad
                    else:
                        new_record=Inventario(
                            id_almacen=record.id_almacen,
                            id_producto=prod.id_producto,
                            cantidad=prod.cantidad,
                            id_usuario=session['id_usuario']
                        )
                        db.session.add(new_record)
            # compra
            compra=Compras.query.get(record.id_compra)
            compra.estatus='Recibida'
            productos=ProductosEnCompras.query.filter_by(id_compra=compra.id)
            for prod in productos:
                prod.estatus='Recibido'
                if prod.cantidad_recibida<prod.cantidad_ordenada:
                    prod.estatus='Recibido parcial'
                    compra.estatus='Recibida parcial'
            db.session.commit()
            flash('La recepción de compra ha sido Finalizada.','success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error al finalizar la recepción de compra: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='recepciones_de_compras'))

@recepciones_de_compras_bp.route("/confirm/<id>", methods=["GET","POST"])
@login_required
@roles_required()
@return_url_redirect
def confirm(id):
    try:
        record=RecepcionesDeCompras.query.get(id)
    except Exception as e:
        db.session.rollback()
        flash(f"Error al confirmar la recepción de compra: {str(e)}", "danger")
    return redirect(url_for('dynamic.table_view', table_name='recepciones_de_compras'))