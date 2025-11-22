WITH base AS (
    SELECT 
        c.id AS cliente_id,
        c.nombre AS cliente,
        c.region,
        cat.nombre AS categoria,
        s.nombre AS sector,
        -- ✅ Group interaction types
        CASE 
            WHEN ti.nombre ILIKE ANY (ARRAY['Llamadas', 'Juntas']) THEN '2Llamadas+Juntas'
            WHEN ti.nombre ILIKE ANY (ARRAY['Mail', 'IMs']) THEN '3Mails+IMs'
            WHEN ti.nombre ILIKE ANY (ARRAY['Corporate Access', 'Acceso Corporativo']) THEN '4Corporate Access+Otros'
            ELSE '4Corporate Access+Otros'
        END AS tipo_interaccion,
        i.fecha_hora::date AS fecha
    FROM interacciones i
    JOIN clientes c ON i.id_cliente = c.id
    LEFT JOIN categorias_de_clientes cat ON cat.id = c.id_categoria_de_cliente
    JOIN tipos_de_interacciones ti ON i.id_tipo_de_interaccion = ti.id
    LEFT JOIN empresas_en_interacciones eei ON eei.id_interaccion = i.id
    LEFT JOIN empresas e ON eei.id_empresa = e.id
    LEFT JOIN sectores s ON e.id_sector = s.id
    WHERE i.estatus = 'Finalizada'
),
grouped AS (
    SELECT
        b.sector,
        b.region,
        b.categoria AS categoria_cliente,
        b.cliente,
        b.tipo_interaccion,
        MAX(b.fecha) AS ultima_interaccion,
        COUNT(*) FILTER (WHERE EXTRACT(quarter FROM b.fecha) = 1) AS q1,
        COUNT(*) FILTER (WHERE EXTRACT(quarter FROM b.fecha) = 2) AS q2,
        COUNT(*) FILTER (WHERE EXTRACT(quarter FROM b.fecha) = 3) AS q3,
        COUNT(*) FILTER (WHERE EXTRACT(quarter FROM b.fecha) = 4) AS q4,
        COUNT(*) FILTER (
            WHERE b.fecha < CURRENT_DATE - INTERVAL '21 days'
              AND b.fecha >= CURRENT_DATE - INTERVAL '28 days'
        ) AS W4,   
        COUNT(*) FILTER (
            WHERE b.fecha < CURRENT_DATE - INTERVAL '14 days'
              AND b.fecha >= CURRENT_DATE - INTERVAL '21 days'
        ) AS W3,
        COUNT(*) FILTER (
            WHERE b.fecha < CURRENT_DATE - INTERVAL '7 days'
              AND b.fecha >= CURRENT_DATE - INTERVAL '14 days'
        ) AS W2,
        COUNT(*) FILTER (WHERE b.fecha >= CURRENT_DATE - INTERVAL '7 days') AS W1,
        COUNT(*) AS total
    FROM base b
    GROUP BY b.region, b.sector, b.categoria, b.cliente, b.tipo_interaccion
),
unioned AS (
    SELECT * FROM grouped
    UNION ALL
    SELECT 
        g.sector,
        g.region,
        g.categoria_cliente,
        g.cliente,
        '1Interacciones exitosas' AS tipo_interaccion,
        MAX(g.ultima_interaccion),
        SUM(g.q1),
        SUM(g.q2),
        SUM(g.q3),
        SUM(g.q4),
        SUM(g.W4),
        SUM(g.W3),
        SUM(g.W2),
        SUM(g.W1),
        SUM(g.total)
    FROM grouped g
    GROUP BY g.region, g.sector, g.categoria_cliente, g.cliente
)
-- ✅ Outer SELECT with CASE ordering (now legal)
SELECT 
    *,
    CASE 
        WHEN tipo_interaccion = '1Interacciones exitosas' THEN 1
        WHEN tipo_interaccion = '2Llamadas+Juntas' THEN 2
        WHEN tipo_interaccion = '3Mails+IMs' THEN 3
        WHEN tipo_interaccion = '4Corporate Access+Otros' THEN 4
        ELSE 5
    END AS tipo_order
FROM unioned
ORDER BY region, sector, categoria_cliente, cliente, tipo_order
