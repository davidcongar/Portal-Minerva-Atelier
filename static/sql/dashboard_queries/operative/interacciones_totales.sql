select
  	count(id) as valor
from interacciones
where 
	estatus='Finalizada'
    AND fecha_hora >= :start_date
    AND fecha_hora < :end_date
