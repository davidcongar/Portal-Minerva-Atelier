SELECT 
    e.nombre AS empresa,
    COUNT(i.id) AS total_interacciones
FROM interacciones i
JOIN empresas_en_interacciones eei ON eei.id_interaccion = i.id
JOIN empresas e ON eei.id_empresa = e.id
WHERE i.fecha_hora >= :start_date
  AND i.fecha_hora < :end_date
  and i.estatus='Finalizada'
GROUP BY e.id, e.nombre
ORDER BY total_interacciones DESC;
