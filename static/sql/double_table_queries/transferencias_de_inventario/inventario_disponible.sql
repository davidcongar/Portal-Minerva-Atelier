with almacen_salida as (
    select
        id_almacen_salida
    from transferencias_de_inventario
    where 
        id=:id_main_record
)
select
    inv.id as id,
    productos.nombre as producto,
    almacenes.nombre as almacen,
    cantidad as cantidad_disponible,
    inv.fecha_de_creacion
from inventario as inv
join almacen_salida
    on inv.id_almacen=almacen_salida.id_almacen_salida
left join almacenes
    on inv.id_almacen=almacenes.id
left join productos
    on inv.id_producto=productos.id
where
    cantidad>0