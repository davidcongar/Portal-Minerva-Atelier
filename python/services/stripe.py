from python.models import db
from python.models.modelos import *
import stripe
import os
from dotenv import load_dotenv

load_dotenv()
#4242424242424242

DOMAIN = os.getenv('DOMAIN')
stripe.api_key = os.getenv('STRIPE_API_KEY')

def create_product(id):
    servicio = PreciosDeServicios.query.get(id)
    if servicio.id_stripe_producto is None:
        product = stripe.Product.create(
            name=f'{servicio.servicio.nombre} - {servicio.espacio.nombre}',
            description=f'{servicio.servicio.descripcion}',
        )
        servicio.id_stripe_producto = product.id
        db.session.commit()

def create_price(id):
    servicio = PreciosDeServicios.query.get(id)
    price = stripe.Price.create(
        unit_amount=int(servicio.precio_unitario * 100),
        currency='mxn',
        product=servicio.id_stripe_producto,
    )
    servicio.id_stripe_precio = price.id
    db.session.commit()

def modify_price(id):
    servicio = PreciosDeServicios.query.get(id)
    if servicio.id_stripe_precio:
        stripe.Price.modify(
            servicio.id_stripe_precio,
            active=False,
        )
    create_price(id)


def create_coupon(id):
    descuento = Descuentos.query.get(id)
    if descuento.tipo_de_descuento=='Importe':
        if descuento.id_servicio and descuento.id_espacio:
            product=PreciosDeServicios.query.filter_by(id_servicio=descuento.id_servicio,id_espacio=descuento.id_espacio).first()
            if product:
                coupon = stripe.Coupon.create(amount_off=int(descuento.valor*100),currency="mxn",duration="forever",applies_to={"products": [product.id_stripe_producto]})
        else:
            coupon = stripe.Coupon.create(amount_off=int(descuento.valor*100),currency="mxn",duration="forever")
    elif descuento.tipo_de_descuento=='Porcentaje':
        if descuento.id_servicio and descuento.id_espacio:
            product=PreciosDeServicios.query.filter_by(id_servicio=descuento.id_servicio,id_espacio=descuento.id_espacio).first()
            if product:
                coupon = stripe.Coupon.create(percent_off=descuento.valor,duration="forever",applies_to={"products": [product.id_stripe_producto]})
        else:
            coupon = stripe.Coupon.create(percent_off=descuento.valor,duration="forever")

    descuento.id_stripe = coupon.id
    db.session.commit()

def checkout_session(id):
    venta=Ventas.query.get(id)
    items=ServiciosEnVentas.query.filter_by(id_venta=id).all()
    line_items=[]
    for item in items:
        line_items.append({
            "price": item.id_stripe_precio,
            "quantity": int(item.cantidad)
        })
    descuento=Descuentos.query.filter_by(estatus='Activo',codigo_de_descuento=venta.codigo_de_descuento).first()
    descuentos=[]
    if descuento:
        descuentos=[{'coupon':descuento.id_stripe}]
    checkout_session = stripe.checkout.Session.create(
        line_items=line_items,
        discounts=descuentos,
        mode='payment',
        success_url=f"{DOMAIN}/ventas/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{DOMAIN}/ventas/cancelar",
        payment_intent_data={'metadata':{'id_venta':id}},
        metadata={"id_venta": id}
    )
    return checkout_session.url   
