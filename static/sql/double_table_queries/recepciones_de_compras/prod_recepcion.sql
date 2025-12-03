select
    prod.id,
    nombre as producto,
    unidad_de_medida,
    cantidad,
    prod.fecha_de_creacion
from productos_en_recepciones_de_compras as prod
left join productos
    on prod.id_producto=productos.id
where
    id_recepcion_de_compra= :id_main_record
order by nombre