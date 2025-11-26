import uuid
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from python.models import db
from python.models.sistema import *


class Clientes(db.Model,BaseMixin,AuditMixin):

    tipo_de_cliente = db.Column(db.String(255), nullable=True)
    nombre = db.Column(db.String(255), nullable=False)
    rfc = db.Column(EncryptedColumn(255))
    direccion = db.Column(EncryptedColumn(255))
    codigo_postal = db.Column(EncryptedColumn(255))
    telefono = db.Column(EncryptedColumn(255))
    correo_electronico = db.Column(EncryptedColumn(255))
    contrasena = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.contrasena = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.contrasena, password)

    estatus = db.Column(db.String(255),default="Inactivo")


class Briefs(db.Model,BaseMixin,AuditMixin):

    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)

class PreguntasDeBriefs(db.Model,BaseMixin,AuditMixin):

    id_brief = db.Column(db.UUID, db.ForeignKey("briefs.id"))
    orden=db.Column(db.Integer, nullable=False)
    pregunta = db.Column(db.String(255), nullable=False)

    brief = db.relationship("Briefs", backref="preguntas_de_briefs", lazy=True)


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
