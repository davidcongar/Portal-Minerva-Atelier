
import uuid
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from python.models import db
from python.models.sistema import *

class Almacenes(db.Model,BaseMixin,AuditMixin):

    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(500), nullable=True)
    estatus = db.Column(db.String(255),default="Activo")

class CategoriasDeProductos(db.Model,BaseMixin,AuditMixin):
    nombre = db.Column(db.String(255), nullable=False)
    descripcion=db.Column(db.String(500), nullable=True)
    estatus = db.Column(db.String(255),default="Activo")

class Productos(db.Model,BaseMixin,AuditMixin):

    id_categoria_de_producto = db.Column(db.UUID, db.ForeignKey("categorias_de_productos.id"), nullable=False)

    nombre = db.Column(db.String(255), nullable=False)
    inventariable = db.Column(db.String(255), nullable=False)
    unidad_de_medida= db.Column(db.String(50), nullable=True) 
    descripcion=db.Column(db.String(500), nullable=True)
    estatus = db.Column(db.String(255),default="Activo")

    categoria = db.relationship("CategoriasDeProductos", backref="productos", lazy=True)

class Inventario(db.Model,BaseMixin,AuditMixin):
    
    id_almacen = db.Column(db.UUID, db.ForeignKey("almacenes.id"), nullable=False)
    id_producto = db.Column(db.UUID, db.ForeignKey("productos.id"), nullable=False)

    cantidad = db.Column(db.Float, nullable=False, default=0)
    cantidad_en_transito = db.Column(db.Float, nullable=False, default=0)

    almacen = db.relationship("Almacenes", backref="inventario", lazy=True)
    producto = db.relationship("Productos", backref="inventario", lazy=True)

class RecepcionesDeCompras(db.Model,BaseMixin,AuditMixin):

    id_almacen = db.Column(db.UUID, db.ForeignKey("almacenes.id"), nullable=False)
    id_compra = db.Column(db.UUID, db.ForeignKey("compras.id"), nullable=False) 

    fecha_entrega = db.Column(db.Date) 
    notas = db.Column(db.Text)
    estatus = db.Column(db.String(50),nullable=False, default="En revisión")

    almacen = db.relationship("Almacenes", backref="recepciones_de_compras", lazy=True)
    compras = db.relationship("Compras", backref="recepciones_de_compras", lazy=True)


class ProductosEnRecepcionesDeCompras(db.Model,BaseMixin,AuditMixin):

    id_recepcion_de_compra = db.Column(db.UUID, db.ForeignKey("recepciones_de_compras.id"), nullable=False) 
    id_producto = db.Column(db.UUID, db.ForeignKey("productos.id"), nullable=False) 

    cantidad = db.Column(db.Float, nullable=False, default=0)
    notas = db.Column(db.Text) 

    recepcion_de_compra = db.relationship("RecepcionesDeCompras", backref="productos_en_recepciones_de_compras", lazy=True)
    producto = db.relationship("Productos", backref="productos_en_recepciones_de_compras", lazy=True)


class AjustesDeInventario(db.Model,BaseMixin,AuditMixin):
    
    id_almacen = db.Column(db.UUID, db.ForeignKey("almacenes.id"), nullable=False)
    id_producto = db.Column(db.UUID, db.ForeignKey("productos.id"), nullable=False)

    fecha_de_ajuste = db.Column(db.Date)
    tipo_de_ajuste = db.Column(db.String(10),nullable=False, default="Entrada")
    cantidad = db.Column(db.Float, nullable=False, default=0)
    notas = db.Column(db.Text)
    estatus = db.Column(db.String(50),nullable=False, default="En revisión")

    almacen = db.relationship("Almacenes", backref="ajustes_de_inventario", lazy=True)
    producto = db.relationship("Productos", backref="ajustes_de_inventario", lazy=True)

    @validates('cantidad')
    def validate_non_negative(self, key, value):
        if float(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value


class TransferenciasDeInventario(db.Model,BaseMixin,AuditMixin):

    id_almacen_salida = db.Column(db.UUID, db.ForeignKey("almacenes.id"), nullable=False)
    id_almacen_entrada = db.Column(db.UUID, db.ForeignKey("almacenes.id"), nullable=False)

    fecha_de_transferencia= db.Column(db.Date)
    notas = db.Column(db.Text)
    estatus = db.Column(db.String(50),nullable=False, default="En revisión")

    almacen_salida = db.relationship("Almacenes",foreign_keys=[id_almacen_salida], backref="transferencias_de_inventario_salida", lazy="joined")
    almacen_entrada = db.relationship("Almacenes",foreign_keys=[id_almacen_entrada], backref="transferencias_de_inventario_entrada", lazy="joined")

class ProductosEnTransferenciasDeInventario(db.Model,BaseMixin,AuditMixin):
    
    id_transferencia_de_inventario = db.Column(db.UUID, db.ForeignKey("transferencias_de_inventario.id"), nullable=False)
    id_producto = db.Column(db.UUID, db.ForeignKey("productos.id"), nullable=False)

    cantidad = db.Column(db.Float, nullable=False, default=0)

    transferencia_de_inventario = db.relationship("TransferenciasDeInventario", backref="productos_en_transferencias_de_inventario", lazy="joined")
    producto = db.relationship("Productos", backref="productos_en_transferencias_de_inventario", lazy="joined")

    @validates('cantidad')
    def validate_non_negative(self, key, value):
        if float(value) < 0:
            raise ValueError(f"{key.replace('_',' ').capitalize()} no puede ser negativo")
        return value

class Envios(db.Model,BaseMixin,AuditMixin):

    id_almacen = db.Column(db.UUID, db.ForeignKey("almacenes.id"), nullable=False)
    id_cliente = db.Column(db.UUID, db.ForeignKey("clientes.id"), nullable=False) 
    id_proyecto = db.Column(db.UUID, db.ForeignKey("proyectos.id"), nullable=False) 
    id_proveedor = db.Column(db.UUID, db.ForeignKey("proveedores.id"), nullable=False) 

    guia_de_envio = db.Column(db.String(255), nullable=False)
    fecha_envio = db.Column(db.Date)
    notas = db.Column(db.Text)
    estatus = db.Column(db.String(50),nullable=False, default="En revisión")

    almacen = db.relationship("Almacenes", backref="envios", lazy=True)
    cliente = db.relationship("Clientes", backref="envios", lazy=True)
    proyecto = db.relationship("Proyectos", backref="envios", lazy=True)
    proveedor = db.relationship("Proveedores", backref="envios", lazy=True)


class ProductosEnEnvios(db.Model,BaseMixin,AuditMixin):

    id_envio = db.Column(db.UUID, db.ForeignKey("envios.id"), nullable=False) 
    id_producto = db.Column(db.UUID, db.ForeignKey("productos.id"), nullable=False) 

    cantidad = db.Column(db.Float, nullable=False, default=0)
    notas = db.Column(db.Text) 

    envio = db.relationship("Envios", backref="productos_en_envios", lazy=True)
    producto = db.relationship("Productos", backref="productos_en_envios", lazy=True)

