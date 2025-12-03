import uuid
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from python.models import db
from python.models.sistema import *

class Proveedores(db.Model,BaseMixin,AuditMixin):
    nombre = db.Column(db.String(255), nullable=False)
    razon_social = db.Column(db.String(255))
    rfc = db.Column(EncryptedColumn(255))
    direccion = db.Column(EncryptedColumn(255))
    codigo_postal = db.Column(db.String(20))
    telefono = db.Column(EncryptedColumn(255))
    correo_electronico = db.Column(EncryptedColumn(255))

    persona_contacto = db.Column(db.String(255))
    telefono_contacto = db.Column(db.String(50))
    correo_electronico_contacto = db.Column(db.String(255))
    condiciones_pago = db.Column(db.String(100))

    sitio_web = db.Column(db.String(255))
    estatus = db.Column(db.String(255),default="Activo")

class CategoriasDeGastos(db.Model,BaseMixin,AuditMixin):
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    estatus = db.Column(db.String(255),default="Activo")
  
class Gastos(db.Model,BaseMixin,AuditMixin):

    id_categoria_de_gasto=db.Column(db.UUID, db.ForeignKey("categorias_de_gastos.id"),nullable=False)
    id_proveedor = db.Column(db.UUID, db.ForeignKey("proveedores.id"),nullable=False)
    id_cuenta_de_banco = db.Column(db.UUID, db.ForeignKey("cuentas_de_banco.id"), nullable=True) 

    importe =db.Column(db.Float, nullable=False, default=0.00)
    importe_pagado = db.Column(db.Float, nullable=False, default=0.00)
    fecha_de_gasto = db.Column(db.Date)
    folio_fiscal_uuid=db.Column(db.String)
    fecha_de_comprobante=db.Column(db.String)
    notas = db.Column(db.Text)
    estatus = db.Column(db.String(100),nullable=False, default="En revisión") # en revision,aprobado, pagado parcial, pagado

    proveedor = db.relationship('Proveedores', backref='gastos', lazy=True)
    categoria = db.relationship('CategoriasDeGastos', backref='gastos', lazy=True)
    cuenta_de_banco = db.relationship("CuentasDeBanco", backref="gastos", lazy=True)

    @validates('importe')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value

class GastosRecurrentes(db.Model,BaseMixin,AuditMixin):

    id_categoria_de_gasto=db.Column(db.UUID, db.ForeignKey("categorias_de_gastos.id"),nullable=False)
    id_proveedor = db.Column(db.UUID, db.ForeignKey("proveedores.id"),nullable=False)
    id_cuenta_de_banco = db.Column(db.UUID, db.ForeignKey("cuentas_de_banco.id"), nullable=True) 

    importe = db.Column(db.Float, nullable=False, default=0.00)
    notas = db.Column(db.Text)
    estatus = db.Column(db.String(100),nullable=False, default="Activo") # en revision,aprobado, pagado parcial, pagado

    proveedor = db.relationship('Proveedores', backref='gastos_recurrentes', lazy=True)
    categoria = db.relationship('CategoriasDeGastos', backref='gastos_recurrentes', lazy=True)
    cuenta_de_banco = db.relationship("CuentasDeBanco", backref="gastos_recurrentes", lazy=True)

    @validates('importe')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value

class PreciosDeProveedores(db.Model,BaseMixin,AuditMixin):
   
    id_proveedor = db.Column(db.UUID, db.ForeignKey("proveedores.id"), nullable=False)
    id_producto = db.Column(db.UUID, db.ForeignKey("productos.id"), nullable=False)
    
    precio_unitario = db.Column(db.Float, nullable=False)
    estatus = db.Column(db.String(255),default="Activo")

    proveedor = db.relationship("Proveedores", backref="precios_de_proveedores", lazy=True)
    producto = db.relationship("Productos", backref="precios_de_proveedores", lazy=True)

    @validates('precio_unitario')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value

class Compras(db.Model,BaseMixin,AuditMixin):

    id_almacen = db.Column(db.UUID, db.ForeignKey("almacenes.id"), nullable=False)
    id_proveedor = db.Column(db.UUID, db.ForeignKey("proveedores.id"), nullable=True)

    fecha_orden = db.Column(db.Date, nullable=False)
    fecha_entrega_estimada = db.Column(db.Date) 

    subtotal = db.Column(db.Float, nullable=False, default=0.00)
    costos_adicionales = db.Column(db.Float, default=0.00)
    descuentos = db.Column(db.Float, default=0.00)
    importe_total = db.Column(db.Float, nullable=False, default=0.00)
    notas = db.Column(db.Text)

    estatus = db.Column(db.String(255),default="En revisión") # e.g., En revisión, Aprobada, Recibida,Cancelada
    estatus_de_pago = db.Column(db.String(255),default="Sin pagar") # e.g., En revisión, Aprobada, Recibida,Cancelada

    almacen = db.relationship("Almacenes", backref="compras", lazy=True)
    proveedor = db.relationship("Proveedores", backref="compras", lazy=True)

class ProductosEnCompras(db.Model,BaseMixin,AuditMixin):

    id_compra = db.Column(db.UUID, db.ForeignKey("compras.id"), nullable=False) 
    id_producto = db.Column(db.UUID, db.ForeignKey("productos.id"), nullable=False) 

    cantidad_ordenada = db.Column(db.Float, nullable=False, default=0)
    cantidad_recibida = db.Column(db.Float, default=0)
    precio_unitario = db.Column(db.Float, nullable=False, default=0.00)
    subtotal = db.Column(db.Float, nullable=False, default=0.00)
    descuento_porcentaje = db.Column(db.Float, default=0.00)
    importe_total= db.Column(db.Float, default=0.00)
    fecha_entrega_estimada = db.Column(db.Date) 
    notas = db.Column(db.Text) 
    estatus = db.Column(db.String(255),default="Pendiente") # e.g., Pendiente, Recibido,Cancelado

    compra = db.relationship("Compras", backref="productos_en_compras", lazy=True)
    producto = db.relationship("Productos", backref="productos_en_compras", lazy=True)