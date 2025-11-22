SELECT 
    concat(e.nombre,' - ',COUNT(iei.id_interaccion)) AS empresa_nombre,
    COUNT(iei.id_interaccion) AS total_interacciones
FROM empresas_en_interacciones iei
JOIN interacciones i ON iei.id_interaccion = i.id
JOIN empresas e ON iei.id_empresa = e.id
WHERE i.fecha_hora>= :start_date 
    AND i.fecha_hora<:end_date
    and i.estatus='Finalizada'
GROUP BY e.id, e.nombre
ORDER BY total_interacciones DESC
LIMIT 1
