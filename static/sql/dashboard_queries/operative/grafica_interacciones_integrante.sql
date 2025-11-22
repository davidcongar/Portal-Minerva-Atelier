SELECT 
    ing.nombre_completo AS integrante,
    COUNT(i.id) AS total_interacciones
FROM interacciones i
JOIN integrantes ing ON i.id_integrante = ing.id
WHERE i.fecha_hora >= :start_date
  AND i.fecha_hora < :end_date
  and i.estatus='Finalizada'
GROUP BY ing.id, ing.nombre_completo
ORDER BY total_interacciones DESC;
