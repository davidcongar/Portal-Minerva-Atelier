import uuid
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from python.models import db
from python.models.sistema import *

class Puestos(db.Model,BaseMixin,AuditMixin):

    nombre = db.Column(db.String(255), nullable=False)
    descripcion=db.Column(db.String(500), nullable=True)
    estatus = db.Column(db.String(255),default="Activo")

class Integrantes(db.Model,BaseMixin,AuditMixin):

    id_puesto=db.Column(db.UUID, db.ForeignKey("puestos.id"), nullable=False)

    nombre_completo = db.Column(db.String(255), nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    genero = db.Column(db.String(255))
    estado_civil = db.Column(db.String(255))
    direccion = db.Column(EncryptedColumn(255))
    codigo_postal = db.Column(EncryptedColumn(255))
    telefono = db.Column(EncryptedColumn(255))
    correo_electronico = db.Column(db.String(255))
    fecha_contratacion = db.Column(db.Date)
    fecha_terminacion = db.Column(db.Date)
    numero_seguridad_social = db.Column(EncryptedColumn(255))
    rfc = db.Column(EncryptedColumn(255))
    curp = db.Column(EncryptedColumn(255))
    estatus = db.Column(db.String(255),default="Activo")

    puesto = db.relationship("Puestos", backref="integrantes", lazy=True)

class Sectores(db.Model,BaseMixin,AuditMixin):

    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)

    estatus = db.Column(db.String(255),default="Activo")

class Empresas(db.Model,BaseMixin,AuditMixin):

    id_sector=db.Column(db.UUID, db.ForeignKey("sectores.id"), nullable=False)

    nombre = db.Column(db.String(255), nullable=False)
    razon_social = db.Column(db.String(255))
    simbolo_de_cotizacion = db.Column(db.String(20))

    estatus = db.Column(db.String(255),default="Activo")

    sector = db.relationship("Sectores", backref="empresas", lazy=True)

class IntegrantesAsignadosAEmpresas(db.Model, BaseMixin, AuditMixin):

    id_integrante = db.Column(db.UUID, db.ForeignKey("integrantes.id"), nullable=False)
    id_empresa = db.Column(db.UUID, db.ForeignKey("empresas.id"), nullable=False)

    integrante = db.relationship("Integrantes", backref=db.backref("integrantes_asignados_a_empresas", lazy=True))
    empresa = db.relationship("Empresas", backref=db.backref("integrantes_asignados_a_empresas", lazy=True))
