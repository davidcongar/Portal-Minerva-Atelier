SELECT * 
FROM (
    -- productos
    SELECT 
        TO_CHAR(orden.fecha_orden, 'MM/YY') AS mes,
        TO_CHAR(orden.fecha_orden, 'YYYYMM')::int AS mes_orden,
        cat.nombre AS categoria,
        SUM(prod.importe_total) AS importe
    FROM productos_en_ordenes_de_compra AS prod
    LEFT JOIN ordenes_de_compra AS orden
        ON prod.id_compra = orden.id
    LEFT JOIN productos
        ON prod.id_producto = productos.id
    LEFT JOIN categorias_de_productos AS cat
        ON productos.id_categoria_de_producto = cat.id
    WHERE orden.estatus NOT IN ('En revisión','Cancelada')
      AND orden.fecha_orden >= :fecha_inicio
      AND orden.fecha_orden <= :fecha_fin
      AND orden.id_empresa = :id_empresa
      AND (:id_sucursal = 'all' OR orden.id_sucursal = NULLIF(:id_sucursal, 'all')::uuid)
    GROUP BY TO_CHAR(orden.fecha_orden, 'MM/YY'), TO_CHAR(orden.fecha_orden, 'YYYYMM'), cat.nombre

    UNION

    -- costo de envío
    SELECT
        TO_CHAR(oc.fecha_orden, 'MM/YY') AS mes,
        TO_CHAR(oc.fecha_orden, 'YYYYMM')::int AS mes_orden,
        'Costo de envío' AS categoria,
        SUM(oc.costo_de_envio) AS importe
    FROM ordenes_de_compra AS oc
    WHERE oc.estatus NOT IN ('En revisión','Cancelada')
      AND oc.fecha_orden >= :fecha_inicio
      AND oc.fecha_orden <= :fecha_fin
      AND oc.id_empresa = :id_empresa
      AND (:id_sucursal = 'all' OR oc.id_sucursal = NULLIF(:id_sucursal, 'all')::uuid)
    GROUP BY TO_CHAR(oc.fecha_orden, 'MM/YY'), TO_CHAR(oc.fecha_orden, 'YYYYMM')

    UNION

    -- otros costos
    SELECT
        TO_CHAR(oc.fecha_orden, 'MM/YY') AS mes,
        TO_CHAR(oc.fecha_orden, 'YYYYMM')::int AS mes_orden,
        'Otros costos' AS categoria,
        SUM(oc.otros_costos) AS importe
    FROM ordenes_de_compra AS oc
    WHERE oc.estatus NOT IN ('En revisión','Cancelada')
      AND oc.fecha_orden >= :fecha_inicio
      AND oc.fecha_orden <= :fecha_fin
      AND oc.id_empresa = :id_empresa
      AND (:id_sucursal = 'all' OR oc.id_sucursal = NULLIF(:id_sucursal, 'all')::uuid)
    GROUP BY TO_CHAR(oc.fecha_orden, 'MM/YY'), TO_CHAR(oc.fecha_orden, 'YYYYMM')
) t
WHERE importe > 0
ORDER BY mes_orden, importe DESC;
