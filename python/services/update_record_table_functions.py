from datetime import timedelta
from python.services.system.helper_functions import *
from python.models.modelos import *
from sqlalchemy import func
from python.services.general_functions import *

def get_variables_double_table_view(table_name):
    columns = {
        "compras": {
            "columns_first_table":["nombre","unidad_de_medida","precio_unitario"],
            "columns_second_table":["nombre","unidad_de_medida","cantidad_ordenada","precio_unitario","subtotal","descuento_porcentaje","importe_total","fecha_entrega_estimada"],
            "title_first_table":"Productos de proveedor",
            "title_second_table":"Productos en orden de compra",
            "query_first_table":"productos",
            "query_second_table":"productos_en_compras",
            "model_first_table":"productos",
            "model_second_table":"productos_en_compras",
            "details":["id_visualizacion","proveedor",'importe_total'],
            "edit_fields":['cantidad_ordenada','descuento_porcentaje','subtotal','fecha_entrega_estimada']
        },    
        "recepciones_de_compras": {
            "columns_first_table":["producto","unidad_de_medida","cantidad_ordenada","cantidad_por_recibir"],
            "columns_second_table":["producto","unidad_de_medida","cantidad"],
            "title_first_table":"Productos en compra",
            "title_second_table":"Productos en recepción",
            "query_first_table":"prod_compras",
            "query_second_table":"prod_recepcion",
            "model_first_table":"productos_en_compras",
            "model_second_table":"productos_en_recepciones_de_compras",
            "edit_fields":['cantidad','lote','fecha_de_caducidad'],
            "details":["id_visualizacion"]
        },         
    }
    columns=columns.get(table_name,'')
    return columns

def add_record_double_table(main_table_name,second_table,id_main_record,id_record):
    model=get_model_by_name(second_table)
    if main_table_name=='compras':
        compra=Compras.query.get(id_main_record)
        precio=PreciosDeProveedores.query.filter_by(id_proveedor=compra.id_proveedor,id_producto=id_record).first()
        new_record=model(
            id_compra=id_main_record,
            id_producto=id_record,
            precio_unitario=precio.precio_unitario,
            cantidad_ordenada=0,
            cantidad_recibida=0,
            descuento_porcentaje=0,
            subtotal=0,
            fecha_entrega_estimada=compra.fecha_entrega_estimada,
            id_usuario=session['id_usuario']
        )
    elif main_table_name=='recepciones_de_compras':
        record=ProductosEnCompras.query.get(id_record)
        new_record=model(
            id_recepcion_de_compra=id_main_record,
            id_producto=record.id_producto,
            cantidad=0,
            id_usuario=session['id_usuario']
        )
    return new_record

def get_update_validation(table_name,record,column,value):
    validation={}
    if table_name=='productos_en_compras' and column in ('cantidad_ordenada','descuento_porcentaje','precio_unitario'):
        if column=='cantidad_ordenada':
            record.subtotal=float(value)*record.precio_unitario
            record.importe_total=record.subtotal*(100-record.descuento_porcentaje)/100   
        elif column=='descuento_porcentaje':
            record.importe_total=record.subtotal*(100-float(value))/100      
        elif column=='precio_unitario':
            record.subtotal=float(value)*record.cantidad_ordenada
            record.importe_total=record.subtotal*(100-record.descuento_porcentaje)/100   
        validation['status']=1
    elif table_name=='productos_en_recepciones_de_compras' and column in ('cantidad'):
        recepcion=RecepcionesDeCompras.query.get(record.id_recepcion_de_compra)
        oc=Compras.query.get(recepcion.id_compra)
        prod_oc=ProductosEnCompras.query.filter_by(id_compra=oc.id,id_producto=record.id_producto).first()
        cantidad_global=prod_oc.cantidad_recibida-record.cantidad+float(value)
        if cantidad_global>prod_oc.cantidad_ordenada:
            validation['status']=0
            validation['value_warning']=prod_oc.cantidad_recibida          
            validation['message']="La cantidad a recibir no puede ser mayor a la cantidad ordenada."
        else:
            prod_oc.cantidad_recibida=cantidad_global
            validation['status']=1
            db.session.flush()        
    else:
        validation['status']=1
    return validation

def get_variables_table_view_input(table_name):
    columns = {
        "ejemplo": {
            "columns":["nombre","cantidad_ordenada","cantidad_recibida_anteriormente","cantidad_recibida","notas","estatus"],
            "table_title":"Productos en orden de compra",
            "query_table":"productos_en_orden_de_compra",
            "table_name":"productos_en_ordenes_de_compra",
            "url_confirm":"ordenes_de_compra.confirmar",
            "details":['proveedor','fecha_orden'],
            "edit_fields":['cantidad_recibida',"notas"]
        },
    }
    columns=columns.get(table_name,'')
    return columns


def on_add_double_table(table_name,id):
    if table_name=='compras':
        record=Compras.query.get(id)
        actualizar_compra(record)

def on_update_double_table(table_name,id):
    if table_name=='productos_en_compras':
        record=ProductosEnCompras.query.get(id)
        record=Compras.query.get(record.id_compra)
        actualizar_compra(record)

def on_delete_double_table(table_name,id):
    if table_name=='compras':
        record=Compras.query.get(id)
        actualizar_compra(record)
    elif table_name=='productos_en_recepciones_de_compras':
        record=ProductosEnRecepcionesDeCompras.query.get(id)
        recepcion=RecepcionesDeCompras.query.get(record.id_recepcion_de_compra)
        oc=Compras.query.get(recepcion.id_compra)
        prod_oc=ProductosEnCompras.query.filter_by(id_compra=oc.id,id_producto=record.id_producto).first()
        prod_oc.cantidad_recibida=prod_oc.cantidad_recibida-record.cantidad
