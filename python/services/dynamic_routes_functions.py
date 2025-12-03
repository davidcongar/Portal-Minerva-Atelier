from python.models.modelos import *
from sqlalchemy import func
from python.services.system.helper_functions import *
from flask import  jsonify
from datetime import timedelta
from python.services.update_record_table_functions import *

def get_joins():
    joins = {
        "id_usuario": (Usuarios, Usuarios.id, Usuarios.nombre),
        "id_rol": (Roles, Roles.id, Roles.nombre),
        "id_categoria_de_reporte":(CategoriasDeReportes, CategoriasDeReportes.id, CategoriasDeReportes.nombre),        
        "id_producto": (Productos, Productos.id, Productos.nombre),
        "id_almacen": (Almacenes, Almacenes.id, Almacenes.nombre),
        "id_compra": (Compras, Compras.id, Compras.id_visualizacion if hasattr(Compras, "id_visualizacion") else Compras.id_visualizacion),
        "id_servicio": (Servicios, Servicios.id, Servicios.nombre),
        "id_cliente": (Clientes, Clientes.id, Clientes.nombre),
        "id_proyecto": (Proyectos, Proyectos.id, Proyectos.id_visualizacion),
        "id_factura": (Facturas, Facturas.id, Facturas.folio_fiscal_uuid),
        "id_cotizacion": (Cotizaciones, Cotizaciones.id, Cotizaciones.descripcion),
        "id_categoria_de_producto": (CategoriasDeProductos, CategoriasDeProductos.id, CategoriasDeProductos.nombre),
        "id_recepcion_de_compra": (RecepcionesDeCompras, RecepcionesDeCompras.id, RecepcionesDeCompras.id_visualizacion),
        "id_almacen_salida": (Almacenes, Almacenes.id, Almacenes.nombre),
        "id_almacen_entrada": (Almacenes, Almacenes.id, Almacenes.nombre),
        "id_transferencia_de_inventario": (TransferenciasDeInventario, TransferenciasDeInventario.id, TransferenciasDeInventario.id_visualizacion),
        "id_envio": (Envios, Envios.id, Envios.id_visualizacion),
        "id_pago": (PagosAdministrativos, PagosAdministrativos.id, PagosAdministrativos.id_visualizacion if hasattr(PagosAdministrativos, "id_visualizacion") else PagosAdministrativos.id),
        "id_gasto": (Gastos, Gastos.id, Gastos.id_visualizacion if hasattr(Gastos, "id_visualizacion") else Gastos.id),
        "id_cuenta_de_banco": (CuentasDeBanco, CuentasDeBanco.id, CuentasDeBanco.nombre),
        "id_cuenta_de_banco_salida": (CuentasDeBanco, CuentasDeBanco.id, CuentasDeBanco.nombre),
        "id_cuenta_de_banco_entrada": (CuentasDeBanco, CuentasDeBanco.id, CuentasDeBanco.nombre),
        "id_brief": (Briefs, Briefs.id, Briefs.nombre),
        "id_integrante": (Integrantes, Integrantes.id, Integrantes.nombre_completo),
        "id_actividad_base": (ActividadesBase, ActividadesBase.id, ActividadesBase.nombre),
        "id_integrante": (Integrantes, Integrantes.id, Integrantes.nombre_completo),
        "id_calidad_de_servicio_de_proyecto": (CalidadDeServicioDeProyectos, CalidadDeServicioDeProyectos.id, CalidadDeServicioDeProyectos.id_visualizacion),
        "id_pregunta_de_calidad_de_servicio": (PreguntasDeCalidadDeServicio, PreguntasDeCalidadDeServicio.id, PreguntasDeCalidadDeServicio.pregunta),
        "id_encuesta_de_satisfaccion_de_proyecto": (EncuestaDeSatisfaccionDeProyectos, EncuestaDeSatisfaccionDeProyectos.id, EncuestaDeSatisfaccionDeProyectos.id_visualizacion),
        "id_pregunta_de_encuesta_de_satisfaccion": (PreguntasDeEncuestaDeSatisfaccion, PreguntasDeEncuestaDeSatisfaccion.id, PreguntasDeEncuestaDeSatisfaccion.pregunta),
        "id_puesto": (Puestos, Puestos.id, Puestos.nombre),
        "id_pago_de_nomina": (PagosDeNomina, PagosDeNomina.id, PagosDeNomina.id_visualizacion),   
        "id_proveedor": (Proveedores, Proveedores.id, Proveedores.id_visualizacion),   
        "id_categoria_de_gasto": (CategoriasDeGastos, CategoriasDeGastos.id, CategoriasDeGastos.id_visualizacion),   



    }
    return joins

