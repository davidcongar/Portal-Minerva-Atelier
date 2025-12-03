with compras as (
    select
        gastos_y_compras_en_pagos.id,
        'C' as tipo,
        proveedores.nombre as proveedor,
        gastos_y_compras_en_pagos.notas,
        gastos_y_compras_en_pagos.importe,
        compras.importe_total-compras.importe_pagado as importe_restante,
        gastos_y_compras_en_pagos.fecha_de_creacion
    from gastos_y_compras_en_pagos
    left join compras
        on gastos_y_compras_en_pagos.id_compra=compras.id  
    left join proveedores
        on  compras.id_proveedor=proveedores.id
    where
        id_compra is not null
        and id_pago = :id_main_record
),
gastos as (
    select
        gastos_y_compras_en_pagos.id,
        'G' as tipo,
        proveedores.nombre as proveedor,
        gastos_y_compras_en_pagos.notas,
        gastos_y_compras_en_pagos.importe,
        gastos.importe-gastos.importe_pagado  as importe_restante,
        gastos_y_compras_en_pagos.fecha_de_creacion
    from gastos_y_compras_en_pagos
    left join gastos
        on gastos_y_compras_en_pagos.id_gasto=gastos.id  
    left join proveedores
        on  gastos.id_proveedor=proveedores.id
    where
        id_gasto is not null
        and id_pago = :id_main_record
)
select * from gastos
union
select * from compras
