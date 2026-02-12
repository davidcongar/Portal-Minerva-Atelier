select
    sueldo.id,
    nombre_completo as integrante,
    sueldo_bruto,
    bono,
    sueldo_bruto_real,
    deduccion_imss,
    deduccion_isr,
    total_deducciones,
    ajuste,
    sueldo_neto,
    notas,
    sueldo.fecha_de_creacion
from sueldos_pagados_en_nomina as sueldo
left join integrantes
    on sueldo.id_integrante=integrantes.id
where
    sueldo.id_pago_de_nomina = :id_main_record
order by nombre_completo