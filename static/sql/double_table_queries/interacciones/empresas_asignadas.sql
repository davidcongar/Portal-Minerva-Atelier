select
    seleccion.id as id,
    sectores.nombre as sector,
    empresas.nombre as empresa,
    empresas.simbolo_de_cotizacion as simbolo,
    seleccion.notas as notas,
    seleccion.fecha_de_creacion
from empresas_en_interacciones as seleccion
left join empresas
  on seleccion.id_empresa=empresas.id
left join sectores
  on empresas.id_sector=sectores.id
where
    id_interaccion= :id_main_record
