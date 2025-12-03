with productos_seleccionados as (
    select
        id_producto
    from productos_en_compras
    where 
        id_compra=:id_main_record
),
proveedor as (
    select
        id_proveedor
    from compras
    where id=:id_main_record
),
precios as (
    select * from precios_de_proveedores join proveedor on precios_de_proveedores.id_proveedor=proveedor.id_proveedor
)
select
    productos.id,
    productos.nombre,
    precio_unitario,
    unidad_de_medida,
    productos.fecha_de_creacion
from productos
join precios
    on precios.id_producto=productos.id
where
    productos.estatus='Activo'
    and precios.estatus='Activo'
    AND NOT EXISTS (
      SELECT 1
      FROM productos_seleccionados ps
      WHERE ps.id_producto = productos.id
    )
order by nombre