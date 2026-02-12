from datetime import timedelta
from python.services.system.helper_functions import *
from python.models.modelos import *
from sqlalchemy import func
from python.services.dynamic_functions.general_functions import *

def get_variables_table_view_input(table_name):
    columns = {
        'transferencias_de_inventario': {
            'columns':['producto','cantidad_enviada','cantidad_recibida','notas'],
            'table_title':'Productos en Transferencia',
            'query_table':'productos_en_transferencias_de_inventario',
            'table_name':'productos_en_transferencias_de_inventario',
            'edit_fields':['cantidad_recibida','notas'],
            'required_fields':['cantidad_recibida'],
            'details':['almacen_salida.nombre','almacen_entrada.nombre'],
            'url_confirm':'transferencias_de_inventario.finalizar',
            'delete_button':'no',
            'add_button':'no'
        },
        'pagos_de_nomina': {
            'columns':['integrante','sueldo_bruto','bono','sueldo_bruto_real','deduccion_imss','deduccion_isr','total_deducciones','ajuste','sueldo_neto','notas'],
            'table_title':'Sueldos a pagar',
            'query_table':'sueldos_a_pagar',
            'table_name':'sueldos_pagados_en_nomina',
            'edit_fields':['bono','deduccion_imss','deduccion_isr','ajuste','notas'],
            'required_fields':['bono','deduccion_imss','deduccion_isr','ajuste'],
            'details':['fecha_inicio','fecha_fin','importe_total'],
            'url_confirm':'pagos_de_nomina.confirm',
            'delete_button':'si',
            'add_button':'si'
        },             
    }
    columns=columns.get(table_name,'')
    return columns


def get_update_validation(table_name,record,column,value):
    validation={}
    validation['status']=1    
    if table_name=='productos_en_compras' and column in ('cantidad_ordenada','descuento_porcentaje','precio_unitario'):
        if column=='cantidad_ordenada':
            record.subtotal=float(value)*record.precio_unitario
            record.importe_total=record.subtotal*(100-record.descuento_porcentaje)/100   
        elif column=='descuento_porcentaje':
            if float(value)>=100:
                validation['message']='El porcentaje de descuento no puede ser mayor a 100.'
                validation['status']=0
                validation['value_warning']=record.descuento_porcentaje
            else:
                record.importe_total=record.subtotal*(100-float(value))/100  
        elif column=='precio_unitario':
            record.subtotal=float(value)*record.cantidad_ordenada
            record.importe_total=record.subtotal*(100-record.descuento_porcentaje)/100   
    elif table_name=='productos_en_recepciones_de_compras' and column in ('cantidad'):
        recepcion=RecepcionesDeCompras.query.get(record.id_recepcion_de_compra)
        oc=Compras.query.get(recepcion.id_compra)
        prod_oc=ProductosEnCompras.query.filter_by(id_compra=oc.id,id_producto=record.id_producto).first()
        cantidad_global=prod_oc.cantidad_recibida-record.cantidad+float(value)
        if cantidad_global>prod_oc.cantidad_ordenada:
            validation['status']=0
            validation['value_warning']=prod_oc.cantidad_recibida
            validation['message']=f'La cantidad a recibir no puede ser mayor a la cantidad faltante de recibir, {prod_oc.cantidad_ordenada-prod_oc.cantidad_recibida}'
        else:
            prod_oc.cantidad_recibida=cantidad_global
            db.session.flush()
    elif table_name=='productos_en_transferencias_de_inventario':
        if column=='cantidad':
            inventario=Inventario.query.filter_by(id_almacen=record.transferencia_de_inventario.id_almacen_salida,id_producto=record.id_producto).first()
            cantidad_disponible=inventario.cantidad+record.cantidad
            if float(value)>cantidad_disponible:
                validation['status']=0
                validation['value_warning']=record.cantidad         
                validation['message']='La cantidad a transferir no puede ser mayor a la cantidad disponible en inventario.'
            else:
                # agregar a no disponible
                inventario.cantidad=inventario.cantidad+record.cantidad-float(value)
                inventario.cantidad_en_transito=inventario.cantidad_en_transito-record.cantidad+float(value)
                record.cantidad_recibida=value
        elif column=='cantidad_recibida':
            if float(value)>record.cantidad:
                validation['status']=0
                validation['value_warning']=record.cantidad
                record.cantidad_recibida=record.cantidad
                db.session.commit()
                validation['message']='La cantidad a recibir no puede ser mayor a la cantidad enviada.'
    elif table_name=='gastos_y_compras_en_pagos':
        if record.id_gasto:
            main_record=Gastos.query.get(record.id_gasto)
            importe_pagado=(
                    db.session.query(func.sum(GastosYComprasEnPagos.importe))
                    .join(PagosAdministrativos, GastosYComprasEnPagos.id_pago == PagosAdministrativos.id)
                    .filter(GastosYComprasEnPagos.id_gasto == record.id_gasto,GastosYComprasEnPagos.id!=record.id)
                    .filter(PagosAdministrativos.estatus != 'Cancelado')
                    .scalar()
                ) or 0
            importe_restante=main_record.importe-importe_pagado
        else:
            main_record=Compras.query.get(record.id_compra)
            importe_pagado=(
                    db.session.query(func.sum(GastosYComprasEnPagos.importe))
                    .join(PagosAdministrativos, GastosYComprasEnPagos.id_pago == PagosAdministrativos.id)
                    .filter(GastosYComprasEnPagos.id_compra == record.id_compra,GastosYComprasEnPagos.id!=record.id)
                    .filter(PagosAdministrativos.estatus != 'Cancelado')
                    .scalar()
                ) or 0
            importe_restante=main_record.importe_total-importe_pagado    
        if float(value)>importe_restante:
            validation['status']=0
            validation['message']='El importe no puede ser mayor al importe restante.'
            validation['value_warning']=importe_restante
        else:
            main_record.importe_pagado=main_record.importe_pagado-record.importe+float(value)
    return validation

