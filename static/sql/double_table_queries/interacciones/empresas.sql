WITH seleccion AS (
  SELECT id_empresa
  FROM empresas_en_interacciones
  WHERE id_interaccion = :id_main_record
)
SELECT
	empresas.id as id,
    sectores.nombre as sector,
    empresas.nombre as empresa,
    empresas.simbolo_de_cotizacion as simbolo,
    empresas.fecha_de_creacion
FROM empresas
left join sectores
  on empresas.id_sector=sectores.id
  WHERE
    NOT EXISTS (
      SELECT 1
      FROM seleccion
      WHERE seleccion.id_empresa = empresas.id
    )
    and empresas.estatus='Activo'