def get_foreign_options():
    foreign_options = {
        "id_rol": Roles.query.filter_by(estatus="Activo"),
        "id_categoria_de_reporte":CategoriasDeReportes.query.filter_by(estatus="Activo"),
        "id_integrante":Integrantes.query.filter_by(estatus="Activo"),
        "id_cuenta_de_banco":CuentasDeBanco.query.filter_by(estatus="Activo"),
        "id_integrante":Integrantes.query.filter_by(estatus="Activo"),
        "id_integrante":Integrantes.query.filter_by(estatus="Activo"),
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
        "ejemplo": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    }      
    for i in options:
        multiple_choice_data[i] = {
            "selected": options[i],
            "options": options[i]
        }
    return multiple_choice_data

def get_columns(table_name,section):
    columns={
        "logs_auditoria": {
            "main_page": ["tabla", "id_registro","usuario","accion","datos_anteriores","datos_nuevos","fecha"],
            "modal": ["tabla", "id_registro","usuario","accion","datos_anteriores","datos_nuevos","fecha"],
            "pdf": []
        },
        "rutas": {
            "main_page": ["categoria", "nombre","ruta"],
            "modal": ["id", "categoria","nombre","ruta", "fecha_de_creacion", "fecha_de_actualizacion"],
            "pdf": []
        },
        "roles": {
            "main_page": ["id_visualizacion", "nombre", "estatus"],
            "modal": ["id", "id_visualizacion", "nombre", "estatus", "estatus", "fecha_de_creacion", "fecha_de_actualizacion"],
            "pdf": []
        },
        "usuarios": {
            "main_page": ["id_visualizacion", "nombre", "correo_electronico","intentos_de_inicio_de_sesion","ultima_sesion","ultimo_cambio_de_contrasena", "estatus"],
            "modal": ["id", "id_visualizacion", "nombre", "correo_electronico", "contrasena_api", "estatus", "fecha_de_creacion", "fecha_de_actualizacion"],
            "pdf": []
        },
        "categorias_de_reportes": {
            "main_page": ["id_visualizacion", "nombre", "estatus"],
            "modal": ["id", "id_visualizacion", "nombre", "estatus"],
            "pdf": []
        },
        "reportes": {
            "main_page": ["id_categoria_de_reporte_nombre", "nombre", "descripcion"],
            "modal": ["id", "id_categoria_de_reporte_nombre", "nombre", "descripcion"],
            "pdf": []
        },
        "archivos": {
            "main_page": ["tabla_origen", "nombre"],
            "modal": ["id", "tabla_origen", "nombre", "ruta_s3", "en_servidor", "fecha_de_creacion"],
            "pdf": []
        },
        "gastos": {
            "main_page": ["id_visualizacion","id_categoria_de_gasto_nombre","id_proveedor_nombre","id_cuenta_de_banco_nombre","importe","importe_pagado","fecha_de_gasto","estatus"],
            "modal": ["id","id_visualizacion","id_categoria_de_gasto_nombre","id_proveedor_nombre","id_cuenta_de_banco_nombre","importe","importe_pagado","fecha_de_gasto","folio_fiscal_uuid","fecha_de_comprobante","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_categoria_de_gasto_nombre","id_proveedor_nombre","id_cuenta_de_banco_nombre","importe","importe_pagado","fecha_de_gasto","folio_fiscal_uuid","fecha_de_comprobante","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "gastos_recurrentes": {
            "main_page": ["id_visualizacion","id_categoria_de_gasto_nombre","id_proveedor_nombre","importe","estatus"],
            "modal": ["id","id_categoria_de_gasto","id_proveedor","id_cuenta_de_banco","id_visualizacion","id_categoria_de_gasto_nombre","id_proveedor_nombre","id_cuenta_de_banco_nombre","importe","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_categoria_de_gasto_nombre","id_proveedor_nombre","id_cuenta_de_banco_nombre","importe","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "pagos_administrativos": {
            "main_page": ["id_visualizacion","id_proveedor_nombre","id_cuenta_de_banco_nombre","fecha_pago","importe","estatus"],
            "modal": ["id","id_visualizacion","id_proveedor_nombre","id_cuenta_de_banco_nombre","fecha_pago","importe","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_proveedor_nombre","id_cuenta_de_banco_nombre","fecha_pago","importe","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "gastos_y_compras_en_pagos": {
            "main_page": ["id_pago_id_visualizacion","id_gasto_id_visualizacion","id_compra_id_visualizacion","importe"],
            "modal": ["id","id_pago_id_visualizacion","id_gasto_id_visualizacion","id_compra_id_visualizacion","importe","notas","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_pago_id_visualizacion","id_gasto_id_visualizacion","id_compra_id_visualizacion","importe","notas","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "transferencias_de_dinero": {
            "main_page": ["id_visualizacion","id_cuenta_de_banco_salida_nombre","id_cuenta_de_banco_entrada_nombre","importe","fecha_de_transferencia","estatus"],
            "modal": ["id","id_visualizacion","id_cuenta_de_banco_salida_nombre","id_cuenta_de_banco_entrada_nombre","importe","fecha_de_transferencia","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_cuenta_de_banco_salida_nombre","id_cuenta_de_banco_entrada_nombre","importe","fecha_de_transferencia","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "ajustes_de_dinero": {
            "main_page": ["id_visualizacion","id_cuenta_de_banco_nombre","tipo_de_ajuste","importe","fecha_de_ajuste","estatus"],
            "modal": ["id","id_visualizacion","id_cuenta_de_banco_nombre","tipo_de_ajuste","importe","fecha_de_ajuste","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_cuenta_de_banco_nombre","tipo_de_ajuste","importe","fecha_de_ajuste","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "facturas": {
            "main_page": ["id_visualizacion","id_cliente_nombre","id_venta_id_visualizacion","fecha_de_expedicion","importe_total","importe_cobrado","estatus"],
            "modal": ["id","id_visualizacion","id_cliente_nombre","id_venta_id_visualizacion","uso_de_cfdi","metodo_de_pago","forma_de_pago","folio_fiscal_uuid","fecha_de_expedicion","subtotal","impuestos","importe_total","importe_cobrado","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_cliente_nombre","id_venta_id_visualizacion","uso_de_cfdi","metodo_de_pago","forma_de_pago","folio_fiscal_uuid","fecha_de_expedicion","subtotal","impuestos","importe_total","importe_cobrado","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "proveedores": {
            "main_page": ["id_visualizacion","nombre","telefono","correo_electronico","estatus"],
            "modal": ["id","id_visualizacion","nombre","razon_social","rfc","direccion","codigo_postal","telefono","correo_electronico","persona_contacto","telefono_contacto","correo_electronico_contacto","condiciones_pago","sitio_web","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","nombre","razon_social","rfc","direccion","codigo_postal","telefono","correo_electronico","persona_contacto","telefono_contacto","correo_electronico_contacto","condiciones_pago","sitio_web","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "precios_de_proveedores": {
            "main_page": ["id_visualizacion","id_proveedor_nombre","id_producto_nombre","id_producto_unidad_de_medida","precio_unitario","estatus"],
            "modal": ["id","id_visualizacion","id_proveedor_nombre","id_producto_nombre","id_producto_unidad_de_medida","precio_unitario","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_proveedor_nombre","id_producto_nombre","id_producto_unidad_de_medida","precio_unitario","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "categorias_de_gastos": {
            "main_page": ["id_visualizacion","nombre","estatus"],
            "modal": ["id","id_visualizacion","nombre","descripcion","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","nombre","descripcion","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "categorias_de_productos": {
            "main_page": ["id_visualizacion","nombre","estatus"],
            "modal": ["id","id_visualizacion","nombre","descripcion","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","nombre","descripcion","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "compras": {
            "main_page": ["id_visualizacion","id_almacen_nombre","id_proveedor_nombre","fecha_orden","fecha_entrega_estimada","importe_total","importe_pagado","estatus","estatus_de_pago"],
            "modal": ["id","id_visualizacion","id_almacen_nombre","id_proveedor_nombre","fecha_orden","fecha_entrega_estimada","subtotal","costos_adicionales","descuentos","importe_total","importe_pagado","notas","estatus","estatus_de_pago","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_almacen_nombre","id_proveedor_nombre","fecha_orden","fecha_entrega_estimada","subtotal","costos_adicionales","descuentos","importe_total","importe_pagado","notas","estatus","estatus_de_pago","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "productos_en_compras": {
            "main_page": ["id_compra_id_visualizacion","id_producto_nombre","cantidad_ordenada","cantidad_recibida","precio_unitario","importe_total","estatus"],
            "modal": ["id","id_compra_id_visualizacion","id_producto_nombre","cantidad_ordenada","cantidad_recibida","precio_unitario","subtotal","descuento_porcentaje","importe_total","fecha_entrega_estimada","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_compra_id_visualizacion","id_producto_nombre","cantidad_ordenada","cantidad_recibida","precio_unitario","importe_total","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "servicios": {
            "main_page": ["id_visualizacion","nombre","estatus"],
            "modal": ["id","id_visualizacion","nombre","descripcion","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","nombre","descripcion","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "precios_de_servicios": {
            "main_page": ["id_visualizacion","id_servicio_nombre","precio_unitario","estatus"],
            "modal": ["id","id_visualizacion","id_servicio_nombre","precio_unitario","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_servicio_nombre","precio_unitario","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "cotizaciones": {
            "main_page": ["id_visualizacion","id_cliente_nombre","id_servicio_nombre","fecha_de_cotizacion","importe_total","estatus"],
            "modal": ["id","id_visualizacion","id_cliente_nombre","id_servicio_nombre","fecha_de_cotizacion","descripcion","importe_total","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_cliente_nombre","id_servicio_nombre","fecha_de_cotizacion","descripcion","importe_total","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "detalle_de_cotizaciones": {
            "main_page": ["id_visualizacion","id_cotizacion_id_visualizacion","descripcion","precio_unitario","cantidad"],
            "modal": ["id","id_visualizacion","id_cotizacion_id_visualizacion","descripcion","precio_unitario","cantidad","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_cotizacion_id_visualizacion","descripcion","precio_unitario","cantidad","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "almacenes": {
            "main_page": ["id_visualizacion","nombre","estatus"],
            "modal": ["id","id_visualizacion","nombre","descripcion","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","nombre","descripcion","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "productos": {
            "main_page": ["id_visualizacion","id_categoria_de_producto_nombre","nombre","inventariable","unidad_de_medida","estatus"],
            "modal": ["id","id_visualizacion","id_categoria_de_producto_nombre","nombre","inventariable","unidad_de_medida","descripcion","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_categoria_de_producto_nombre","nombre","inventariable","unidad_de_medida","descripcion","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "inventario": {
            "main_page": ["id_almacen_nombre","id_producto_nombre","cantidad","cantidad_en_transito"],
            "modal": ["id","id_almacen_nombre","id_producto_nombre","cantidad","cantidad_en_transito","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_almacen_nombre","id_producto_nombre","cantidad","cantidad_en_transito","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "recepciones_de_compras": {
            "main_page": ["id_visualizacion","id_almacen_nombre","id_compra_id_visualizacion","fecha_entrega","estatus"],
            "modal": ["id","id_visualizacion","id_almacen_nombre","id_compra_id_visualizacion","fecha_entrega","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_almacen_nombre","id_compra_id_visualizacion","fecha_entrega","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "productos_en_recepciones_de_compras": {
            "main_page": ["id_recepcion_de_compra_id_visualizacion","id_producto_nombre","cantidad"],
            "modal": ["id","id_recepcion_de_compra_id_visualizacion","id_producto_nombre","cantidad","notas","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_recepcion_de_compra_id_visualizacion","id_producto_nombre","cantidad","notas","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "ajustes_de_inventario": {
            "main_page": ["id_visualizacion","id_almacen_nombre","id_producto_nombre","fecha_de_ajuste","tipo_de_ajuste","cantidad","estatus"],
            "modal": ["id","id_visualizacion","id_almacen_nombre","id_producto_nombre","fecha_de_ajuste","tipo_de_ajuste","cantidad","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_almacen_nombre","id_producto_nombre","fecha_de_ajuste","tipo_de_ajuste","cantidad","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "transferencias_de_inventario": {
            "main_page": ["id_visualizacion","id_almacen_salida_nombre","id_almacen_entrada_nombre","fecha_de_transferencia","estatus"],
            "modal": ["id","id_visualizacion","id_almacen_salida_nombre","id_almacen_entrada_nombre","fecha_de_transferencia","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_almacen_salida_nombre","id_almacen_entrada_nombre","fecha_de_transferencia","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "productos_en_transferencias_de_inventario": {
            "main_page": ["id_visualizacion","id_transferencia_de_inventario_visualizacion","id_producto_nombre","cantidad"],
            "modal": ["id","id_visualizacion","id_transferencia_de_inventario_visualizacion","id_producto_nombre","cantidad","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_transferencia_de_inventario_visualizacion","id_producto_nombre","cantidad","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "envios": {
            "main_page": ["id_visualizacion","id_almacen_nombre","id_cliente_nombre","id_proyecto_nombre","id_proveedor_nombre","guia_de_envio","fecha_envio","estatus"],
            "modal": ["id","id_visualizacion","id_almacen_nombre","id_cliente_nombre","id_proyecto_nombre","id_proveedor_nombre","guia_de_envio","fecha_envio","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_almacen_nombre","id_cliente_nombre","id_proyecto_nombre","id_proveedor_nombre","guia_de_envio","fecha_envio","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "productos_en_envios": {
            "main_page": ["id_visualizacion","id_envio_id_visualizacion","id_producto_nombre","cantidad"],
            "modal": ["id","id_visualizacion","id_envio_id_visualizacion","id_producto_nombre","cantidad","notas","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_envio_id_visualizacion","id_producto_nombre","cantidad","notas","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "clientes": {
            "main_page": ["id_visualizacion","nombre","tipo_de_cliente","telefono","correo_electronico","estatus"],
            "modal": ["id","id_visualizacion","tipo_de_cliente","nombre","rfc","direccion","codigo_postal","telefono","correo_electronico","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","tipo_de_cliente","nombre","rfc","direccion","codigo_postal","telefono","correo_electronico","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "briefs": {
            "main_page": ["id_visualizacion","id_servicio_nombre","nombre","estatus"],
            "modal": ["id","id_visualizacion","id_servicio_nombre","nombre","descripcion","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_servicio_nombre","nombre","descripcion","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "preguntas_de_briefs": {
            "main_page": ["id_visualizacion","id_brief_nombre","orden","pregunta","estatus"],
            "modal": ["id","id_visualizacion","id_brief_nombre","orden","pregunta","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_brief_nombre","orden","pregunta","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "agenda": {
            "main_page": ["id_visualizacion","id_cliente_nombre","id_integrante_nombre","fecha","hora_inicio","hora_fin","estatus"],
            "modal": ["id","id_visualizacion","id_cliente_nombre","id_integrante_nombre","fecha","hora_inicio","hora_fin","notas","motivo_de_cancelacion","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_cliente_nombre","id_integrante_nombre","fecha","hora_inicio","hora_fin","notas","motivo_de_cancelacion","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "proyectos": {
            "main_page": ["id_visualizacion","id_venta_id_visualizacion","fecha_inicio","fecha_fin","estatus"],
            "modal": ["id","id_visualizacion","id_venta_id_visualizacion","fecha_inicio","fecha_fin","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_venta_id_visualizacion","fecha_inicio","fecha_fin","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "actividades_base": {
            "main_page": ["id_visualizacion","id_servicio_nombre","nombre","horas_estimadas","estatus"],
            "modal": ["id","id_visualizacion","id_servicio_nombre","nombre","descripcion","entregable","horas_estimadas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_servicio_nombre","nombre","descripcion","entregable","horas_estimadas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "actividades": {
            "main_page": ["id_visualizacion","id_proyecto_nombre","id_integrante_nombre","id_actividad_base_nombre","fecha_inicio","fecha_estimada","fecha_fin","estatus"],
            "modal": ["id","id_visualizacion","id_proyecto_nombre","id_integrante_nombre","id_actividad_base_nombre","fecha_inicio","fecha_estimada","fecha_fin","prioridad","horas","notas","notas_cierre","comentarios_supervisor","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_proyecto_nombre","id_integrante_nombre","id_actividad_base_nombre","fecha_inicio","fecha_estimada","fecha_fin","prioridad","horas","notas","comentarios_supervisor","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "preguntas_de_calidad_de_servicio": {
            "main_page": ["id_visualizacion","id_servicio_nombre","orden","pregunta","tipo_de_respuesta"],
            "modal": ["id","id_visualizacion","id_servicio_nombre","orden","pregunta","tipo_de_respuesta","opciones","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_servicio_nombre","orden","pregunta","tipo_de_respuesta","opciones","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "calidad_de_servicio_de_proyectos": {
            "main_page": ["id_visualizacion","id_cliente_nombre","id_proyecto_nombre","fecha_cierre","estatus"],
            "modal": ["id","id_visualizacion","id_cliente_nombre","id_proyecto_nombre","fecha_cierre","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_cliente_nombre","id_proyecto_nombre","fecha_cierre","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "respuestas_calidad_de_servicio": {
            "main_page": ["id_visualizacion","id_calidad_de_servicio_de_proyecto_id_visualizacion","id_pregunta_de_calidad_de_servicio_visualizacion","respuesta"],
            "modal": ["id","id_visualizacion","id_calidad_de_servicio_de_proyecto_id_visualizacion","id_pregunta_de_calidad_de_servicio_visualizacion","respuesta","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_calidad_de_servicio_de_proyecto_id_visualizacion","id_pregunta_de_calidad_de_servicio_visualizacion","respuesta","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "preguntas_de_encuesta_de_satisfaccion": {
            "main_page": ["id_visualizacion","id_servicio_nombre","orden","pregunta","tipo_de_respuesta"],
            "modal": ["id","id_visualizacion","id_servicio_nombre","orden","pregunta","tipo_de_respuesta","opciones","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_servicio_nombre","orden","pregunta","tipo_de_respuesta","opciones","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "encuesta_de_satisfaccion_de_proyectos": {
            "main_page": ["id_visualizacion","id_cliente_nombre","id_proyecto_nombre","fecha_cierre","estatus"],
            "modal": ["id","id_visualizacion","id_cliente_nombre","id_proyecto_nombre","fecha_cierre","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_cliente_nombre","id_proyecto_nombre","fecha_cierre","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "respuestas_encuesta_de_satisfaccion": {
            "main_page": ["id_visualizacion","id_encuesta_de_satisfaccion_de_proyecto_id_visualizacion","id_pregunta_de_encuesta_de_satisfaccion_visualizacion","respuesta"],
            "modal": ["id","id_visualizacion","id_encuesta_de_satisfaccion_de_proyecto_id_visualizacion","id_pregunta_de_encuesta_de_satisfaccion_visualizacion","respuesta","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_encuesta_de_satisfaccion_de_proyecto_id_visualizacion","id_pregunta_de_encuesta_de_satisfaccion_visualizacion","respuesta","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "puestos": {
            "main_page": ["id_visualizacion","nombre","estatus"],
            "modal": ["id","id_visualizacion","nombre","descripcion","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","nombre","descripcion","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "integrantes": {
            "main_page": ["id_visualizacion","id_puesto_nombre","nombre_completo","telefono","correo_electronico","estatus"],
            "modal": ["id","id_visualizacion","id_puesto_nombre","nombre_completo","fecha_nacimiento","genero","estado_civil","direccion","codigo_postal","telefono","correo_electronico","fecha_contratacion","fecha_terminacion","numero_seguridad_social","rfc","curp","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_puesto_nombre","nombre_completo","fecha_nacimiento","genero","estado_civil","direccion","codigo_postal","telefono","correo_electronico","fecha_contratacion","fecha_terminacion","numero_seguridad_social","rfc","curp","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "pagos_de_nomina": {
            "main_page": ["id_visualizacion","id_cuenta_de_banco_nombre","fecha","importe_total","estatus"],
            "modal": ["id","id_visualizacion","id_cuenta_de_banco_nombre","fecha","importe_total","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_cuenta_de_banco_nombre","fecha","importe_total","notas","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "sueldos_pagados_en_nomina": {
            "main_page": ["id_visualizacion","id_pago_de_nomina_id_visualizacion","id_integrante_nombre","importe","importe_ajuste","importe_total"],
            "modal": ["id","id_visualizacion","id_pago_de_nomina_id_visualizacion","id_integrante_nombre","importe","importe_ajuste","importe_total","notas","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_pago_de_nomina_id_visualizacion","id_integrante_nombre","importe","importe_ajuste","importe_total","notas","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "sueldo_de_integrantes": {
            "main_page": ["id_visualizacion","id_integrante_nombre","sueldo","estatus"],
            "modal": ["id","id_visualizacion","id_integrante_nombre","sueldo","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_integrante_nombre","sueldo","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
       "ventas": {
            "main_page": ["id_visualizacion","id_servicio_nombre","id_cliente_nombre","importe","iva","importe_total","estatus"],
            "modal": ["id","id_visualizacion","id_servicio_nombre","id_cliente_nombre","id_stripe","espacio_de_proyecto","importe","tipo_de_iva","iva","importe_total","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_servicio_nombre","id_cliente_nombre","id_stripe","espacio_de_proyecto","importe","tipo_de_iva","iva","importe_total","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "cuentas_de_banco": {
            "main_page": ["id_visualizacion","id_integrante_nombre","banco","tipo_de_cuenta","nombre","balance","estatus"],
            "modal": ["id","id_visualizacion","id_integrante_nombre","banco","tipo_de_cuenta","nombre","numero_de_cuenta","clabe","balance","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_integrante_nombre","banco","tipo_de_cuenta","nombre","numero_de_cuenta","clabe","balance","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "briefs_de_clientes": {
            "main_page": ["id_visualizacion","id_cliente_nombre","id_proyecto_nombre","fecha_cierre","estatus"],
            "modal": ["id","id_visualizacion","id_cliente_nombre","id_proyecto_nombre","fecha_cierre","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_cliente_nombre","id_proyecto_nombre","fecha_cierre","estatus","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        "respuestas_briefs_de_clientes": {
            "main_page": ["id_visualizacion","id_brief_de_cliente_id_visualizacion","id_pregunta_de_brief_visualizacion","respuesta"],
            "modal": ["id","id_visualizacion","id_brief_de_cliente_id_visualizacion","id_pregunta_de_brief_visualizacion","respuesta","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"],
            "pdf": ["id_visualizacion","id_brief_de_cliente_id_visualizacion","id_pregunta_de_brief_visualizacion","respuesta","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },

    }
    columns=columns.get(table_name).get(section)
    return columns

def get_table_buttons():
    buttons = {
        "reportes":1,
    }
    return buttons

def get_estatus_options(table_name):
    options = {
        'clientes': ["En proceso","Activo","Inactivo","Perdido"],
        'proyectos': ['En revisión','En proceso','Finalizado','Cancelado'],
        'pagos_administrativos': ["En revisión","Aprobado","Pagado"],
        'gastos': ["En revisión","Aprobado","Pagado parcial","Pagado","Cancelado"],
        'transferencias_de_dinero': ["En revisión","Aprobada","Realizada","Cancelada"], 
        'ajustes_de_dinero': ["En revisión","Realizado","Cancelado"],
        'facturas': ["En revisión","Aprobada","Facturada","Cobrada parcial","Cobrada",'Cancelada'],
        'compras': ['En revisión','Aprobada','Recibida parcial','Recibida','Cancelada'],
        'productos_en_compras': ['Pendiente','Recibido','Recibido parcial','Cancelado'],
        'recepciones_de_compras': ['En revisión','Aprobada','Finalizada','Cancelada'],
        'actividades': ["Pendiente","En proceso","Realizada","Con cambios","Cerrada",'Cancelada'],
        'ajustes_de_inventario': ["En revisión","Aprobado","Finalizado","Cancelado"],
        'transferencias_de_inventario': ["En revisión","Aprobada","Finalizada","Cancelado"],
    }
    options=options.get(table_name, ["Activo", "Inactivo"])
    return options

def get_open_status(table_name):
    status={
        "clientes": ['En proceso','Activo'],
        'proyectos': ['En revisión','En proceso'],
        'pagos_administrativos': ["En revisión","Aprobado"],
        'gastos': ["En revisión","Aprobado","Pagado parcial"],
        'transferencias_de_dinero': ["En revisión","Aprobada"], 
        'ajustes_de_dinero': ["En revisión"],
        'compras': ['En revisión','Aprobada','Recibida parcial'],
        'recepciones_de_compras': ['En revisión','Aprobada'],
        'productos_en_compras': ['Pendiente','Recibido','Recibido parcial'],
        'ajustes_de_inventario': ['En revisión','Aprobado'],
        'transferencias_de_inventario': ['En revisión','Aprobada'],
    }
    status=status.get(table_name,['Activo'])
    return status

def get_breadcrumbs(table_name):
    # [modulo,active_menu]
    breadcrumbs={
        "usuarios":['Permisos','permisos'],
        "roles":['Permisos','permisos'],
        "logs_auditoria":['Auditoría','auditoria'],
        "reportes":['Reportes','reportes'],
        "archivos":[session['tabla_origen'].capitalize(),session['tabla_origen']],

        "almacenes":['Almacén','almacen'],
        "categorias_de_productos":['Almacén','almacen'],
        "productos":['Almacén','almacen'],
        "inventario":['Almacén','almacen'],
        "recepciones_de_compras":['Almacén','almacen'],
        "ajustes_de_inventario":['Almacén','almacen'],
        "transferencias_de_inventario":['Almacén','almacen'],
        "envios":['Almacén','almacen'],

        "cuentas_de_banco":['Banca','banca'],
        "pagos_administrativos":['Banca','banca'],
        "transferencias_de_dinero":['Banca','banca'],
        "ajustes_de_dinero":['Banca','banca'],
        "pagos_de_nomina":['Banca','banca'],

        "compras":['Compras','compras'],
        "proveedores":['Compras','compras'],
        "categorias_de_gastos":['Compras','compras'],
        "gastos":['Compras','compras'],
        "gastos_recurrentes":['Compras','compras'],
        "precios_de_proveedores":['Compras','compras'],

        "proyectos":['Proyectos','proyectos'],
        "clientes":['Proyectos','proyectos'],
        "briefs_de_clientes":['Proyectos','proyectos'],
        "briefs":['Proyectos','proyectos'],
        "agenda":['Proyectos','proyectos'],
        "actividades_base":['Proyectos','proyectos'],
        "actividades":['Proyectos','proyectos'],
        "preguntas_de_calidad_de_servicio":['Proyectos','proyectos'],
        "preguntas_de_encuesta_de_satisfaccion":['Proyectos','proyectos'],

        "puestos":['Recursos Humanos','recursos_humanos'],
        "integrantes":['Recursos Humanos','recursos_humanos'],
        "sueldos_de_integrantes":['Recursos Humanos','recursos_humanos'],

        "servicios":['Ventas','ventas'],
        "ventas":['Ventas','ventas'],
        "facturas":['Ventas','ventas'],
        "cotizaciones":['Ventas','ventas'],

    }
    breadcrumbs=breadcrumbs.get(table_name,['Bases de datos','bases_de_datos'])
    return breadcrumbs[0],breadcrumbs[1]

def get_ignored_columns(table_name):
    columnas_generales = {'fecha_de_creacion', 'estatus', 'id_usuario', 'id_visualizacion', 'fecha_de_actualizacion'}
    columns = {
        "usuarios":{'codigo_unico','id_rol','contrasena','contrasena_api','intentos_de_inicio_de_sesion','ultima_sesion','ultimo_cambio_de_contrasena','codigo_unico_expira'},
        "archivos":{'tabla_origen','id_registro','nombre','ruta_s3'},
        "proyectos":{'importe_cobrado','fecha_fin'},
        "gastos": {'importe_pagado'},
        "compras": {'importe_total','subtotal','descuentos','estatus_de_pago'},
        "pagos": {'importe'},  
        "cuentas_de_banco": {'balance'},
        "facturas": {'importe_total','impuestos','subtotal','importe_cobrado'},
        "integrantes": {'fecha_terminacion'},
        "actividades": {'notas_cierre','notas_cambios','fecha_realizado','fecha_cerrado','horas'},
        "pagos_administrativos":{'importe'}
    }
    columns=columns.get(table_name,columnas_generales) | columnas_generales
    return columns

def get_ignored_columns_edit(table_name,estatus):
    columnas_generales = {'default':{'fecha_de_creacion', 'id_usuario', 'id_visualizacion', 'fecha_de_actualizacion','estatus'}}
    tables = {
        "usuarios":{'default':{'codigo_unico','id_rol','contrasena','contrasena_api','intentos_de_inicio_de_sesion','ultima_sesion','ultimo_cambio_de_contrasena','codigo_unico_expira'}},
        "archivos":{'default':{'tabla_origen','id_registro','nombre','ruta_s3'}},
        "proyectos":{'default':{'importe_cobrado','fecha_fin'}},   
        "gastos": {'default':{'importe_pagado'}},
        "pagos": {'default':{'importe'}},
        "compras": {'default':{'importe_total','subtotal','descuentos','estatus_de_pago'}},
        "ajustes_de_inventario": {'default':{'cantidad','tipo_de_ajuste','id_almacen','id_producto'}},
        "transferencias_de_inventario": {'default':{'id_almacen_salida','id_almacen_entrada'}},
        "pagos_administrativos":{'default':{'importe'}},
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
        "integrantes":{'rfc','curp','numero_seguridad_social'},
    }
    columns=columns.get(table_name,{''}) | columnas_generales
    return columns

def get_table_relationships(table_name):
    relationships={
        "roles":["usuarios"],
        "briefs":["preguntas_de_briefs"],
        "pagos_administrativos":["gastos_y_compras_en_pagos"],
        "compras":["productos_en_compras"],
        "recepciones_de_compras":["productos_en_recepciones_de_compras"],

    }
    relationships=relationships.get(table_name,'')
    return relationships

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

def get_calendar_date_variable(table_name):
    date_variable={
        "interacciones":"fecha_hora",
    }
    date_variable=date_variable.get(table_name,'')
    return date_variable

def get_variable_tabs(table_name):
    tabs = {
        "ejemplo": "estatus"
    }
    tabs=tabs.get(table_name,'estatus')
    return tabs

def get_data_tabs(table_name,parent_table,id_parent_record):
    column_tabs=get_variable_tabs(table_name)
    tabs=get_estatus_options(table_name)
    model = get_model_by_name(table_name)
    column = getattr(model, column_tabs, None)
    count_col = func.count().label("count")
    query = db.session.query(column, count_col).group_by(column)
    if parent_table and id_parent_record:
        for rel in model.__mapper__.relationships.values():
            related_table_name = rel.mapper.class_.__tablename__
            if related_table_name == parent_table:
                fk_column = list(rel.local_columns)[0]
                query = query.filter(fk_column == id_parent_record)
                break
    query = query.order_by(count_col.desc())
    results = dict(query.all())
    results = [
        {
            'tab': estatus if estatus else 'Sin estatus',
            'count': results.get(estatus, 0) if estatus in get_open_status(table_name) else ''
        }
        for estatus in tabs
    ]
    return results

def get_date_fields():
    date_fields=["fecha_venta", "fecha_orden", "fecha_de_gasto", "fecha_de_transferencia","fecha","fecha_hora"]
    return date_fields

def get_non_edit_status(table_name):
    general_status = {'Cancelado','Cancelada','Recibida','Facturada','Finalizada','Entregada','Realizada','Realizado','Pagado','Pagado parcial','Aprobada','Aprobado','Recibida parcial','Pagado parcial','En proceso'}
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
