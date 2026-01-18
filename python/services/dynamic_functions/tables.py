from python.models.modelos import *
from sqlalchemy import func
from python.services.system.helper_functions import *
from flask import  jsonify
from datetime import timedelta
from python.services.dynamic_functions.double_tables import *
from python.services.dynamic_functions.input_tables import *

def get_joins():
    joins = {
        'id_usuario': (Usuarios, Usuarios.id, Usuarios.nombre),
        'id_rol': (Roles, Roles.id, Roles.nombre),
        'id_categoria_de_reporte':(CategoriasDeReportes, CategoriasDeReportes.id, CategoriasDeReportes.nombre),        
        'id_producto': (Productos, Productos.id, Productos.nombre),
        'id_almacen': (Almacenes, Almacenes.id, Almacenes.nombre),
        'id_compra': (Compras, Compras.id, Compras.id_visualizacion if hasattr(Compras, 'id_visualizacion') else Compras.id_visualizacion),
        'id_servicio': (Servicios, Servicios.id, Servicios.nombre),
        'id_cliente': (Clientes, Clientes.id, Clientes.nombre_completo),
        'id_proyecto': (Proyectos, Proyectos.id, Proyectos.id_visualizacion),
        'id_factura': (Facturas, Facturas.id, Facturas.folio_fiscal_uuid),
        'id_cotizacion': (Cotizaciones, Cotizaciones.id, Cotizaciones.descripcion),
        'id_categoria_de_producto': (CategoriasDeProductos, CategoriasDeProductos.id, CategoriasDeProductos.nombre),
        'id_recepcion_de_compra': (RecepcionesDeCompras, RecepcionesDeCompras.id, RecepcionesDeCompras.id_visualizacion),
        'id_almacen_salida': (Almacenes, Almacenes.id, Almacenes.nombre),
        'id_almacen_entrada': (Almacenes, Almacenes.id, Almacenes.nombre),
        'id_transferencia_de_inventario': (TransferenciasDeInventario, TransferenciasDeInventario.id, TransferenciasDeInventario.id_visualizacion),
        'id_envio': (Envios, Envios.id, Envios.id_visualizacion),
        'id_pago': (PagosAdministrativos, PagosAdministrativos.id, PagosAdministrativos.id_visualizacion if hasattr(PagosAdministrativos, 'id_visualizacion') else PagosAdministrativos.id),
        'id_gasto': (Gastos, Gastos.id, Gastos.id_visualizacion if hasattr(Gastos, 'id_visualizacion') else Gastos.id),
        'id_cuenta_de_banco': (CuentasDeBanco, CuentasDeBanco.id, CuentasDeBanco.nombre),
        'id_cuenta_de_banco_salida': (CuentasDeBanco, CuentasDeBanco.id, CuentasDeBanco.nombre),
        'id_cuenta_de_banco_entrada': (CuentasDeBanco, CuentasDeBanco.id, CuentasDeBanco.nombre),
        'id_brief': (Briefs, Briefs.id, Briefs.nombre),
        'id_pregunta_de_brief': (PreguntasDeBriefs, PreguntasDeBriefs.id, PreguntasDeBriefs.pregunta),
        'id_integrante': (Integrantes, Integrantes.id, Integrantes.nombre_completo),
        'id_actividad_base': (ActividadesBase, ActividadesBase.id, ActividadesBase.nombre),
        'id_integrante': (Integrantes, Integrantes.id, Integrantes.nombre_completo),
        'id_calidad_de_servicio_de_proyecto': (CalidadDeServicioDeProyectos, CalidadDeServicioDeProyectos.id, CalidadDeServicioDeProyectos.id_visualizacion),
        'id_pregunta_de_calidad_de_servicio': (PreguntasDeCalidadDeServicio, PreguntasDeCalidadDeServicio.id, PreguntasDeCalidadDeServicio.pregunta),
        'id_encuesta_de_satisfaccion_de_proyecto': (EncuestaDeSatisfaccionDeProyectos, EncuestaDeSatisfaccionDeProyectos.id, EncuestaDeSatisfaccionDeProyectos.id_visualizacion),
        'id_pregunta_de_encuesta_de_satisfaccion': (PreguntasDeEncuestaDeSatisfaccion, PreguntasDeEncuestaDeSatisfaccion.id, PreguntasDeEncuestaDeSatisfaccion.pregunta),
        'id_puesto': (Puestos, Puestos.id, Puestos.nombre),
        'id_pago_de_nomina': (PagosDeNomina, PagosDeNomina.id, PagosDeNomina.id_visualizacion),   
        'id_proveedor': (Proveedores, Proveedores.id, Proveedores.nombre),   
        'id_categoria_de_gasto': (CategoriasDeGastos, CategoriasDeGastos.id, CategoriasDeGastos.nombre),   
        'id_espacio_de_proyecto': (EspaciosDeProyectos, EspaciosDeProyectos.id, EspaciosDeProyectos.nombre),   
        'id_venta': (Ventas, Ventas.id, Ventas.id_visualizacion),

    }
    return joins

