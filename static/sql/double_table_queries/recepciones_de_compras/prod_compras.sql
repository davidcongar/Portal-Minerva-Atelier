with orden as (
    select
        id_compra
    from recepciones_de_compras
    where id=:id_main_record
)
select
    prod.id,
    productos.nombre as producto,
    unidad_de_medida,
    cantidad_ordenada,
    cantidad_ordenada-cantidad_recibida as cantidad_por_recibir,
    prod.fecha_de_creacion
from productos_en_compras as prod
left join productos
    on prod.id_producto=productos.id
join orden on prod.id_compra=orden.id_compra
where
    prod.cantidad_ordenada>prod.cantidad_recibida
order by nombre