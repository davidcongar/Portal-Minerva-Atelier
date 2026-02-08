import uuid
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from python.models import db
from python.models.sistema import *


class Proyectos(db.Model,BaseMixin,AuditMixin):

    id_venta=db.Column(db.UUID, db.ForeignKey("ventas.id"),nullable=False)
    id_cliente = db.Column(db.UUID, db.ForeignKey("clientes.id"),nullable=False)
    id_servicio=db.Column(db.UUID, db.ForeignKey("servicios.id"),nullable=False)
    id_espacio = db.Column(db.UUID, db.ForeignKey("espacios.id"), nullable=False)    
    id_integrante = db.Column(db.UUID, db.ForeignKey("integrantes.id"))    

    metros_cuadrados= db.Column(db.Float, nullable=False, default=0.00)
    fecha_inicio = db.Column(db.Date,nullable=False)
    fecha_fin = db.Column(db.Date)
    estatus = db.Column(db.String(100),nullable=False, default="En proceso") # activo,finalizado, cancelado

    venta = db.relationship('Ventas', backref='proyectos',lazy=True)
    cliente = db.relationship('Clientes', backref='proyectos',lazy=True)
    servicio = db.relationship('Servicios', backref='proyectos',lazy=True)
    espacio = db.relationship('Espacios', backref='proyectos',lazy=True)
    integrante = db.relationship('Integrantes', backref='proyectos',lazy=True)


class ActividadesBase(db.Model,BaseMixin,AuditMixin):

    id_servicio = db.Column(db.UUID, db.ForeignKey("servicios.id"),nullable=False)

    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    entregable=db.Column(db.String(255))
    horas_estimadas = db.Column(db.Float, nullable=False, default=0.00)
    estatus = db.Column(db.String(255),default="Activo")

    servicio = db.relationship('Servicios', backref='actividades_base',lazy=True)

class Actividades(db.Model,BaseMixin,AuditMixin):

    id_actividad_base = db.Column(db.UUID, db.ForeignKey("actividades_base.id"),nullable=False)
    id_proyecto=db.Column(db.UUID, db.ForeignKey("proyectos.id"),nullable=False)
    id_integrante=db.Column(db.UUID, db.ForeignKey("integrantes.id"))

    fecha_inicio = db.Column(db.Date)
    fecha_estimada = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)

    horas = db.Column(db.Float, default=0.00)
    notas = db.Column(db.Text)

    calificacion_cliente = db.Column(db.Integer)
    aceptacion_de_cliente = db.Column(db.String(100), default="Sin aceptar") 

    notas_cierre = db.Column(db.Text)
    comentarios_supervisor = db.Column(db.Text)

    estatus = db.Column(db.String(100),nullable=False, default="Sin iniciar") 

    proyecto = db.relationship('Proyectos', backref='actividades',lazy=True)
    integrante = db.relationship('Integrantes', backref='actividades',lazy=True)
    actividad_base = db.relationship('ActividadesBase', backref='actividades', lazy=True)

class ComentariosDeClientesDeActividades(db.Model,BaseMixin,AuditMixin):

    id_actividad = db.Column(db.UUID, db.ForeignKey("actividades.id"),nullable=False)

    comentario_cliente = db.Column(db.Text)
    notas_cierre = db.Column(db.Text)
    estatus = db.Column(db.String(100),nullable=False, default="En proceso") 

    actividad = db.relationship('Actividades', backref='comentarios_de_clientes_de_actividades',lazy=True)

class PreguntasDeCalidadDeServicio(db.Model,BaseMixin,AuditMixin):

    id_servicio = db.Column(db.UUID, db.ForeignKey("servicios.id"),nullable=False)

    orden = db.Column(db.Integer)
    pregunta = db.Column(db.Text)
    tipo_de_respuesta = db.Column(db.String(255))
    opciones = db.Column(db.Text)

    estatus = db.Column(db.String(255),default="Activo")

    servicio = db.relationship('Servicios', backref='preguntas_de_calidad_de_servicio',lazy=True)


class CalidadDeServicioDeProyectos(db.Model,BaseMixin,AuditMixin):

    id_cliente = db.Column(db.UUID, db.ForeignKey("clientes.id"),nullable=False)
    id_proyecto = db.Column(db.UUID, db.ForeignKey("proyectos.id"),nullable=False)
    fecha_cierre = db.Column(db.Date)

    estatus = db.Column(db.String(255),default="En revisión")

    cliente = db.relationship('Clientes', backref='calidad_de_servicio_de_proyectos',lazy=True)
    proyecto = db.relationship('Proyectos', backref='calidad_de_servicio_de_proyectos',lazy=True)


class RespuestasCalidadDeServicio(db.Model,BaseMixin,AuditMixin):

    id_calidad_de_servicio_de_proyecto = db.Column(db.UUID, db.ForeignKey("calidad_de_servicio_de_proyectos.id"),nullable=False)
    id_pregunta_de_calidad_de_servicio = db.Column(db.UUID, db.ForeignKey("preguntas_de_calidad_de_servicio.id"),nullable=False)

    respuesta = db.Column(db.Text)

    calidad_de_servicio_de_proyecto = db.relationship('CalidadDeServicioDeProyectos', backref='calidad_de_servicio_de_proyectos',lazy=True)
    pregunta_de_calidad_de_servicio = db.relationship('PreguntasDeCalidadDeServicio', backref='calidad_de_servicio_de_proyectos',lazy=True)

class PreguntasDeEncuestaDeSatisfaccion(db.Model,BaseMixin,AuditMixin):

    id_servicio = db.Column(db.UUID, db.ForeignKey("servicios.id"),nullable=False)

    orden = db.Column(db.Integer)
    pregunta = db.Column(db.Text)
    tipo_de_respuesta = db.Column(db.String(255))
    opciones = db.Column(db.Text)

    estatus = db.Column(db.String(255),default="Activo")

    servicio = db.relationship('Servicios', backref='preguntas_de_encuesta_de_satisfaccion',lazy=True)


class EncuestaDeSatisfaccionDeProyectos(db.Model,BaseMixin,AuditMixin):

    id_cliente = db.Column(db.UUID, db.ForeignKey("clientes.id"),nullable=False)
    id_proyecto = db.Column(db.UUID, db.ForeignKey("proyectos.id"),nullable=False)
    fecha_cierre = db.Column(db.Date)

    estatus = db.Column(db.String(255),default="En revisión")

    cliente = db.relationship('Clientes', backref='encuesta_de_satisfaccion_de_proyectos',lazy=True)
    proyecto = db.relationship('Proyectos', backref='encuesta_de_satisfaccion_de_proyectos',lazy=True)


class RespuestasEncuestaDeSatisfaccion(db.Model,BaseMixin,AuditMixin):

    id_encuesta_de_satisfaccion_de_proyecto = db.Column(db.UUID, db.ForeignKey("encuesta_de_satisfaccion_de_proyectos.id"),nullable=False)
    id_pregunta_de_encuesta_de_satisfaccion = db.Column(db.UUID, db.ForeignKey("preguntas_de_encuesta_de_satisfaccion.id"),nullable=False)

    respuesta = db.Column(db.Text)

    encuesta_de_satisfaccion_de_proyecto = db.relationship('EncuestaDeSatisfaccionDeProyectos', backref='respuestas_encuesta_de_satisfaccion_de_proyectos',lazy=True)
    pregunta_de_encuesta_de_satisfaccion = db.relationship('PreguntasDeEncuestaDeSatisfaccion', backref='respuestas_encuesta_de_satisfaccion_de_proyectos',lazy=True)
