import uuid
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from python.models import db
from python.models.sistema import *

class CategoriasDeClientes(db.Model,BaseMixin,AuditMixin):

    nombre = db.Column(db.String(255), nullable=False)
    descripcion=db.Column(db.String(500), nullable=True)

    estatus = db.Column(db.String(255),default="Activo")

class Clientes(db.Model,BaseMixin,AuditMixin):

    id_categoria_de_cliente = db.Column(db.UUID, db.ForeignKey("categorias_de_clientes.id"), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    region = db.Column(db.String(255))     # Nacional, Internacionales
    fecha_de_apertura=db.Column(db.Date, default=datetime.utcnow, nullable=False)
    razon_social = db.Column(db.String(255))
    rfc = db.Column(EncryptedColumn(255))
    direccion = db.Column(EncryptedColumn(255))
    codigo_postal = db.Column(EncryptedColumn(255))
    telefono = db.Column(EncryptedColumn(255))
    correo_electronico = db.Column(EncryptedColumn(255))

    estatus = db.Column(db.String(255),default="Contacto inicial") #Perdido, Activo, Inactivo 

    categoria_de_cliente = db.relationship("CategoriasDeClientes", backref=db.backref("clientes", lazy=True))

class ContactosDeClientes(db.Model,BaseMixin,AuditMixin):

    id_cliente = db.Column(db.UUID, db.ForeignKey("clientes.id"), nullable=False)

    nombre = db.Column(db.String(255), nullable=False)
    telefono = db.Column(EncryptedColumn(255))
    correo_electronico = db.Column(EncryptedColumn(255))

    estatus = db.Column(db.String(255),default="Activo")
    
    cliente = db.relationship("Clientes", backref=db.backref("contactos_de_clientes", lazy=True))


class CategoriasDeInteracciones(db.Model,BaseMixin,AuditMixin):

    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)

    estatus = db.Column(db.String(255),default="Activo")

class TiposDeInteracciones(db.Model,BaseMixin,AuditMixin):

    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)

    estatus = db.Column(db.String(255),default="Activo")


class Interacciones(db.Model, BaseMixin, AuditMixin):

    id_integrante = db.Column(db.UUID, db.ForeignKey("integrantes.id"), nullable=False)
    id_cliente = db.Column(db.UUID, db.ForeignKey("clientes.id"), nullable=False)
    id_contacto_de_cliente= db.Column(db.UUID, db.ForeignKey("contactos_de_clientes.id"), nullable=False)
    id_tipo_de_interaccion= db.Column(db.UUID, db.ForeignKey("tipos_de_interacciones.id"), nullable=False)
    id_categoria_de_interaccion= db.Column(db.UUID, db.ForeignKey("categorias_de_interacciones.id"), nullable=False)

    iniciada_por = db.Column(db.String(255))
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    duracion_minutos = db.Column(db.Integer,default=0)
    descripcion = db.Column(db.Text)
    estatus = db.Column(db.String(255),default="Pendiente") # Pendiente,Finalizada,Cancelada
    
    integrante = db.relationship("Integrantes", backref=db.backref("interacciones", lazy=True))
    cliente = db.relationship("Clientes", backref=db.backref("interacciones", lazy=True))
    contacto_de_cliente = db.relationship("ContactosDeClientes", backref=db.backref("interacciones", lazy=True))
    tipo_de_interaccion = db.relationship("TiposDeInteracciones", backref=db.backref("interacciones", lazy=True))
    categoria_de_interaccion = db.relationship("CategoriasDeInteracciones", backref=db.backref("interacciones", lazy=True))

class EmpresasEnInteracciones(db.Model, BaseMixin, AuditMixin):

    id_interaccion = db.Column(db.UUID, db.ForeignKey("interacciones.id"), nullable=False)
    id_empresa= db.Column(db.UUID, db.ForeignKey("empresas.id"), nullable=False)

    notas = db.Column(db.Text)
    
    empresa = db.relationship("Empresas", backref=db.backref("empresas_en_interacciones", lazy=True))
    interaccion = db.relationship("Interacciones", backref=db.backref("empresas_en_interacciones", lazy=True))

class InteresesDeClientes(db.Model, BaseMixin, AuditMixin):

    id_cliente = db.Column(db.UUID, db.ForeignKey("clientes.id"), nullable=False)
    id_interaccion = db.Column(db.UUID, db.ForeignKey("interacciones.id"), nullable=False)
    id_empresa = db.Column(db.UUID, db.ForeignKey("empresas.id"), nullable=False)

    fecha = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    descripcion = db.Column(db.Text)
    
    cliente = db.relationship("Clientes", backref=db.backref("intereses_de_clientes", lazy=True))
    empresa = db.relationship("Empresas", backref=db.backref("intereses_de_clientes", lazy=True))
    interaccion = db.relationship("Interacciones", backref=db.backref("intereses_de_clientes", lazy=True))

class Actividades(db.Model, BaseMixin, AuditMixin):

    id_integrante = db.Column(db.UUID, db.ForeignKey("integrantes.id"), nullable=False)
    id_cliente = db.Column(db.UUID, db.ForeignKey("clientes.id"), nullable=False)

    fecha = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    descripcion = db.Column(db.Text)
    estatus = db.Column(db.String(255),default="Pendiente") # Pendiente,Finalizada,Cancelada

    integrante = db.relationship("Integrantes", backref=db.backref("actividades", lazy=True))
    cliente = db.relationship("Clientes", backref=db.backref("actividades", lazy=True))
