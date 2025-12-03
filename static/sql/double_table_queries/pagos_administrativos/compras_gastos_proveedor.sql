WITH compras_gastos_seleccionados AS (
  SELECT id_gasto,id_compra
  FROM gastos_y_compras_en_pagos
  WHERE id_pago = :id_main_record
),
proveedor_pago AS (
  SELECT id_proveedor
  FROM pagos_administrativos
  WHERE id = :id_main_record
),
compras as (
    SELECT
        compras.id as id,
        compras.id_visualizacion as id_,
        'C' as tipo,
        nombre as proveedor,
        notas,
        importe_total,
        importe_pagado,
        importe_total-importe_pagado as importe_restante,
        compras.fecha_de_creacion
    FROM compras
    JOIN proveedor_pago
        ON proveedor_pago.id_proveedor = compras.id_proveedor
    left join proveedores
        on compras.id_proveedor=proveedores.id
    where 
        compras.estatus in ('Aprobada','Recibida','Recibida parcial','Finalizada')
        and compras.estatus_de_pago in ('Sin pagar','Pagada parcial')
        and importe_total-importe_pagado>0
        AND NOT EXISTS (
            SELECT 2
            FROM compras_gastos_seleccionados
            WHERE compras_gastos_seleccionados.id_compra = compras.id
        )
),
gastos as (
    SELECT
        gastos.id as id,
        gastos.id_visualizacion as id_,
        'G' as tipo,
        nombre as proveedor,
        notas,
        importe as importe_total,
        importe_pagado,
        importe-importe_pagado as importe_restante,
        gastos.fecha_de_creacion
    FROM gastos
    JOIN proveedor_pago
        ON proveedor_pago.id_proveedor = gastos.id_proveedor
    left join proveedores
        on gastos.id_proveedor=proveedores.id
    where 
        gastos.estatus in ('Aprobado','Pagado parcial')
        and importe-importe_pagado>0
        AND NOT EXISTS (
            SELECT 1
            FROM compras_gastos_seleccionados
            WHERE compras_gastos_seleccionados.id_gasto = gastos.id
        )
)
select * from compras
union
select * from gastos


