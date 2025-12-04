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
        "transferencias_de_inventario": {
            "columns_first_table":["almacen","producto","cantidad_disponible"],
            "columns_second_table":["producto","cantidad","cantidad_disponible"],
            "title_first_table":"Inventario disponible",
            "title_second_table":"Productos a transferir",
            "query_first_table":"inventario_disponible",
            "query_second_table":"productos_en_transferencia_de_inventario",
            "model_first_table":"inventario",
            "model_second_table":"productos_en_transferencias_de_inventario",
            "details":["id_visualizacion","almacen_entrada","almacen_salida"],
            "edit_fields":['cantidad',"id_posicion_de_sub_almacen_entrada"],
        },    
        "pagos_administrativos": {
            "columns_first_table":["id_","tipo","proveedor","notas", "importe_total","importe_pagado","importe_restante"],
            "columns_second_table":["tipo","proveedor","importe","importe_restante","notas"],
            "title_first_table":"Compras y Gastos de Proveedor",
            "title_second_table":"Compras y Gastos en Pago",
            "query_first_table":"compras_gastos_proveedor",
            "query_second_table":"compras_gastos_pago",
            "model_first_table":"gastos",
            "model_second_table":"gastos_y_compras_en_pagos",
            "details":["id_visualizacion","proveedor","importe"],
            "edit_fields":['notas','importe']
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
    elif main_table_name=='transferencias_de_inventario':
        inventario=Inventario.query.get(id_record)
        new_record=model(
            id_transferencia_de_inventario=id_main_record,
            id_producto=inventario.id_producto,
            cantidad=0,
            id_usuario=session['id_usuario']
        )   
    elif main_table_name=='pagos_administrativos':
        new_record=model(
            id_pago=id_main_record,
            importe=0,
            id_usuario=session['id_usuario']
        )
        compra=Compras.query.get(id_record)
        if compra:
            new_record.id_compra=compra.id
            new_record.importe=compra.importe_total-compra.importe_pagado
            compra.importe_pagado=new_record.importe
        else:
            gasto=Gastos.query.get(id_record)
            new_record.id_gasto=gasto.id
            new_record.importe=gasto.importe-gasto.importe_pagado
            gasto.importe_pagado=new_record.importe             
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
    elif table_name=='productos_en_transferencias_de_inventario':
        if column=='cantidad':
            inventario=Inventario.query.filter_by(id_almacen=record.transferencia_de_inventario.id_almacen_salida,id_producto=record.id_producto).first()
            cantidad_disponible=inventario.cantidad+record.cantidad
            if float(value)>cantidad_disponible:
                validation['status']=0
                validation['value_warning']=record.cantidad         
                validation['message']="La cantidad a transferir no puede ser mayor a la cantidad disponible en inventario."
            else:
                # agregar a no disponible
                inventario.cantidad=inventario.cantidad+record.cantidad-float(value)
                inventario.cantidad_en_transito=inventario.cantidad_en_transito-record.cantidad+float(value)
                validation['status']=1
    elif table_name=='gastos_y_compras_en_pagos':
        if record.id_gasto:
            main_record=Gastos.query.get(record.id_gasto)
            importe_pagado=(
                    db.session.query(func.sum(GastosYComprasEnPagos.importe))
                    .join(PagosAdministrativos, GastosYComprasEnPagos.id_pago == PagosAdministrativos.id)
                    .filter(GastosYComprasEnPagos.id_gasto == record.id_gasto,GastosYComprasEnPagos.id!=record.id)
                    .filter(PagosAdministrativos.estatus != "Cancelado")
                    .scalar()
                ) or 0
            importe_restante=main_record.importe-importe_pagado
        else:
            main_record=Compras.query.get(record.id_compra)
            importe_pagado=(
                    db.session.query(func.sum(GastosYComprasEnPagos.importe))
                    .join(PagosAdministrativos, GastosYComprasEnPagos.id_pago == PagosAdministrativos.id)
                    .filter(GastosYComprasEnPagos.id_compra == record.id_compra,GastosYComprasEnPagos.id!=record.id)
                    .filter(PagosAdministrativos.estatus != "Cancelado")
                    .scalar()
                ) or 0
            importe_restante=main_record.importe_total-importe_pagado    
        if float(value)>importe_restante:
            validation['status']=0
            validation['message']="El importe no puede ser mayor al importe restante."
            validation['value_warning']=importe_restante
        else:
            main_record.importe_pagado=main_record.importe_pagado-record.importe+float(value)
            validation['status']=1                                       
    else:
        validation['status']=1
    return validation

def get_variables_table_view_input(table_name):
    columns = {
        "briefs_de_clientes": {
            "columns":["pregunta","respuesta"],
            "table_title":"Preguntas de Brief",
            "query_table":"respuestas_briefs_de_clientes",
            "table_name":"respuestas_briefs_de_clientes",
            "url_confirm":"briefs_de_clientes.confirmar",
            "details":['cliente','brief'],
            "edit_fields":['respuesta']
        },
    }
    columns=columns.get(table_name,'')
    return columns


def on_add_double_table(table_name,id):
    if table_name=='compras':
        record=Compras.query.get(id)
        actualizar_compra(record)
    elif table_name=='pagos_administrativos':
        record=PagosAdministrativos.query.get(id)
        calcular_importe_pago(record)

def on_update_double_table(table_name,id):
    if table_name=='productos_en_compras':
        record=ProductosEnCompras.query.get(id)
        record=Compras.query.get(record.id_compra)
        actualizar_compra(record)
    elif table_name=='gastos_y_compras_en_pagos':
        record=GastosYComprasEnPagos.query.get(id)
        record=PagosAdministrativos.query.get(record.id_pago)
        calcular_importe_pago(record) 

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
    elif table_name=='productos_en_transferencias_de_inventario':
        record=ProductosEnTransferenciasDeInventario.query.get(id)
        inventario=Inventario.query.filter_by(id_almacen=record.transferencia_de_inventario.id_almacen_salida,id_producto=record.id_producto).first()
        inventario.cantidad=inventario.cantidad+record.cantidad
        inventario.cantidad_en_transito=inventario.cantidad_en_transito-record.cantidad
    elif table_name=='pagos_administrativos':
        pago=PagosAdministrativos.query.get(id)
        calcular_importe_pago(pago)        