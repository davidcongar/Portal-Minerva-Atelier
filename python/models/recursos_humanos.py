import uuid
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from python.models import db
from python.models.sistema import *

class Puestos(db.Model,BaseMixin,AuditMixin):

    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
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

class SueldosDeIntegrantes(db.Model,BaseMixin,AuditMixin):

    id_integrante = db.Column(db.UUID, db.ForeignKey("integrantes.id"), nullable=False)
    sueldo_bruto = db.Column(db.Float, nullable=False)
    deduccion_imss = db.Column(db.Float)
    deduccion_isr = db.Column(db.Float)
    total_deducciones = db.Column(db.Float)
    sueldo_neto = db.Column(db.Float)

    estatus = db.Column(db.String(50), default="Activo")

    integrante = db.relationship("Integrantes", backref="sueldos_de_integrantes", lazy=True)

    @validates('sueldo_bruto','sueldo_neto','deduccion_imss','deduccion_isr','total_deducciones')
    def validate_non_negative(self, key, value):
        if float(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value
