SELECT 
    round(AVG(valor)) AS valor
FROM (
    SELECT 
        id_integrante,
        COUNT(id) AS valor
    FROM interacciones
    WHERE 
        estatus = 'Finalizada'
        aND fecha_hora >= :start_date
        AND fecha_hora < :end_date
    GROUP BY id_integrante
) AS sub;
