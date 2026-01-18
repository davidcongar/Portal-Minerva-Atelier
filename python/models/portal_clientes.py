import uuid
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from python.models import db
from python.models.sistema import *


class Clientes(db.Model,BaseMixin,AuditMixin):

    nombre_completo = db.Column(db.String(255), nullable=False)
    rfc = db.Column(EncryptedColumn(255))
    razon_social = db.Column(db.String(255))
    regimen_fiscal = db.Column(db.String(255))
    domicilio_fiscal = db.Column(db.String(255))    
    direccion = db.Column(EncryptedColumn(255))
    codigo_postal = db.Column(EncryptedColumn(255))
    telefono = db.Column(EncryptedColumn(255))
    correo_electronico = db.Column(EncryptedColumn(255))
    contrasena = db.Column(db.String(255))

    def set_password(self, password):
        self.contrasena = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.contrasena, password)

    estatus = db.Column(db.String(255),default="En proceso")


class Briefs(db.Model,BaseMixin,AuditMixin):

    id_servicio = db.Column(db.UUID, db.ForeignKey("servicios.id"))

    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    estatus = db.Column(db.String(255),default="Activo")

    servicio = db.relationship('Servicios', backref='briefs',lazy=True)

class PreguntasDeBriefs(db.Model,BaseMixin,AuditMixin):

    id_brief = db.Column(db.UUID, db.ForeignKey("briefs.id"))
    orden=db.Column(db.Integer, nullable=False)
    pregunta = db.Column(db.String(255), nullable=False)
    estatus = db.Column(db.String(255),default="Activo")

    brief = db.relationship("Briefs", backref="preguntas_de_briefs", lazy=True)

class RespuestasDePreguntasDeBriefs(db.Model,BaseMixin,AuditMixin):

    id_pregunta_de_brief = db.Column(db.UUID, db.ForeignKey("preguntas_de_briefs.id"))
    respuesta=db.Column(db.String(255), nullable=False)

    estatus = db.Column(db.String(255),default="Activo")

    pregunta_de_brief = db.relationship("PreguntasDeBriefs", backref="respuestas_de_preguntas_de_briefs", lazy=True)

class Agenda(db.Model,BaseMixin,AuditMixin):

    id_integrante = db.Column(db.UUID, db.ForeignKey("integrantes.id"), nullable=True)
    id_cliente = db.Column(db.UUID, db.ForeignKey("clientes.id"), nullable=False)
    
    fecha = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=True)
    notas = db.Column(db.Text) 
    motivo_de_cancelacion = db.Column(db.Text) 
    estatus = db.Column(db.String(50), default="Pendiente")  # e.g., Pendiente, Confirmado, Completado, Cancelado

    cliente = db.relationship("Clientes", backref="agenda", lazy=True)
    integrante = db.relationship("Integrantes", backref="agenda", lazy=True)

class BriefsDeClientes(db.Model,BaseMixin,AuditMixin):

    id_cliente = db.Column(db.UUID, db.ForeignKey("clientes.id"),nullable=False)
    id_brief = db.Column(db.UUID, db.ForeignKey("briefs.id"),nullable=False)
    id_proyecto = db.Column(db.UUID, db.ForeignKey("proyectos.id"))
    fecha_cierre = db.Column(db.Date)

    estatus = db.Column(db.String(255),default="En proceso")

    brief = db.relationship('Briefs', backref='briefs_de_clientes',lazy=True)
    cliente = db.relationship('Clientes', backref='briefs_de_clientes',lazy=True)
    proyecto = db.relationship('Proyectos', backref='briefs_de_clientes',lazy=True)


class RespuestasBriefsDeClientes(db.Model,BaseMixin,AuditMixin):

    id_brief_de_cliente = db.Column(db.UUID, db.ForeignKey("briefs_de_clientes.id"),nullable=False)
    id_pregunta_de_brief = db.Column(db.UUID, db.ForeignKey("preguntas_de_briefs.id"),nullable=False)

    respuesta = db.Column(db.Text)

    brief_de_cliente = db.relationship('BriefsDeClientes', backref='respuestas_briefs_de_clientes',lazy=True)
    pregunta_de_brief = db.relationship('PreguntasDeBriefs', backref='respuestas_briefs_de_clientes',lazy=True)
