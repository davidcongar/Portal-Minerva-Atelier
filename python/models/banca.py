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
        if float(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value


class GastosYComprasEnPagos(db.Model,BaseMixin,AuditMixin):

    id_pago = db.Column(db.UUID, db.ForeignKey("pagos_administrativos.id"), nullable=True) 
    id_gasto = db.Column(db.UUID, db.ForeignKey("gastos.id"), nullable=True) 
    id_compra = db.Column(db.UUID, db.ForeignKey("compras.id"), nullable=True) 

    importe = db.Column(db.Float, nullable=False, default=0.00)
    notas = db.Column(db.Text)

    pago = db.relationship("PagosAdministrativos", backref="gastos_y_compras_en_pagos", lazy=True)
    gasto = db.relationship("Gastos", backref="gastos_y_compras_en_pagos", lazy=True)
    compra = db.relationship("Compras", backref="gastos_y_compras_en_pagos", lazy=True)

    @validates('importe')
    def validate_non_negative(self, key, value):
        if float(value) < 0:
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
        if float(value) < 0:
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
        if float(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value
class PagosDeNomina(db.Model,BaseMixin,AuditMixin):

    id_cuenta_de_banco = db.Column(db.UUID, db.ForeignKey("cuentas_de_banco.id"), nullable=False)

    fecha = db.Column(db.Date, nullable=True)
    importe_total = db.Column(db.Float, nullable=False, default=0.00)
    notas = db.Column(db.Text) 
    estatus = db.Column(db.String(50), default="En revisión")

    cuenta_de_banco = db.relationship("CuentasDeBanco", backref="pagos_de_nomina", lazy=True)

class SueldosPagadosEnNomina(db.Model,BaseMixin,AuditMixin):

    id_pago_de_nomina = db.Column(db.UUID, db.ForeignKey("pagos_de_nomina.id"), nullable=False)
    id_integrante = db.Column(db.UUID, db.ForeignKey("integrantes.id"), nullable=False)
    importe = db.Column(db.Float, nullable=False)
    importe_ajuste=db.Column(db.Float,nullable=False, default=0)
    importe_total=db.Column(db.Float,nullable=False, default=0)
    notas = db.Column(db.Text) 

    pago_de_nomina = db.relationship("PagosDeNomina", backref="sueldos_pagados_en_nomina", lazy=True)
    integrante = db.relationship("Integrantes", backref="sueldos_pagados_en_nomina", lazy=True)

    @validates('importe')
    def validate_non_negative(self, key, value):
        if float(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value