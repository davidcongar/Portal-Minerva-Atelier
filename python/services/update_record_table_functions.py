from datetime import timedelta
from python.services.system.helper_functions import *
from python.models.modelos import *
from sqlalchemy import func

def get_variables_double_table_view(table_name):
    columns = {
        "integrantes": {
            "columns_first_table":["sector","empresa","simbolo"],
            "columns_second_table":["sector","empresa","simbolo"],
            "title_first_table":"Empresas",
            "title_second_table":"Empresas asignadas a Integrante",
            "query_first_table":"empresas",
            "query_second_table":"empresas_asignadas",
            "model_first_table":"empresas",
            "model_second_table":"integrantes_asignados_a_empresas",
            "details":["nombre_completo"],
            "edit_fields":[]
        },
        "interacciones": {
            "columns_first_table":["sector","empresa","simbolo"],
            "columns_second_table":["sector","empresa","simbolo","notas"],
            "title_first_table":"Empresas",
            "title_second_table":"Empresas comentadas en interacción",
            "query_first_table":"empresas",
            "query_second_table":"empresas_asignadas",
            "model_first_table":"empresas",
            "model_second_table":"empresas_en_interacciones",
            "details":["cliente","integrante","fecha_hora"],
            "edit_fields":['notas']
        },        
    }
    columns=columns.get(table_name,'')
    return columns

def add_record_double_table(main_table_name,second_table,id_main_record,id_record):
    model=get_model_by_name(second_table)
    if main_table_name=='integrantes':
        new_record=model(
            id_integrante=id_main_record,
            id_empresa=id_record,
            id_usuario=session['id_usuario']
        )
    if main_table_name=='interacciones':
        new_record=model(
            id_interaccion=id_main_record,
            id_empresa=id_record,
            id_usuario=session['id_usuario']
        )        
    return new_record

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

def get_update_validation(table_name,record,column,value):
    validation={}
    if table_name=='ejemplo':
        if column=='hora_inicio':
            tiempo_servicio=Servicios.query.filter_by(id=record.id_servicio).first().duracion_en_minutos
            hora_inicio_dt = datetime.combine(datetime.today(), datetime.strptime(value, "%H:%M").time())
            hora_fin_dt = hora_inicio_dt + timedelta(minutes=tiempo_servicio)
            record.hora_fin=hora_fin_dt.time()
        validation['status']=1
    else:
        validation['status']=1
    return validation

def on_add_double_table(table_name,id):
    if table_name=='ejemplo':
        orden=OrdenesDeVenta.query.get(id)

def on_update_double_table(table_name,id):
    if table_name=='ejemplo':
        orden=OrdenesDeVenta.query.get(id)

def on_delete_double_table(table_name,id):
    if table_name=='ejemplo':
        orden=OrdenesDeVenta.query.get(id)