def get_columns(table_name,section):
    columns={
        'logs_auditoria': {
            'main_page': ['tabla', 'id_registro','usuario','accion','datos_anteriores','datos_nuevos','fecha'],
            'modal': {'informacion_general':['tabla','id_registro','usuario','accion','fecha'],'detalles':['datos_anteriores','datos_nuevos']},
            'pdf': []
        },
        'rutas': {
            'main_page': ['categoria', 'nombre','ruta'],
            'modal': {'informacion_general':['id','categoria','nombre','ruta'],'sistema':['fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': []
        },
        'roles': {
            'main_page': ['id_visualizacion', 'nombre', 'estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','nombre','estatus'],'sistema':['fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': []
        },
        'usuarios': {
            'main_page': ['id_visualizacion', 'nombre', 'correo_electronico','intentos_de_inicio_de_sesion','ultima_sesion','ultimo_cambio_de_contrasena', 'estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','nombre','correo_electronico','estatus'],'seguridad':['contrasena_api'],'sistema':['fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': []
        },
        'categorias_de_reportes': {
            'main_page': ['id_visualizacion', 'nombre', 'estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','nombre','estatus'],'sistema':['fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': []
        },
        'reportes': {
            'main_page': ['id_visualizacion', 'id_categoria_de_reporte_nombre', 'nombre', 'descripcion'],
            'modal': {'informacion_general':['id','id_visualizacion','id_categoria_de_reporte_nombre','nombre','descripcion'],'detalles':['ruta_sql'],'sistema':['fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': []
        },
        'archivos': {
            'main_page': ['nombre','nombre_del_archivo'],
            'modal': {'informacion_general':['id','tabla_origen','nombre'],'detalles':['nombre_del_archivo','ruta_s3'],'sistema':['fecha_de_creacion']},
            'pdf': []
        },
        'gastos': {
            'main_page': ['id_visualizacion','id_categoria_de_gasto_nombre','id_proveedor_nombre','id_cuenta_de_banco_nombre','importe','importe_pagado','fecha_de_gasto','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_categoria_de_gasto_nombre','id_proveedor_nombre','id_cuenta_de_banco_nombre','fecha_de_gasto','folio_fiscal_uuid','fecha_de_comprobante','estatus'],'financiero':['importe','importe_pagado'],'detalles':['notas'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_categoria_de_gasto_nombre','id_proveedor_nombre','id_cuenta_de_banco_nombre','importe','importe_pagado','fecha_de_gasto','folio_fiscal_uuid','fecha_de_comprobante','notas','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'gastos_recurrentes': {
            'main_page': ['id_visualizacion','id_categoria_de_gasto_nombre','id_proveedor_nombre','importe','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_categoria_de_gasto','id_categoria_de_gasto_nombre','id_proveedor','id_proveedor_nombre','id_cuenta_de_banco','id_cuenta_de_banco_nombre','estatus'],'financiero':['importe'],'detalles':['notas'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_categoria_de_gasto_nombre','id_proveedor_nombre','id_cuenta_de_banco_nombre','importe','notas','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'pagos_administrativos': {
            'main_page': ['id_visualizacion','id_proveedor_nombre','id_cuenta_de_banco_nombre','fecha_pago','importe','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_proveedor_nombre','id_cuenta_de_banco_nombre','fecha_pago','estatus'],'financiero':['importe'],'detalles':['notas'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_proveedor_nombre','id_cuenta_de_banco_nombre','fecha_pago','importe','notas','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'gastos_y_compras_en_pagos': {
            'main_page': ['id_pago_id_visualizacion','id_gasto_id_visualizacion','id_compra_id_visualizacion','importe'],
            'modal': {'informacion_general':['id','id_pago_id_visualizacion','id_gasto_id_visualizacion','id_compra_id_visualizacion'],'financiero':['importe'],'detalles':['notas'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_pago_id_visualizacion','id_gasto_id_visualizacion','id_compra_id_visualizacion','importe','notas','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'transferencias_de_dinero': {
            'main_page': ['id_visualizacion','id_cuenta_de_banco_salida_nombre','id_cuenta_de_banco_entrada_nombre','importe','fecha_de_transferencia','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_cuenta_de_banco_salida_nombre','id_cuenta_de_banco_entrada_nombre','fecha_de_transferencia','estatus'],'financiero':['importe'],'detalles':['notas'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_cuenta_de_banco_salida_nombre','id_cuenta_de_banco_entrada_nombre','importe','fecha_de_transferencia','notas','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'ajustes_de_dinero': {
            'main_page': ['id_visualizacion','id_cuenta_de_banco_nombre','tipo_de_ajuste','importe','fecha_de_ajuste','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_cuenta_de_banco_nombre','tipo_de_ajuste','fecha_de_ajuste','estatus'],'financiero':['importe'],'detalles':['notas'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_cuenta_de_banco_nombre','tipo_de_ajuste','importe','fecha_de_ajuste','notas','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'facturas': {
            'main_page': ['id_visualizacion','id_cliente_nombre','id_venta_id_visualizacion','fecha_de_expedicion','importe_total','importe_cobrado','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_cliente_nombre','id_venta_id_visualizacion','uso_de_cfdi','metodo_de_pago','forma_de_pago','folio_fiscal_uuid','fecha_de_expedicion','estatus'],'financiero':['subtotal','impuestos','importe_total','importe_cobrado'],'detalles':['notas'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_cliente_nombre','id_venta_id_visualizacion','uso_de_cfdi','metodo_de_pago','forma_de_pago','folio_fiscal_uuid','fecha_de_expedicion','subtotal','impuestos','importe_total','importe_cobrado','notas','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'proveedores': {
            'main_page': ['id_visualizacion','nombre','telefono','correo_electronico','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','nombre','razon_social','rfc','direccion','codigo_postal','estatus','condiciones_pago'],'contacto':['telefono','correo_electronico','persona_contacto','telefono_contacto','correo_electronico_contacto','sitio_web'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','nombre','razon_social','rfc','direccion','codigo_postal','telefono','correo_electronico','persona_contacto','telefono_contacto','correo_electronico_contacto','condiciones_pago','sitio_web','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'precios_de_proveedores': {
            'main_page': ['id_visualizacion','id_proveedor_nombre','id_producto_nombre','id_producto_unidad_de_medida','precio_unitario','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_proveedor_nombre','id_producto_nombre','id_producto_unidad_de_medida','estatus'],'financiero':['precio_unitario'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_proveedor_nombre','id_producto_nombre','id_producto_unidad_de_medida','precio_unitario','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'categorias_de_gastos': {
            'main_page': ['id_visualizacion','nombre','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','nombre','descripcion','estatus'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','nombre','descripcion','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'categorias_de_productos': {
            'main_page': ['id_visualizacion','nombre','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','nombre','descripcion','estatus'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','nombre','descripcion','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'compras': {
            'main_page': ['id_visualizacion','id_almacen_nombre','id_proveedor_nombre','fecha_orden','fecha_entrega_estimada','importe_total','importe_pagado','estatus','estatus_de_pago'],
            'modal': {'informacion_general':['id','id_visualizacion','id_almacen_nombre','id_proveedor_nombre','fecha_orden','fecha_entrega_estimada','estatus','estatus_de_pago'],'financiero':['subtotal','costos_adicionales','descuentos','importe_total','importe_pagado'],'detalles':['notas'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_almacen_nombre','id_proveedor_nombre','fecha_orden','fecha_entrega_estimada','subtotal','costos_adicionales','descuentos','importe_total','importe_pagado','notas','estatus','estatus_de_pago','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'productos_en_compras': {
            'main_page': ['id_compra_id_visualizacion','id_producto_nombre','cantidad_ordenada','cantidad_recibida','precio_unitario','importe_total','estatus'],
            'modal': {'informacion_general':['id','id_compra_id_visualizacion','id_producto_nombre','cantidad_ordenada','cantidad_recibida','fecha_entrega_estimada','estatus'],'financiero':['precio_unitario','subtotal','descuento_porcentaje','importe_total'],'detalles':['notas'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_compra_id_visualizacion','id_producto_nombre','cantidad_ordenada','cantidad_recibida','precio_unitario','importe_total','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'espacios_de_proyectos': {
            'main_page': ['id_visualizacion','nombre','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','nombre','descripcion','estatus'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','nombre','descripcion','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },        
        'servicios': {
            'main_page': ['id_visualizacion','nombre','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','nombre','descripcion','estatus'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','nombre','descripcion','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'precios_de_servicios': {
            'main_page': ['id_visualizacion','id_servicio_nombre','id_espacio_de_proyecto_nombre','metros_cuadrados_minimos','metros_cuadrados_maximos','precio_unitario','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_servicio_nombre','id_espacio_de_proyecto_nombre','metros_cuadrados_minimos','metros_cuadrados_maximos','estatus'],'financiero':['precio_unitario'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_servicio_nombre','precio_unitario','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'cotizaciones': {
            'main_page': ['id_visualizacion','id_cliente_nombre','id_servicio_nombre','fecha_de_cotizacion','importe_total','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_cliente_nombre','id_servicio_nombre','fecha_de_cotizacion','estatus'],'financiero':['importe_total'],'detalles':['descripcion'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_cliente_nombre','id_servicio_nombre','fecha_de_cotizacion','descripcion','importe_total','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'detalle_de_cotizaciones': {
            'main_page': ['id_visualizacion','id_cotizacion_id_visualizacion','descripcion','precio_unitario','cantidad'],
            'modal': {'informacion_general':['id','id_visualizacion','id_cotizacion_id_visualizacion','descripcion','cantidad'],'financiero':['precio_unitario'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_cotizacion_id_visualizacion','descripcion','precio_unitario','cantidad','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'almacenes': {
            'main_page': ['id_visualizacion','nombre','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','nombre','descripcion','estatus'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','nombre','descripcion','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'productos': {
            'main_page': ['id_visualizacion','id_categoria_de_producto_nombre','nombre','inventariable','unidad_de_medida','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_categoria_de_producto_nombre','nombre','inventariable','unidad_de_medida','descripcion','estatus'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_categoria_de_producto_nombre','nombre','inventariable','unidad_de_medida','descripcion','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'inventario': {
            'main_page': ['id_almacen_nombre','id_producto_nombre','cantidad','cantidad_en_transito'],
            'modal': {'informacion_general':['id','id_almacen_nombre','id_producto_nombre','cantidad','cantidad_en_transito'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_almacen_nombre','id_producto_nombre','cantidad','cantidad_en_transito','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'recepciones_de_compras': {
            'main_page': ['id_visualizacion','id_almacen_nombre','id_compra_id_visualizacion','fecha_entrega','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_almacen_nombre','id_compra_id_visualizacion','fecha_entrega','estatus'],'detalles':['notas'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_almacen_nombre','id_compra_id_visualizacion','fecha_entrega','notas','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'productos_en_recepciones_de_compras': {
            'main_page': ['id_recepcion_de_compra_id_visualizacion','id_producto_nombre','cantidad'],
            'modal': {'informacion_general':['id','id_recepcion_de_compra_id_visualizacion','id_producto_nombre','cantidad'],'detalles':['notas'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_recepcion_de_compra_id_visualizacion','id_producto_nombre','cantidad','notas','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'ajustes_de_inventario': {
            'main_page': ['id_visualizacion','id_almacen_nombre','id_producto_nombre','fecha_de_ajuste','tipo_de_ajuste','cantidad','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_almacen_nombre','id_producto_nombre','fecha_de_ajuste','tipo_de_ajuste','cantidad','estatus'],'detalles':['notas'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_almacen_nombre','id_producto_nombre','fecha_de_ajuste','tipo_de_ajuste','cantidad','notas','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'transferencias_de_inventario': {
            'main_page': ['id_visualizacion','id_almacen_salida_nombre','id_almacen_entrada_nombre','fecha_de_transferencia','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_almacen_salida_nombre','id_almacen_entrada_nombre','fecha_de_transferencia','estatus'],'detalles':['notas'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_almacen_salida_nombre','id_almacen_entrada_nombre','fecha_de_transferencia','notas','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'productos_en_transferencias_de_inventario': {
            'main_page': ['id_visualizacion','id_transferencia_de_inventario_visualizacion','id_producto_nombre','cantidad'],
            'modal': {'informacion_general':['id','id_visualizacion','id_transferencia_de_inventario_visualizacion','id_producto_nombre','cantidad'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_transferencia_de_inventario_visualizacion','id_producto_nombre','cantidad','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'envios': {
            'main_page': ['id_visualizacion','id_almacen_nombre','id_cliente_nombre','id_proyecto_nombre','id_proveedor_nombre','guia_de_envio','fecha_envio','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_almacen_nombre','id_cliente_nombre','id_proyecto_nombre','id_proveedor_nombre','guia_de_envio','fecha_envio','estatus'],'detalles':['notas'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_almacen_nombre','id_cliente_nombre','id_proyecto_nombre','id_proveedor_nombre','guia_de_envio','fecha_envio','notas','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'productos_en_envios': {
            'main_page': ['id_visualizacion','id_envio_id_visualizacion','id_producto_nombre','cantidad'],
            'modal': {'informacion_general':['id','id_visualizacion','id_envio_id_visualizacion','id_producto_nombre','cantidad'],'detalles':['notas'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_envio_id_visualizacion','id_producto_nombre','cantidad','notas','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'clientes': {
            'main_page': ['id_visualizacion','nombre_completo','telefono','correo_electronico','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','nombre_completo','rfc','direccion','codigo_postal','estatus'],'contacto':['telefono','correo_electronico'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','nombre_completo','rfc','direccion','codigo_postal','telefono','correo_electronico','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'briefs': {
            'main_page': ['id_visualizacion','id_servicio_nombre','nombre','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_servicio_nombre','nombre','descripcion','estatus'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_servicio_nombre','nombre','descripcion','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'preguntas_de_briefs': {
            'main_page': ['id_visualizacion','id_brief_nombre','orden','pregunta','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_brief_nombre','orden','pregunta','estatus'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_brief_nombre','orden','pregunta','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'respuestas_de_preguntas_de_briefs': {
            'main_page': ['id_visualizacion','id_pregunta_de_brief_pregunta','respuesta','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_pregunta_de_brief','respuesta','estatus'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_pregunta_de_brief','respuesta','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },        
        'agenda': {
            'main_page': ['id_visualizacion','id_cliente_nombre_completo','id_integrante_nombre_completo','fecha','hora_inicio','hora_fin','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_cliente_nombre_completo','id_integrante_nombre_completo','fecha','hora_inicio','hora_fin','estatus'],'detalles':['notas','motivo_de_cancelacion'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_cliente_nombre_completo','id_integrante_nombre_completo','fecha','hora_inicio','hora_fin','notas','motivo_de_cancelacion','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'proyectos': {
            'main_page': ['id_visualizacion','id_venta_id_visualizacion','id_servicio_nombre','id_espacio_de_proyecto_nombre','id_integrante_nombre_completo','metros_cuadrados','fecha_inicio','fecha_fin','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_venta_id_visualizacion','id_servicio_nombre','id_espacio_de_proyecto_nombre','id_integrante_nombre_completo','metros_cuadrados','fecha_inicio','fecha_fin','estatus'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_venta_id_visualizacion','id_servicio_nombre','id_espacio_de_proyecto_nombre','id_integrante_nombre_completo','metros_cuadrados','fecha_inicio','fecha_fin','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'actividades_base': {
            'main_page': ['id_visualizacion','id_servicio_nombre','nombre','horas_estimadas','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_servicio_nombre','nombre','entregable','horas_estimadas','estatus'],'detalles':['descripcion'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_servicio_nombre','nombre','descripcion','entregable','horas_estimadas','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'actividades': {
            'main_page': ['id_visualizacion','id_proyecto_nombre','id_integrante_nombre_completo','id_actividad_base_nombre','fecha_inicio','fecha_estimada','fecha_fin','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_proyecto_nombre','id_integrante_nombre_completo','id_actividad_base_nombre','fecha_inicio','fecha_estimada','fecha_fin','prioridad','horas','estatus'],'detalles':['notas','notas_cierre','comentarios_supervisor'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_proyecto_nombre','id_integrante_nombre_completo','id_actividad_base_nombre','fecha_inicio','fecha_estimada','fecha_fin','prioridad','horas','notas','comentarios_supervisor','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'preguntas_de_calidad_de_servicio': {
            'main_page': ['id_visualizacion','id_servicio_nombre','orden','pregunta','tipo_de_respuesta'],
            'modal': {'informacion_general':['id','id_visualizacion','id_servicio_nombre','orden','pregunta','tipo_de_respuesta','estatus'],'detalles':['opciones'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_servicio_nombre','orden','pregunta','tipo_de_respuesta','opciones','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'calidad_de_servicio_de_proyectos': {
            'main_page': ['id_visualizacion','id_cliente_nombre','id_proyecto_nombre','fecha_cierre','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_cliente_nombre','id_proyecto_nombre','fecha_cierre','estatus'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_cliente_nombre','id_proyecto_nombre','fecha_cierre','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'respuestas_calidad_de_servicio': {
            'main_page': ['id_visualizacion','id_calidad_de_servicio_de_proyecto_id_visualizacion','id_pregunta_de_calidad_de_servicio_visualizacion','respuesta'],
            'modal': {'informacion_general':['id','id_visualizacion','id_calidad_de_servicio_de_proyecto_id_visualizacion','id_pregunta_de_calidad_de_servicio_visualizacion','respuesta'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_calidad_de_servicio_de_proyecto_id_visualizacion','id_pregunta_de_calidad_de_servicio_visualizacion','respuesta','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'preguntas_de_encuesta_de_satisfaccion': {
            'main_page': ['id_visualizacion','id_servicio_nombre','orden','pregunta','tipo_de_respuesta'],
            'modal': {'informacion_general':['id','id_visualizacion','id_servicio_nombre','orden','pregunta','tipo_de_respuesta','estatus'],'detalles':['opciones'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_servicio_nombre','orden','pregunta','tipo_de_respuesta','opciones','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'encuesta_de_satisfaccion_de_proyectos': {
            'main_page': ['id_visualizacion','id_cliente_nombre','id_proyecto_nombre','fecha_cierre','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_cliente_nombre','id_proyecto_nombre','fecha_cierre','estatus'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_cliente_nombre','id_proyecto_nombre','fecha_cierre','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'respuestas_encuesta_de_satisfaccion': {
            'main_page': ['id_visualizacion','id_encuesta_de_satisfaccion_de_proyecto_id_visualizacion','id_pregunta_de_encuesta_de_satisfaccion_visualizacion','respuesta'],
            'modal': {'informacion_general':['id','id_visualizacion','id_encuesta_de_satisfaccion_de_proyecto_id_visualizacion','id_pregunta_de_encuesta_de_satisfaccion_visualizacion','respuesta'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_encuesta_de_satisfaccion_de_proyecto_id_visualizacion','id_pregunta_de_encuesta_de_satisfaccion_visualizacion','respuesta','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'puestos': {
            'main_page': ['id_visualizacion','nombre','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','nombre','descripcion','estatus'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','nombre','descripcion','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'integrantes': {
            'main_page': ['id_visualizacion','id_puesto_nombre','nombre_completo','telefono','correo_electronico','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_puesto_nombre','nombre_completo','fecha_nacimiento','genero','estado_civil','fecha_contratacion','fecha_terminacion','estatus'],'contacto':['direccion','codigo_postal','telefono','correo_electronico'],'documentos':['numero_seguridad_social','rfc','curp'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_puesto_nombre','nombre_completo','fecha_nacimiento','genero','estado_civil','direccion','codigo_postal','telefono','correo_electronico','fecha_contratacion','fecha_terminacion','numero_seguridad_social','rfc','curp','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'pagos_de_nomina': {
            'main_page': ['id_visualizacion','id_cuenta_de_banco_nombre','fecha','importe_total','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_cuenta_de_banco_nombre','fecha','estatus'],'financiero':['importe_total'],'detalles':['notas'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_cuenta_de_banco_nombre','fecha','importe_total','notas','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'sueldos_pagados_en_nomina': {
            'main_page': ['id_visualizacion','id_pago_de_nomina_id_visualizacion','id_integrante_nombre','importe','importe_ajuste','importe_total'],
            'modal': {'informacion_general':['id','id_visualizacion','id_pago_de_nomina_id_visualizacion','id_integrante_nombre'],'financiero':['importe','importe_ajuste','importe_total'],'detalles':['notas'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_pago_de_nomina_id_visualizacion','id_integrante_nombre','importe','importe_ajuste','importe_total','notas','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'sueldo_de_integrantes': {
            'main_page': ['id_visualizacion','id_integrante_nombre','sueldo','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_integrante_nombre','estatus'],'financiero':['sueldo'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_integrante_nombre','sueldo','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'ventas': {
            'main_page': ['id_visualizacion','id_cliente_nombre_completo','importe','iva','importe_total','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_cliente_nombre_completo','espacio_de_proyecto','tipo_de_iva','estatus'],'financiero':['importe','iva','importe_total'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_cliente_nombre_completo','espacio_de_proyecto','importe','tipo_de_iva','iva','importe_total','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        "servicios_en_ventas": {
            "main_page": ["id_visualizacion","id_venta_id_visualizacion","id_servicio_nombre","id_espacio_de_proyecto_nombre","metros_cuadrados","cantidad","precio_unitario","importe"],
            "modal": {"informacion_general":["id","id_visualizacion","id_venta_id_visualizacion","id_servicio_nombre","id_espacio_de_proyecto_nombre"],"detalles":["metros_cuadrados","cantidad","precio_unitario","importe"],"sistema":["id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]},
            "pdf": ["id_visualizacion","id_venta_id_visualizacion","id_servicio_nombre","id_espacio_de_proyecto_nombre","metros_cuadrados","cantidad","precio_unitario","importe","id_usuario_correo_electronico","fecha_de_creacion","fecha_de_actualizacion"]
        },
        'cuentas_de_banco': {
            'main_page': ['id_visualizacion','id_integrante_nombre','banco','tipo_de_cuenta','nombre','balance','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_integrante_nombre','banco','tipo_de_cuenta','nombre','estatus'],'financiero':['balance'],'detalles':['numero_de_cuenta','clabe'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_integrante_nombre','banco','tipo_de_cuenta','nombre','numero_de_cuenta','clabe','balance','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'briefs_de_clientes': {
            'main_page': ['id_visualizacion','id_cliente_nombre_completo','id_proyecto_nombre','id_brief_nombre','fecha_cierre','estatus'],
            'modal': {'informacion_general':['id','id_visualizacion','id_cliente_nombre_completo','id_proyecto_nombre','fecha_cierre','estatus'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_cliente_nombre_completo','id_proyecto_nombre','fecha_cierre','estatus','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        },
        'respuestas_briefs_de_clientes': {
            'main_page': ['id_visualizacion','id_brief_de_cliente_id_visualizacion','id_pregunta_de_brief_visualizacion','respuesta'],
            'modal': {'informacion_general':['id','id_visualizacion','id_brief_de_cliente_id_visualizacion','id_pregunta_de_brief_visualizacion','respuesta'],'sistema':['id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']},
            'pdf': ['id_visualizacion','id_brief_de_cliente_id_visualizacion','id_pregunta_de_brief_visualizacion','respuesta','id_usuario_correo_electronico','fecha_de_creacion','fecha_de_actualizacion']
        }
    }
    columns=columns.get(table_name).get(section)
    return columns

def get_table_buttons():
    buttons = {
        'reportes':1,
    }
    return buttons

def get_estatus_options(table_name):
    options = {
        'clientes': ['En proceso','Perfect match','Swipe','Activo','Inactivo','Perdido'],
        'proyectos': ['En revisión','En proceso','Finalizado','Cancelado'],
        'pagos_administrativos': ['En revisión','Aprobado','Pagado'],
        'gastos': ['En revisión','Aprobado','Pagado parcial','Pagado','Cancelado'],
        'transferencias_de_dinero': ['En revisión','Aprobada','Realizada','Cancelada'], 
        'ajustes_de_dinero': ['En revisión','Realizado','Cancelado'],
        'facturas': ['En revisión','Aprobada','Facturada','Cobrada parcial','Cobrada','Cancelada'],
        'compras': ['En revisión','Aprobada','Recibida parcial','Recibida','Cancelada'],
        'productos_en_compras': ['Pendiente','Recibido','Recibido parcial','Cancelado'],
        'recepciones_de_compras': ['En revisión','Aprobada','Finalizada','Cancelada'],
        'actividades': ['Pendiente','En proceso','Realizada','Con cambios','Cerrada','Cancelada'],
        'ajustes_de_inventario': ['En revisión','Aprobado','Finalizado','Cancelado'],
        'transferencias_de_inventario': ['En revisión','Aprobada','Finalizada','Cancelado'],
        'briefs_de_clientes': ['En proceso','Contestado','Cancelado'],
        'agenda': ['Pendiente','Confirmada','Finalizada','Cancelada'],
        'ventas': ['Pendiente','Cobrada','Cancelada'],

    }
    options=options.get(table_name, ['Activo', 'Inactivo'])
    return options

def get_open_status(table_name):
    status={
        'clientes': ['En proceso','Perfect match','Swipe','Activo'],
        'proyectos': ['En revisión','En proceso'],
        'pagos_administrativos': ['En revisión','Aprobado'],
        'gastos': ['En revisión','Aprobado','Pagado parcial'],
        'transferencias_de_dinero': ['En revisión','Aprobada'], 
        'ajustes_de_dinero': ['En revisión'],
        'compras': ['En revisión','Aprobada','Recibida parcial'],
        'recepciones_de_compras': ['En revisión','Aprobada'],
        'productos_en_compras': ['Pendiente','Recibido','Recibido parcial'],
        'ajustes_de_inventario': ['En revisión','Aprobado'],
        'transferencias_de_inventario': ['En revisión','Aprobada'],
        'briefs_de_clientes': ['En proceso'],
        'agenda': ['Pendiente','Confirmada'],
        'ventas': ['Pendiente'],
    }
    status=status.get(table_name,['Activo'])
    return status

def get_breadcrumbs(table_name):
    # [modulo,active_menu]
    breadcrumbs={
        'usuarios':['Permisos','permisos'],
        'roles':['Permisos','permisos'],
        'logs_auditoria':['Auditoría','auditoria'],
        'reportes':['Reportes','reportes'],
        'archivos':[session['tabla_origen'].replace('_',' ').capitalize(),session['tabla_origen']],

        'almacenes':['Almacén','almacen'],
        'categorias_de_productos':['Almacén','almacen'],
        'productos':['Almacén','almacen'],
        'inventario':['Almacén','almacen'],
        'recepciones_de_compras':['Almacén','almacen'],
        'ajustes_de_inventario':['Almacén','almacen'],
        'transferencias_de_inventario':['Almacén','almacen'],
        'envios':['Almacén','almacen'],

        'cuentas_de_banco':['Banca','banca'],
        'pagos_administrativos':['Banca','banca'],
        'transferencias_de_dinero':['Banca','banca'],
        'ajustes_de_dinero':['Banca','banca'],
        'pagos_de_nomina':['Banca','banca'],

        'compras':['Compras','compras'],
        'proveedores':['Compras','compras'],
        'categorias_de_gastos':['Compras','compras'],
        'gastos':['Compras','compras'],
        'gastos_recurrentes':['Compras','compras'],
        'precios_de_proveedores':['Compras','compras'],

        'proyectos':['Proyectos','proyectos'],
        'clientes':['Proyectos','proyectos'],
        'briefs_de_clientes':['Proyectos','proyectos'],
        'respuestas_briefs_de_clientes':['Proyectos','proyectos'],
        'briefs':['Proyectos','proyectos'],
        'preguntas_de_briefs':['Proyectos','proyectos'],
        'respuestas_de_preguntas_de_briefs':['Proyectos','proyectos'],
        'agenda':['Proyectos','proyectos'],
        'actividades_base':['Proyectos','proyectos'],
        'actividades':['Proyectos','proyectos'],
        'preguntas_de_calidad_de_servicio':['Proyectos','proyectos'],
        'preguntas_de_encuesta_de_satisfaccion':['Proyectos','proyectos'],

        'puestos':['Recursos Humanos','recursos_humanos'],
        'integrantes':['Recursos Humanos','recursos_humanos'],
        'sueldos_de_integrantes':['Recursos Humanos','recursos_humanos'],

        'espacios_de_proyectos':['Ventas','ventas'],
        'servicios':['Ventas','ventas'],
        'ventas':['Ventas','ventas'],
        'facturas':['Ventas','ventas'],
        'cotizaciones':['Ventas','ventas'],

    }
    breadcrumbs=breadcrumbs.get(table_name,['Bases de datos','bases_de_datos'])
    return breadcrumbs[0],breadcrumbs[1]

def get_table_relationships(table_name):
    relationships={
        'roles':['usuarios'],
        'almacenes':['inventario','compras','recepciones_de_compras','ajustes_de_inventario','transferencias_de_inventario','envios'],
        'proveedores':['compras','gastos','pagos_administrativos','precios_de_proveedores','gastos_recurrentes'],
        'productos':['inventario','precios_de_proveedores'],
        'gastos':['gastos_y_compras_en_pagos'],
        'cuentas_de_banco':['gastos','pagos_administrativos','transferencias_de_dinero','ajustes_de_dinero','pagos_de_nomina'],
        'clientes':['resumen','briefs_de_clientes','agenda','ventas','facturas','proyectos','envios','calidad_de_servicio_de_proyectos'],
        'briefs':['preguntas_de_briefs'],
        'preguntas_de_briefs':['respuestas_de_preguntas_de_briefs'],
        'servicios':['precios_de_servicios'],
        'ventas':['servicios_en_ventas'],

        'pagos_administrativos':['gastos_y_compras_en_pagos'],
        'compras':['productos_en_compras'],
        'recepciones_de_compras':['productos_en_recepciones_de_compras'],

    }
    relationships = relationships.get(table_name, [])
    if table_name not in ('archivos','usuarios','roles','logs_auditoria','reportes','rutas','puestos','preguntas_de_briefs','categorias_de_reportes','categorias_de_productos','inventario','categorias_de_gastos','gastos_recurrentes'):
        relationships.append('archivos')
    return relationships

def get_calendar_date_variable(table_name):
    date_variable={
        'agenda':'fecha',
    }
    date_variable=date_variable.get(table_name,'')
    return date_variable

def get_variable_tabs(table_name):
    tabs = {
        'ejemplo': 'estatus'
    }
    tabs=tabs.get(table_name,'estatus')
    return tabs

def get_data_tabs(table_name,parent_table,id_parent_record):
    column_tabs=get_variable_tabs(table_name)
    tabs=get_estatus_options(table_name)
    model = get_model_by_name(table_name)
    column = getattr(model, column_tabs, None)
    count_col = func.count().label('count')
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
    date_fields=['fecha_venta', 'fecha_orden', 'fecha_de_gasto', 'fecha_de_transferencia','fecha','fecha_hora']
    return date_fields

def get_checkbox(table_name):
    checkbox = {
        'table_name':True,
    }
    checkbox=checkbox.get(table_name, False)
    return checkbox

def get_summary_data(table_name):
    data={
        'clientes': {
                        'primary':['nombre_completo','estatus','correo_electronico'],
                        'data':{'información general':['telefono']}
                        },
    }
    data=data.get(table_name,'')
    return data
# get_kpi(table_name,'sql_name',{'variable': id_parent_record})
def get_summary_kpis(table_name,id_parent_record):
    data = {
        'clientes': {
            'generales': {
                'proyectos': 5
            },
        }
    }
    data=data.get(table_name,'')
    return data