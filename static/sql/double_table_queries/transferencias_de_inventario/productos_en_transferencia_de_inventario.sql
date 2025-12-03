select
    prod.id,
    productos.nombre as producto,
    prod.cantidad as cantidad,
    inv.cantidad as cantidad_disponible,
    prod.fecha_de_creacion
from productos_en_transferencias_de_inventario as prod
left join transferencias_de_inventario as transferencia
    on prod.id_transferencia_de_inventario=transferencia.id

left join productos
    on prod.id_producto=productos.id
left join inventario as inv
    on prod.id_producto=inv.id_producto and transferencia.id_almacen_salida=inv.id_almacen
where
    id_transferencia_de_inventario= :id_main_record
