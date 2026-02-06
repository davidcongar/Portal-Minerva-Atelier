select
    prod.id,
    nombre as producto,
    cantidad as cantidad_enviada,
    cantidad_recibida,
    notas,
    prod.fecha_de_creacion
from productos_en_transferencias_de_inventario as prod
left join productos
    on prod.id_producto=productos.id
where
    id_transferencia_de_inventario = :id_main_record
order by nombre