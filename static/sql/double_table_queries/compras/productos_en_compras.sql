select
    productos_en_compras.id,
    cantidad_ordenada,
    descuento_porcentaje,
    unidad_de_medida,
    nombre,
    precio_unitario,
    subtotal,
    importe_total,
    fecha_entrega_estimada,
    productos_en_compras.fecha_de_creacion
from productos_en_compras
left join productos
    on productos_en_compras.id_producto=productos.id
where
    id_compra= :id_main_record
order by nombre