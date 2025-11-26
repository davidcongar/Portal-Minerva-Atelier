import uuid
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from python.models import db
from python.models.sistema import *

class CuentasDeBanco(db.Model,BaseMixin,AuditMixin):

    id_integrante = db.Column(db.UUID, db.ForeignKey("integrantes.id"), nullable=True)

    banco = db.Column(db.String(100),nullable=False)
    tipo_de_cuenta = db.Column(db.String(100),nullable=False)
    nombre = db.Column(db.String(100),nullable=False)
    numero_de_cuenta = db.Column(EncryptedColumn(255),nullable=True)
    clabe = db.Column(EncryptedColumn(255),nullable=True)
    balance = db.Column(db.Float, nullable=False, default=0)
    estatus = db.Column(db.String(255),default="Activo")

    integrante = db.relationship("Integrantes", backref="cuentas_de_banco", lazy=True)


class PagosAdministrativos(db.Model,BaseMixin,AuditMixin):

    id_proveedor = db.Column(db.UUID, db.ForeignKey("proveedores.id"), nullable=True)
    id_cuenta_de_banco = db.Column(db.UUID, db.ForeignKey("cuentas_de_banco.id"), nullable=True) 

    fecha_pago = db.Column(db.Date, nullable=False)
    importe = db.Column(db.Float, nullable=False, default=0.00)
    notas = db.Column(db.Text)

    estatus = db.Column(db.String(255),default="En revisión") # e.g., En revisión, Aprobado, Pagado,Cancelado

    proveedor = db.relationship("Proveedores", backref="pagos", lazy=True)
    cuenta_de_banco = db.relationship("CuentasDeBanco", backref="pagos", lazy=True)
    

    @validates('importe')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value


class GastosyComprasEnPagos(db.Model,BaseMixin,AuditMixin):

    id_pago = db.Column(db.UUID, db.ForeignKey("pagos.id"), nullable=True) 
    id_gasto = db.Column(db.UUID, db.ForeignKey("gastos.id"), nullable=True) 
    id_compra = db.Column(db.UUID, db.ForeignKey("compras.id"), nullable=True) 

    importe = db.Column(db.Float, nullable=False, default=0.00)
    notas = db.Column(db.Text)

    pago = db.relationship("Pagos", backref="gastos_y_compras_en_pagos", lazy=True)
    gasto = db.relationship("Gastos", backref="gastos_y_compras_en_pagos", lazy=True)
    compra = db.relationship("Compras", backref="gastos_y_compras_en_pagos", lazy=True)

    @validates('importe')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value

class TransferenciasDeDinero(db.Model,BaseMixin,AuditMixin):

    id_cuenta_de_banco_salida = db.Column(db.UUID, db.ForeignKey("cuentas_de_banco.id"), nullable=False)
    id_cuenta_de_banco_entrada = db.Column(db.UUID, db.ForeignKey("cuentas_de_banco.id"), nullable=False)

    fecha_de_transferencia= db.Column(db.Date)
    importe = db.Column(db.Float, nullable=False, default=0.00)
    notas = db.Column(db.Text)
    estatus = db.Column(db.String(50),nullable=False, default="En revisión")

    cuenta_de_banco_salida = db.relationship("CuentasDeBanco",foreign_keys=[id_cuenta_de_banco_salida], backref="transferencias_de_dinero_salida", lazy="joined")
    cuenta_de_banco_entrada = db.relationship("CuentasDeBanco",foreign_keys=[id_cuenta_de_banco_entrada], backref="transferencias_de_dinero_entrada", lazy="joined")

    @validates('importe')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value


class AjustesDeDinero(db.Model,BaseMixin,AuditMixin):

    id_cuenta_de_banco = db.Column(db.UUID, db.ForeignKey("cuentas_de_banco.id"), nullable=False)

    fecha_de_ajuste = db.Column(db.Date)
    tipo_de_ajuste = db.Column(db.String(10),nullable=False, default="Entrada")
    importe = db.Column(db.Float, nullable=False, default=0.00)
    notas = db.Column(db.Text)
    estatus = db.Column(db.String(50),nullable=False, default="En revisión")

    cuenta_de_banco = db.relationship("CuentasDeBanco", backref="ajustes_de_dinero", lazy=True)

    @validates('importe')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value

class Ingresos(db.Model,BaseMixin,AuditMixin):

    id_cliente = db.Column(db.UUID, db.ForeignKey("clientes.id"), nullable=False) 
    id_cuenta_de_banco = db.Column(db.UUID, db.ForeignKey("cuentas_de_banco.id"), nullable=False) 

    forma_de_pago=db.Column(db.String(255))
    folio_fiscal_uuid=db.Column(db.String(255))
    fecha_de_expedicion=db.Column(db.Date)

    importe = db.Column(db.Float, nullable=False, default=0.00)
    notas = db.Column(db.Text)
    estatus = db.Column(db.String(255),default="En revisión") # e.g., En revisión,Finalizado,Cancelado

    cliente = db.relationship("Clientes", backref="ingresos", lazy=True)
    cuenta_de_banco = db.relationship("CuentasDeBanco", backref="ingresos", lazy=True)

    @validates('importe')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value

class FacturasEnIngresos(db.Model,BaseMixin,AuditMixin):

    id_ingreso = db.Column(db.UUID, db.ForeignKey("ingresos.id"), nullable=False) 
    id_factura = db.Column(db.UUID, db.ForeignKey("facturas.id"), nullable=True) 

    importe = db.Column(db.Float, nullable=False, default=0.00)
    notas = db.Column(db.Text)

    factura = db.relationship("Facturas", backref="facturas_en_ingresos", lazy=True)
    ingreso = db.relationship("Ingresos", backref="facturas_en_ingresos", lazy=True)

    @validates('importe')
    def validate_non_negative(self, key, value):
        if Decimal(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value