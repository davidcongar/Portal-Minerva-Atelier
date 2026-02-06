from datetime import timedelta
from python.services.system.helper_functions import *
from python.models.modelos import *
from sqlalchemy import func
from python.services.dynamic_functions.general_functions import *


def get_variables_double_table_view(table_name):
    columns = {
        'compras': {
            'columns_first_table':['nombre','unidad_de_medida','precio_unitario'],
            'columns_second_table':['nombre','unidad_de_medida','cantidad_ordenada','precio_unitario','subtotal','descuento_porcentaje','importe_total','fecha_entrega_estimada'],
            'title_first_table':'Productos de proveedor',
            'title_second_table':'Productos en orden de compra',
            'query_first_table':'productos',
            'query_second_table':'productos_en_compras',
            'model_first_table':'productos',
            'model_second_table':'productos_en_compras',
            'details':['id_visualizacion','proveedor.nombre','importe_total'],
            'edit_fields':['cantidad_ordenada','descuento_porcentaje','subtotal','fecha_entrega_estimada'],
            'required_fields':[''],
            'url_confirm':'compras.confirm'                   
        },    
        'recepciones_de_compras': {
            'columns_first_table':['producto','unidad_de_medida','cantidad_ordenada','cantidad_por_recibir'],
            'columns_second_table':['producto','unidad_de_medida','cantidad'],
            'title_first_table':'Productos en compra',
            'title_second_table':'Productos en recepción',
            'query_first_table':'prod_compras',
            'query_second_table':'prod_recepcion',
            'model_first_table':'productos_en_compras',
            'model_second_table':'productos_en_recepciones_de_compras',
            'edit_fields':['cantidad','lote','fecha_de_caducidad'],
            'details':['id_visualizacion','compras.proveedor.nombre'],
            'required_fields':[''],
            'url_confirm':'recepciones_de_compras.confirm'  
        },  
        'transferencias_de_inventario': {
            'columns_first_table':['almacen','producto','cantidad_disponible'],
            'columns_second_table':['producto','cantidad','cantidad_disponible'],
            'title_first_table':'Inventario disponible',
            'title_second_table':'Productos a transferir',
            'query_first_table':'inventario_disponible',
            'query_second_table':'productos_en_transferencia_de_inventario',
            'model_first_table':'inventario',
            'model_second_table':'productos_en_transferencias_de_inventario',
            'details':['id_visualizacion','almacen_salida.nombre','almacen_entrada.nombre'],
            'edit_fields':['cantidad','id_posicion_de_sub_almacen_entrada'],
            'required_fields':[''],
            'url_confirm':'transferencias_de_inventario.confirm'  
        },    
        'pagos_administrativos': {
            'columns_first_table':['id_','tipo','proveedor','notas', 'importe_total','importe_pagado','importe_restante'],
            'columns_second_table':['tipo','proveedor','importe','importe_restante','notas'],
            'title_first_table':'Compras y Gastos de Proveedor',
            'title_second_table':'Compras y Gastos en Pago',
            'query_first_table':'compras_gastos_proveedor',
            'query_second_table':'compras_gastos_pago',
            'model_first_table':'gastos',
            'model_second_table':'gastos_y_compras_en_pagos',
            'details':['id_visualizacion','proveedor.nombre','importe'],
            'edit_fields':['notas','importe'],
            'required_fields':[''],
            'url_confirm':'pagos_administrativos.confirm'  
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

def on_add_double_table(table_name,id):
    if table_name=='compras':
        record=Compras.query.get(id)
        actualizar_compra(record)
    elif table_name=='pagos_administrativos':
        record=PagosAdministrativos.query.get(id)
        calcular_importe_pago(record)

def validate_delete(table_name,id):
    if table_name=='table_name':
        record=table_name.query.get(id)
        if record.column=='':
            return False
    return True

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