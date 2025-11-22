select
    seleccion.id as id,
    sectores.nombre as sector,
    empresas.nombre as empresa,
    empresas.simbolo_de_cotizacion as simbolo,
    seleccion.fecha_de_creacion
from integrantes_asignados_a_empresas as seleccion
left join empresas
  on seleccion.id_empresa=empresas.id
left join sectores
  on empresas.id_sector=sectores.id
where
    id_integrante= :id_main_record
