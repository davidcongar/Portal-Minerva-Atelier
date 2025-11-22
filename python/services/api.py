# python/routes/home.py

from flask import Blueprint, render_template, jsonify, request, Response, session
from sqlalchemy import or_, and_, cast, String, func, text
from python.models.modelos import *
from python.services.system.authentication import *

import io
from PIL import Image, ImageDraw, ImageFont
from python.services.dynamic_routes_functions import *
import traceback

api_bp = Blueprint("api", __name__, url_prefix="/api")
def api_login(json_data):
    id_usuario = json_data['id_usuario']
    contrasena = json_data['contrasena']
    user = Usuarios.query.filter(Usuarios.id==id_usuario).first()
    if user!=None:
        if contrasena==user.contrasena_api:
            data={'message':'Credenciales validas'}
        else:
            data={'message':'Credenciales no validas'}
    else:
        data={'message':'Credenciales no validas'}
    return data  # Redirect back to the form

@api_bp.route("/user_image", methods=["GET"])
@login_required
def user_image():
    """Genera una imagen con la inicial del nombre del usuario actual y la letra centrada."""
    # Configuración de la imagen
    width, height = 100, 100
    bg_color = (52, 152, 219)  # Azul
    text_color = (255, 255, 255)  # Blanco
    font_size = 55

    user_name = session.get("nombre", None)
    if user_name:
        initial = user_name.strip()[0].upper()
    else:
        initial = "?"

    # Crear la imagen
    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    # Cargar la fuente
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), initial, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # centrar letra
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    # Dibujar letra
    draw.text((text_x, text_y), initial, fill=text_color, font=font, anchor="lt")

    # Guardar imagen en buffer
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return Response(buffer, mimetype="image/png")

@api_bp.route('/<table_name>',methods=['GET', 'POST'])
def dynamic_data(table_name):
    json_data = request.json
    auth=api_login(json_data)
    if auth['message']=='Credenciales validas':
        model = get_model_by_name(table_name)
        if not model:
            data={'message':'La tabla no existe.'}
            return data
        data = [item.to_dict() for item in model.query.all()]
        return jsonify(data)
    else:
        data={'message':'Credenciales no validas'}
        return data
