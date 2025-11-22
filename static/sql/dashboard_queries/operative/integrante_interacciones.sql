SELECT 
    concat(i2.nombre_completo, ' - ', COUNT(i.id)) AS integrante_nombre,
    COUNT(i.id) AS total_interacciones
FROM interacciones i
JOIN integrantes i2 ON i.id_integrante = i2.id
WHERE i.fecha_hora >= :start_date
  AND i.fecha_hora < :end_date
  and i.estatus='Finalizada'
GROUP BY i2.id, i2.nombre_completo
ORDER BY total_interacciones DESC
LIMIT 1
