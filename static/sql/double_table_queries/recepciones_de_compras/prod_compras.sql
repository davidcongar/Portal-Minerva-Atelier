WITH orden AS (
    SELECT
        id_compra
    FROM recepciones_de_compras
    WHERE id = :id_main_record
),
productos_seleccionados AS (
    SELECT
        id_producto
    FROM productos_en_recepciones_de_compras
    WHERE id_recepcion_de_compra = :id_main_record
)
SELECT
    prod.id,
    productos.nombre AS producto,
    productos.unidad_de_medida,
    prod.cantidad_ordenada,
    prod.cantidad_ordenada - prod.cantidad_recibida AS cantidad_por_recibir,
    prod.fecha_de_creacion
FROM productos_en_compras AS prod
LEFT JOIN productos
    ON prod.id_producto = productos.id
LEFT JOIN orden
    ON prod.id_compra = orden.id_compra
WHERE
    prod.cantidad_ordenada > prod.cantidad_recibida
    AND NOT EXISTS (
        SELECT 1
        FROM productos_seleccionados ps
        WHERE ps.id_producto = productos.id
    )
ORDER BY productos.nombre