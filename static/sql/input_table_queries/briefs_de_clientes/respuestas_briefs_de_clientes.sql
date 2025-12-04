select
    respuestas_briefs_de_clientes.id,
    pregunta,
    respuesta,
    respuestas_briefs_de_clientes.fecha_de_creacion
from respuestas_briefs_de_clientes 
left join briefs_de_clientes
    on respuestas_briefs_de_clientes.id_brief_de_cliente=briefs_de_clientes.id
left join preguntas_de_briefs
    on respuestas_briefs_de_clientes.id_pregunta_de_brief=preguntas_de_briefs.id 
where
    id_brief_de_cliente = :id_main_record
order by preguntas_de_briefs.orden