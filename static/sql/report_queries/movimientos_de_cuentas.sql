with pagos_cuenta as (
    select
        fecha_pago as fecha,
        'pago administrativo' as tipo,
        concat('Pago a ',proveedores.nombre) as concepto,
        importe as salida,
        0 as entrada,
        pagos.id_visualizacion as id_registro
    from pagos_administrativos as pagos
    left join proveedores
        on pagos.id_proveedor=proveedores.id
    where 
        id_cuenta_de_banco=:id_cuenta_de_banco
        and pagos.estatus in ('Pagado')
),
pagos_nomina as (
    select
        fecha as fecha,
        'Pago de nómina' as tipo,
        concat('Pago de nómina de sucursal ',sucursales.nombre) as concepto,
        importe_total as salida,
        0 as entrada,
        pagos_de_nomina.id_visualizacion as id_registro
    from pagos_de_nomina
    left join sucursales
        on pagos_de_nomina.id_sucursal=sucursales.id
    where 
        id_cuenta_de_banco=:id_cuenta_de_banco
        and pagos_de_nomina.estatus in ('Pagado')
),
transferencias_salidas as (
    select
        fecha_de_transferencia as fecha,
        'Transferencia de dinero' as tipo,
        concat('Transferencia de dinero a cuenta ',cuentas_de_banco.nombre) as concepto,
        importe as salida,
        0 as entrada,
        transferencias_de_dinero.id_visualizacion as id_registro
    from transferencias_de_dinero
    left join cuentas_de_banco
        on transferencias_de_dinero.id_cuenta_de_banco_entrada=cuentas_de_banco.id
    where 
        id_cuenta_de_banco_salida=:id_cuenta_de_banco
        and transferencias_de_dinero.estatus in ('Realizada')
),
ajustes_salidas as (
    select
        fecha_de_ajuste as fecha,
        'Ajuste de dinero' as tipo,
        concat('Ajuste de dinero - ',notas) as concepto,
        importe as salida,
        0 as entrada,
        ajustes_de_dinero.id_visualizacion as id_registro
    from ajustes_de_dinero
    where 
        tipo_de_ajuste='Salida'
        and id_cuenta_de_banco=:id_cuenta_de_banco
        and ajustes_de_dinero.estatus in ('Realizado')
),
ventas as (
     select
        fecha_venta as fecha,
        'Venta' as tipo,
        concat('Venta de sucursal ',sucursales.nombre) as concepto,
        0 as salida,
        importe_total as entrada,
        ordenes_de_venta.id_visualizacion as id_registro
    from ordenes_de_venta
    left join sucursales
        on ordenes_de_venta.id_sucursal=sucursales.id
    where 
        id_cuenta_de_banco=:id_cuenta_de_banco
        and ordenes_de_venta.estatus in ('Finalizada')   
),
transferencias_entradas as (
    select
        fecha_de_transferencia as fecha,
        'Transferencia de dinero' as tipo,
        concat('Transferencia de dinero de cuenta ',cuentas_de_banco.nombre) as concepto,
        0 as salida,
        importe as entrada,
        transferencias_de_dinero.id_visualizacion as id_registro
    from transferencias_de_dinero
    left join cuentas_de_banco
        on transferencias_de_dinero.id_cuenta_de_banco_salida=cuentas_de_banco.id
    where 
        id_cuenta_de_banco_entrada=:id_cuenta_de_banco
        and transferencias_de_dinero.estatus in ('Realizada')
),
ajustes_entradas as (
    select
        fecha_de_ajuste as fecha,
        'Ajuste de dinero' as tipo,
        concat('Ajuste de dinero - ',notas) as concepto,
        0 as salida,
        importe as entrada,
        ajustes_de_dinero.id_visualizacion as id_registro
    from ajustes_de_dinero
    where 
        tipo_de_ajuste='Entrada'
        and id_cuenta_de_banco=:id_cuenta_de_banco
        and ajustes_de_dinero.estatus in ('Realizado')
),
final as (
    select * from ventas
    union all
    select * from transferencias_entradas
    union all
    select * from ajustes_entradas
    union all
    select * from ajustes_salidas
    union all
    select * from pagos_nomina
    union all
    select * from pagos_cuenta
    union all
    select * from transferencias_salidas
),
totales as (
    select
        null::date as fecha,
        'TOTAL' as tipo,
        null as concepto,
        sum(entrada) as "Entrada ($)",
        sum(salida) as "Salida ($)",
        null::integer as id_registro
    from final
)
select * from totales
union all
select 
    fecha,
    tipo,
    concepto,
    entrada as "Entrada ($)",
    salida as "Salida ($)",
    id_registro
from final
order by fecha nulls first
