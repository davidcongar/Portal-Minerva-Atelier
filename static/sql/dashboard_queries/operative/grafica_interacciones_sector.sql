SELECT 
    s.nombre AS sector,
    TO_CHAR(DATE_TRUNC('week', i.fecha_hora), 'YYYY-MM-DD') AS semana,
    COUNT(i.id) AS total_interacciones
FROM interacciones i
JOIN empresas_en_interacciones eei ON eei.id_interaccion = i.id
JOIN empresas e ON eei.id_empresa = e.id
JOIN sectores s ON e.id_sector = s.id
WHERE i.fecha_hora >= :start_date
  AND i.fecha_hora < :end_date
  and i.estatus='Finalizada'
GROUP BY s.nombre, DATE_TRUNC('week', i.fecha_hora)
ORDER BY s.nombre, semana;
