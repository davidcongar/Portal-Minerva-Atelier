import uuid
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from python.models import db
from python.models.sistema import *
 
class Servicios(db.Model,BaseMixin,AuditMixin):

    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    estatus = db.Column(db.String(255),default="Activo")

class PreciosDeServicios(db.Model,BaseMixin,AuditMixin):

    id_servicio = db.Column(db.UUID, db.ForeignKey("servicios.id"), nullable=False)

    precio_unitario = db.Column(db.Float, nullable=False)
    estatus = db.Column(db.String(255),default="Activo")

    @validates('precio_unitario')
    def validate_non_negative(self, key, value):
        if float(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value

class Ventas(db.Model,BaseMixin,AuditMixin):

    id_servicio=db.Column(db.UUID, db.ForeignKey("servicios.id"),nullable=False)
    id_cliente = db.Column(db.UUID, db.ForeignKey("clientes.id"),nullable=False)
    id_cuenta_de_banco = db.Column(db.UUID, db.ForeignKey("cuentas_de_banco.id"))

    id_stripe = db.Column(db.String(255))
    espacio_de_proyecto = db.Column(db.String(255))
    importe = db.Column(db.Float, nullable=False, default=0.00)
    tipo_de_iva = db.Column(db.String(255))
    iva = db.Column(db.Float, default=0.00)
    importe_total = db.Column(db.Float, default=0.00)

    estatus = db.Column(db.String(100),nullable=False, default="Pendiente")

    cliente = db.relationship('Clientes', backref='ventas',lazy=True)
    servicio = db.relationship('Servicios', backref='ventas', lazy=True)
    cuenta_de_banco = db.relationship('CuentasDeBanco', backref='ventas',lazy=True)

    @validates('importe','importe_cobrado')
    def validate_non_negative(self, key, value):
        if float(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value

class Facturas(db.Model,BaseMixin,AuditMixin):

    id_cliente = db.Column(db.UUID, db.ForeignKey("clientes.id"),nullable=False)
    id_venta = db.Column(db.UUID, db.ForeignKey("ventas.id"),nullable=False)
    uso_de_cfdi=db.Column(db.String(255))
    metodo_de_pago=db.Column(db.String(255))
    forma_de_pago=db.Column(db.String(255))

    folio_fiscal_uuid=db.Column(db.String(255))
    fecha_de_expedicion=db.Column(db.Date)
    subtotal=db.Column(db.Float, nullable=False, default=0.00)
    impuestos=db.Column(db.Float, nullable=False, default=0.00)
    importe_total = db.Column(db.Float, nullable=False, default=0.00)
    importe_cobrado = db.Column(db.Float, default=0.00)
    notas = db.Column(db.Text)

    estatus = db.Column(db.String(255),default="En revisión") # e.g., En revisión,Finalizado,Cancelado

    cliente = db.relationship('Clientes', backref='facturas', lazy=True)
    ventas = db.relationship('Ventas', backref='facturas', lazy=True)

    @validates('importe_total')
    def validate_non_negative(self, key, value):
        if float(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value
    
class ServiciosEnFacturas(db.Model,BaseMixin,AuditMixin):

    id_factura = db.Column(db.UUID, db.ForeignKey("facturas.id"),nullable=False)
    id_servicio = db.Column(db.UUID, db.ForeignKey("servicios.id"),nullable=False)
    cantidad=db.Column(db.Float, default=0.00)
    valor_unitario=db.Column(db.Float, default=0.00)
    impuesto=db.Column(db.Float, default=0.00)
    importe = db.Column(db.Float, nullable=False, default=0.00)
    notas = db.Column(db.Text)

    estatus = db.Column(db.String(255),default="En revisión") # e.g., En revisión,Finalizado,Cancelado

    factura = db.relationship('Facturas', backref='servicios_en_facturas', lazy=True)
    servicio = db.relationship('Servicios', backref='servicios_en_facturas', lazy=True)

    @validates('importe','impuesto')
    def validate_non_negative(self, key, value):
        if float(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value

class Cotizaciones(db.Model,BaseMixin,AuditMixin):

    id_cliente = db.Column(db.UUID, db.ForeignKey("clientes.id"),nullable=False)
    id_servicio = db.Column(db.UUID, db.ForeignKey("servicios.id"),nullable=False)

    fecha_de_cotizacion = db.Column(db.Date)
    descripcion = db.Column(db.Text)
    importe_total = db.Column(db.Float, nullable=False, default=0.00)
    estatus = db.Column(db.String(100),nullable=False, default="En revisión") # en revision,aprobado, pagado parcial, pagado

    cliente = db.relationship('Clientes', backref='cotizaciones', lazy=True)
    servicio = db.relationship('Servicios', backref='cotizaciones',lazy=True)

    @validates('importe_total')
    def validate_non_negative(self, key, value):
        if float(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value
    
class DetalleDeCotizaciones(db.Model,BaseMixin,AuditMixin):

    id_cotizacion = db.Column(db.UUID, db.ForeignKey("cotizaciones.id"),nullable=False)

    descripcion = db.Column(db.Text)
    precio_unitario = db.Column(db.Float, nullable=False, default=0.00)
    cantidad = db.Column(db.Float, nullable=False, default=0.00)

    cotizacion = db.relationship('Cotizaciones', backref='detalle_de_cotizaciones', lazy=True)

    @validates('precio_unitario','cantidad')
    def validate_non_negative(self, key, value):
        if float(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value