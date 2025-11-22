SELECT 
    c.nombre AS cliente,
    COUNT(i.id) AS total_interacciones
FROM interacciones i
JOIN clientes c ON i.id_cliente = c.id
WHERE i.fecha_hora >= :start_date
  AND i.fecha_hora < :end_date
  and i.estatus='Finalizada'
GROUP BY c.id, c.nombre
ORDER BY total_interacciones DESC
