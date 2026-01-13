from python.models.modelos import *
from sqlalchemy import func
from python.services.system.helper_functions import *
from flask import  jsonify
from datetime import timedelta
from python.services.dynamic_functions.double_tables import *
from python.services.dynamic_functions.input_tables import *

def get_foreign_options():
    foreign_options = {
        "id_rol": Roles.query.filter_by(estatus="Activo"),
        "id_categoria_de_reporte":CategoriasDeReportes.query.filter_by(estatus="Activo"),
        "id_integrante":Integrantes.query.filter_by(estatus="Activo"),
        "id_puesto":Puestos.query.filter_by(estatus="Activo"),
        "id_cuenta_de_banco":CuentasDeBanco.query.filter_by(estatus="Activo"),
        "id_cuenta_de_banco_entrada":CuentasDeBanco.query.filter_by(estatus="Activo"),
        "id_cuenta_de_banco_salida":CuentasDeBanco.query.filter_by(estatus="Activo"),
        "id_servicio":Servicios.query.filter_by(estatus="Activo"),
        "id_brief":Briefs.query.filter_by(estatus="Activo"),
        "id_categoria_de_gasto":CategoriasDeGastos.query.filter_by(estatus="Activo"),
        "id_proveedor":Proveedores.query.filter_by(estatus="Activo"),
        "id_almacen":Almacenes.query.filter_by(estatus="Activo"),
        "id_categoria_de_producto": CategoriasDeProductos.query.filter_by(estatus="Activo"),
        "id_producto": Productos.query.filter_by(estatus="Activo"),
        "id_compra": Compras.query.filter(Compras.estatus.in_(["Aprobada", "Recibida parcial"])),
        "id_almacen_salida":Almacenes.query.filter_by(estatus="Activo"),
        "id_almacen_entrada":Almacenes.query.filter_by(estatus="Activo"),
        "id_cliente":Clientes.query.filter_by(estatus="Activo"),
        "id_cliente": Clientes.query.filter(Clientes.estatus.in_(["En proceso", "Activo"])),
        "id_proyecto":Proyectos.query.filter_by(estatus="Activo"),

        # --- Campos con opciones fijas ---
        "regimen_fiscal":['601 - General de Ley Personas Morales','603 - Personas Morales con Fines no Lucrativos','605 - Sueldos y Salarios e Ingresos Asimilados a Salarios','606 - Arrendamiento','607 - Régimen de Enajenación o Adquisición de Bienes','608 - Demás ingresos','610 - Residentes en el Extranjero sin Establecimiento Permanente en México','611 - Ingresos por Dividendos (socios y accionistas)','612 - Personas Físicas con Actividades Empresariales y Profesionales','614 - Ingresos por intereses','615 - Régimen de los ingresos por obtención de premios','616 - Sin obligaciones fiscales','620 - Sociedades Cooperativas de Producción que optan por diferir sus ingresos','621 - Incorporación Fiscal (ya derogado, solo histórico)','622 - Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras (Personas Morales)','623 - Opcional para Grupos de Sociedades','624 - Coordinados','625 - Régimen de las Actividades Empresariales con ingresos a través de Plataformas Tecnológicas','626 - Régimen Simplificado de Confianza (RESICO)',],
        "forma_de_pago":['01 - Efectivo','02 - Cheque nominativo','03 - Transferencia electrónica de fondos','04 - Tarjeta de crédito','05 - Monedero electrónico','06 - Dinero electrónico','08 - Vales de despensa','12 - Dación en pago','13 - Pago por subrogación','14 - Pago por consignación','15 - Condonación','17 - Compensación','23 - Novación','24 - Confusión','25 - Remisión de deuda','26 - Prescripción o caducidad','27 - A satisfacción del acreedor','28 - Tarjeta de débito','29 - Tarjeta de servicios','30 - Aplicación de anticipos','31 - Intermediario de pagos','99 - Por definir'],
        "metodo_de_pago":['PUE','PPD'],
        "uso_de_cfdi":['G01 Adquisición de mercancías','G02 Devolución, descuentos o bonificaciones','G03 Gastos en general','I01 Construcciones','I02 Mobiliario y equipo de oficina por inversiones','I03 Equipo de transporte','I04 Equipo de cómputo y accesorios','I05 Dados, troqueles, moldes, matrices y herramental','I06 Comunicaciones telefónicas','I07 Comunicaciones satelitales','I08 Otra maquinaria y equipo','D01 Honorarios médicos, dentales y gastos hospitalarios','D02 Gastos médicos por incapacidad o discapacidad','D03 Gastos funerales','D04 Donativos','D05 Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación)','D06 Aportaciones voluntarias al SAR','D07 Primas por seguros de gastos médicos','D08 Gastos de transportación escolar obligatoria','D09 Depósitos en cuentas para el ahorro, primas que tengan como base planes de pensiones','D10 Pagos por servicios educativos (colegiaturas)','S01 Sin efectos fiscales','CP01 Pagos','CN01 Nómina'],
        "tipo_de_ajuste": ["Entrada", "Salida"],
        "estado_civil": ["Soltero/a", "Casado/a"],
        "genero": ["Masculino", "Femenino"],
        "tipo_de_cuenta":["Efectivo","Débito","Crédito"],
        "prioridad":["P0","P1","P2","P3"],
        "inventariable":["Si","No"],
        "unidad_de_medida":["Pieza","Caja"],
        "tipo_de_iva":["16%","0%","8%"],
        "espacio_de_proyecto":["Oficina","Cuarto principal","Cuarto de visitas","Sala","Comedor","Sala de TV","Cocina"],

    }
    return foreign_options


