
from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for,session

from python.models import db
from python.models.modelos import *
from python.services.system.authentication import *
from sqlalchemy.orm import joinedload
from sqlalchemy import String, Text, or_,func,desc
from datetime import date,timedelta
from python.services.system.helper_functions import *

transferencias_de_inventario_bp = Blueprint('transferencias_de_inventario', __name__,url_prefix='/transferencias_de_inventario')

@transferencias_de_inventario_bp.route('/aprobar/<id>', methods=['GET','POST'])
@login_required
@roles_required()
@return_url_redirect
def aprobar(id):
    try:
        record=TransferenciasDeInventario.query.get(id)
        if record.estatus=='En revisión':
            record.estatus='Aprobada'
            db.session.commit()
            flash('La transferencia de inventario ha sido Aprobada.','success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al aprobar la transferencia de inventario: {str(e)}', 'danger')
    return redirect(url_for('dynamic.table_view', table_name='transferencias_de_inventario'))

@transferencias_de_inventario_bp.route('/cancelar/<id>', methods=['GET','POST'])
@login_required
@roles_required()
@return_url_redirect
def cancelar(id):
    try:
        record=TransferenciasDeInventario.query.get(id)
        if record.estatus in ('En revisión','Aprobada'):
            record.estatus='Cancelada'
            productos=ProductosEnTransferenciasDeInventario.query.filter_by(id_transferencia_de_inventario=id)
            for prod in productos:
                inventario_salida = Inventario.query.filter_by(id_almacen=record.id_almacen_salida,id_producto=prod.id_producto).first()
                inventario_salida.cantidad=inventario_salida.cantidad+prod.cantidad
                inventario_salida.cantidad_en_transito=inventario_salida.cantidad_en_transito-prod.cantidad
            db.session.commit()
            flash('La transferencia de inventario ha sido Cancelada.','success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cancelar la transferencia de inventario: {str(e)}', 'danger')
    return redirect(url_for('dynamic.table_view', table_name='transferencias_de_inventario'))

@transferencias_de_inventario_bp.route('/en_transito/<id>', methods=['GET'])
@login_required
@roles_required()
@return_url_redirect
def en_transito(id):
    try:
        record=TransferenciasDeInventario.query.get(id)
        if record.estatus=='Aprobada':
            record.estatus='En tránsito'
            db.session.commit()
            flash('La transferencia de inventario ha sido puesta En tránsito.','success')            
    except Exception as e:
        db.session.rollback()
        flash(f'Error al modificar estatus de la transferencia de inventario: {str(e)}', 'danger')
    return redirect(url_for('dynamic.table_view', table_name='transferencias_de_inventario'))

@transferencias_de_inventario_bp.route('/recibir/<id>', methods=['GET'])
@login_required
@roles_required()
@return_url_redirect
def recibir(id):
    try:
        record=TransferenciasDeInventario.query.get(id)
        if record.estatus=='En tránsito':
            return redirect(url_for('dynamic.table_view_input', main_table_name='transferencias_de_inventario',id=id))
    except Exception as e:
        db.session.rollback()
        flash(f'Error al recibir la transferencia de inventario: {str(e)}', 'danger')
    return redirect(url_for('dynamic.table_view', table_name='transferencias_de_inventario'))

@transferencias_de_inventario_bp.route('/finalizar/<id>', methods=['GET'])
@login_required
@roles_required()
@return_url_redirect
def finalizar(id):
    try:
        record=TransferenciasDeInventario.query.get(id)
        if record.estatus=='En tránsito':
            record.estatus='Finalizada'
            record.fecha_de_recepcion=date.today()
            productos=ProductosEnTransferenciasDeInventario.query.filter_by(id_transferencia_de_inventario=id)
            for prod in productos:
                inventario_salida = Inventario.query.filter_by(id_almacen=record.id_almacen_salida,id_producto=prod.id_producto).first()
                inventario_salida.cantidad_en_transito=inventario_salida.cantidad_en_transito-prod.cantidad
                inventario_entrada=Inventario.query.filter_by(id_almacen=record.id_almacen_entrada,id_producto=prod.id_producto).first()
                if inventario_entrada:
                    inventario_entrada.cantidad=inventario_entrada.cantidad+prod.cantidad
                else:
                    new_record=Inventario(
                        id_almacen=record.id_almacen_entrada,
                        id_producto=prod.id_producto,
                        cantidad=prod.cantidad,
                        id_usuario=session['id_usuario']
                    )
                    db.session.add(new_record)
            db.session.commit()
            flash('La transferencia de inventario se ha Finalizado.','success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al finalizar la transferencia de inventario: {str(e)}', 'danger')
    return redirect(url_for('dynamic.table_view', table_name='transferencias_de_inventario'))

@transferencias_de_inventario_bp.route('/confirm/<id>', methods=['GET','POST'])
@login_required
@roles_required()
def confirm(id):
    return redirect(url_for('dynamic.table_view', table_name='transferencias_de_inventario'))