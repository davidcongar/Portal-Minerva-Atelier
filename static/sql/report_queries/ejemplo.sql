SELECT 
    sucursal,
    fecha,
    categoria,
    importe
FROM (
    -- productos
    SELECT 
        suc.nombre AS sucursal,
        DATE_TRUNC('month', orden.fecha_orden)::date AS fecha,
        TO_CHAR(orden.fecha_orden, 'YYYYMM')::int AS mes_orden,
        cat.nombre AS categoria,
        SUM(prod.importe_total) AS importe
    FROM productos_en_ordenes_de_compra AS prod
    LEFT JOIN ordenes_de_compra AS orden
        ON prod.id_orden_de_compra = orden.id
    LEFT JOIN productos
        ON prod.id_producto = productos.id
    LEFT JOIN categorias_de_productos AS cat
        ON productos.id_categoria_de_producto = cat.id
    LEFT JOIN sucursales AS suc
        ON orden.id_sucursal = suc.id
    WHERE orden.estatus NOT IN ('En revisión','Cancelada')
      AND orden.id_empresa = :id_empresa
    GROUP BY suc.nombre, DATE_TRUNC('month', orden.fecha_orden), TO_CHAR(orden.fecha_orden, 'YYYYMM'), cat.nombre

    UNION

    -- costo de envío
    SELECT
        suc.nombre AS sucursal,
        DATE_TRUNC('month', oc.fecha_orden)::date AS fecha,
        TO_CHAR(oc.fecha_orden, 'YYYYMM')::int AS mes_orden,
        'Costo de envío' AS categoria,
        SUM(oc.costo_de_envio) AS importe
    FROM ordenes_de_compra AS oc
    LEFT JOIN sucursales AS suc
        ON oc.id_sucursal = suc.id
    WHERE oc.estatus NOT IN ('En revisión','Cancelada')
      AND oc.id_empresa = :id_empresa
    GROUP BY suc.nombre, DATE_TRUNC('month', oc.fecha_orden), TO_CHAR(oc.fecha_orden, 'YYYYMM')

    UNION

    -- otros costos
    SELECT
        suc.nombre AS sucursal,
        DATE_TRUNC('month', oc.fecha_orden)::date AS fecha,
        TO_CHAR(oc.fecha_orden, 'YYYYMM')::int AS mes_orden,
        'Otros costos' AS categoria,
        SUM(oc.otros_costos) AS importe
    FROM ordenes_de_compra AS oc
    LEFT JOIN sucursales AS suc
        ON oc.id_sucursal = suc.id
    WHERE oc.estatus NOT IN ('En revisión','Cancelada')
      AND oc.id_empresa = :id_empresa
    GROUP BY suc.nombre, DATE_TRUNC('month', oc.fecha_orden), TO_CHAR(oc.fecha_orden, 'YYYYMM')
) t
WHERE importe > 0
ORDER BY sucursal, mes_orden, importe DESC