# specific filters for forms
def get_form_options(table_name):
    options = {
        #"integr": {"id_producto": Productos.query.filter(Productos.estatus == "Activo",Productos.categoria.has(CategoriasDeProductos.nombre.in_(["Producto terminado", "Producto intermedio"])))},
    }
    options=options.get(table_name,{})
    return options

def get_multiple_choice_data():
    multiple_choice_data = {}
    options = {
        "tags": ['Lunes','Martes','Miércoles'],
    }      
    for i in options:
        multiple_choice_data[i] = {
            "selected": [],
            "options": options[i]
        }
    return multiple_choice_data

def get_ignored_columns(table_name):
    columnas_generales = {'fecha_de_creacion', 'estatus', 'id_usuario', 'id_visualizacion', 'fecha_de_actualizacion'}
    columns = {
        "usuarios":{'codigo_unico','id_rol','contrasena','contrasena_api','intentos_de_inicio_de_sesion','ultima_sesion','ultimo_cambio_de_contrasena','codigo_unico_expira'},
        "archivos":{'tabla_origen','id_registro','nombre','ruta_s3'},
        "proyectos":{'importe_cobrado','fecha_fin'},
        "gastos": {'importe_pagado'},
        "compras": {'importe_total','subtotal','descuentos','estatus_de_pago','importe_pagado'},
        "pagos": {'importe'},  
        "clientes": {'rfc','razon_social','regimen_fiscal','domicilio_fiscal','direccion','codigo_postal','telefono','contrasena'},  
        "cuentas_de_banco": {'balance'},
        "facturas": {'importe_total','impuestos','subtotal','importe_cobrado'},
        "integrantes": {'fecha_terminacion'},
        "actividades": {'notas_cierre','notas_cambios','fecha_realizado','fecha_cerrado','horas'},
        "pagos_administrativos":{'importe'},
        "briefs_de_clientes":{'fecha_cierre'},
        "agenda":{'id_integrante','hora_fin','motivo_de_cancelacion','notas'},
        "ventas":{'id_stripe','id_cuenta_de_banco','importe_total','iva'},

    }
    columns=columns.get(table_name,columnas_generales) | columnas_generales
    return columns

def get_ignored_columns_edit(table_name,estatus):
    columnas_generales = {'default':{'fecha_de_creacion', 'id_usuario', 'id_visualizacion', 'fecha_de_actualizacion'}}
    tables = {
        "usuarios":{'default':{'codigo_unico','id_rol','contrasena','contrasena_api','intentos_de_inicio_de_sesion','ultima_sesion','ultimo_cambio_de_contrasena','codigo_unico_expira','estatus'}},
        "archivos":{'default':{'tabla_origen','id_registro','nombre','ruta_s3'}},
        "proyectos":{'default':{'importe_cobrado','fecha_fin','estatus'}},   
        "gastos": {'default':{'importe_pagado','estatus'}},
        "pagos": {'default':{'importe','estatus'}},
        "compras": {'default':{'importe_total','subtotal','descuentos','estatus_de_pago','estatus'}},
        "ajustes_de_inventario": {'default':{'cantidad','tipo_de_ajuste','id_almacen','id_producto','estatus'}},
        "transferencias_de_inventario": {'default':{'id_almacen_salida','id_almacen_entrada','estatus'}},
        "pagos_administrativos":{'default':{'importe','estatus'}},
        "preguntas_de_briefs":{'default':{'id_brief'}},
        "agenda":{'default':{'id_integrante','hora_fin','motivo_de_cancelacion','notas','estatus','id_cliente'}},
        "cuentas_de_banco": {'default':{'balance'}},
        "facturas": {'default':{'importe_total','impuestos','subtotal','importe_cobrado'},'Aprobada':{'id_cliente','id_proyecto','importe_total','impuestos','subtotal','importe_cobrado'}},
        "actividades": {'default':{''},
                        'En proceso':{'id_cliente','notas_cambios','id_proyecto','id_integrante','actividad','id_categoria_de_actividad','fecha_solicitud','fecha_realizado','fecha_cerrado'},                        
                        'Con cambios':{'id_cliente','notas_cambios','prioridad','comentarios','id_proyecto','id_integrante','actividad','id_categoria_de_actividad','fecha_solicitud','fecha_realizado','fecha_cerrado'},
                        'Realizada':{'id_cliente','notas_cierre','prioridad','horas','comentarios','id_proyecto','id_integrante','actividad','id_categoria_de_actividad','fecha_solicitud','fecha_realizado','fecha_cerrado'}},
    }
    table_dict = tables.get(table_name, columnas_generales)
    if not estatus or estatus not in table_dict:
        estatus = 'default'    
    columns = table_dict.get(estatus, set()) | columnas_generales['default']
    if table_name in ('ejemplo'):
        columns=columns-{'estatus'}
    return columns

def get_non_mandatory_columns(table_name):
    columnas_generales = {'descripcion','notas'}
    columns = {
        "roles":{'id_empresa'} ,
        "clientes": {'telefono','correo_electronico','direccion','codigo_postal','persona_contacto','telefono_contacto','correo_electronico_contacto','condiciones_de_pago','rfc','razon_social','sitio_web','condiciones_pago'} ,
        "proveedores": {'telefono','correo_electronico','direccion','codigo_postal','pais','persona_contacto','telefono_contacto','correo_electronico_contacto','condiciones_de_pago','rfc','razon_social','sitio_web','condiciones_pago'} ,
        "gastos": {'folio_fiscal_uuid','fecha_de_comprobante','id_cuenta_de_banco'} ,
        "cuentas_de_banco": {'clabe','numero_de_cuenta','id_integrante'} ,
        "facturas": {'folio_fiscal_uuid','fecha_de_expedicion'} ,
        "actividades": {'comentarios'},
        "integrantes":{'rfc','curp','numero_seguridad_social','direccion','codigo_postal','telefono','correo_electronico','genero','estado_civil','fecha_nacimiento'},
        "briefs": {'id_servicio'},
        "briefs_de_clientes": {'id_proyecto'},
    }
    columns=columns.get(table_name,{''}) | columnas_generales
    return columns

def get_default_variable_values(table_name):
    current_time = datetime.today() - timedelta(hours=6)
    default_values = {
        "proyectos": {"fecha_inicio": current_time.strftime("%Y-%m-%d")},
        "gastos": {"fecha_de_gasto": current_time.strftime("%Y-%m-%d")},
        "ajustes_de_dinero": {"fecha_de_ajuste": current_time.strftime("%Y-%m-%d")},
        "pagos": {"fecha_pago": current_time.strftime("%Y-%m-%d")},
        "transferencias_de_dinero": {'fecha_de_transferencia': current_time.strftime("%Y-%m-%d")},
        "actividades": {"fecha_solicitud": current_time.strftime("%Y-%m-%d")},
        "compras": {"fecha_orden": current_time.strftime("%Y-%m-%d"),"costos_adicionales":0},
        "recepciones_de_compras": {"fecha_entrega": current_time.strftime("%Y-%m-%d")},
        "ajustes_de_inventario": {"fecha_de_ajuste": current_time.strftime("%Y-%m-%d")},
        "transferencias_de_inventario": {"fecha_de_transferencia": current_time.strftime("%Y-%m-%d")},
        "pagos_administrativos": {"fecha_pago": current_time.strftime("%Y-%m-%d")},
        "ventas": {"importe": 0,"tipo_de_iva":"16%","iva":0},
    }
    default_values=default_values.get(table_name,{})
    return default_values

def get_url_after_add(table_name):
    columns = {
        "facturas": "dynamic.double_table_view",
        "pagos_administrativos": "dynamic.double_table_view",
        "compras": "dynamic.double_table_view",
        "recepciones_de_compras": "dynamic.double_table_view",
        "transferencias_de_inventario": "dynamic.double_table_view",
    }
    columns=columns.get(table_name,'dynamic.table_view')
    return columns

def get_non_edit_status(table_name):
    general_status = {'Cancelado','Contestado','Cancelada','Recibida','Facturada','Finalizada','Entregada','Realizada','Realizado','Pagado','Pagado parcial','Aprobada','Aprobado','Recibida parcial','Pagado parcial','En proceso'}
    status_to_remove = {
        "facturas": {'Aprobada'},
        "actividades": {'En proceso','Realizada'},

    }
    status=general_status-status_to_remove.get(table_name,{''})
    return status

def get_no_edit_access():
    tables=['servicios_en_facturas','gastos_en_pagos','facturas_en_ingresos']
    return tables

def get_form_filters(table_name):
    filters={
        "facturas": {'id_proyecto':'id_cliente'},
        "actividades": {'id_proyecto':'id_cliente'},
        "recepciones_de_compras": {'id_compra':'id_almacen'},
    }
    filters=filters.get(table_name,'')
    return filters

def get_parent_record(table_name):
    parent_record={
        "preguntas_de_briefs":'id_brief',
    }
    parent_record=parent_record.get(table_name,'')
    return parent_record
