from flask import Blueprint, render_template, jsonify, request, Response, session
from sqlalchemy import or_, and_, cast, String, func, text
from python.models.modelos import *
from python.services.system.authentication import *

import io
from PIL import Image, ImageDraw, ImageFont
from python.services.dynamic_functions.forms import *
from python.services.dynamic_functions.tables import *
import traceback
from python.services.stripe import checkout_session

def api_basic_auth():
    auth = request.authorization
    if not auth:
        return {"message": "Missing Basic Auth credentials"}, False
    user = Usuarios.query.filter(Usuarios.correo_electronico == auth.username).first()
    if user and str(auth.password) == str(user.contrasena_api):
        return {"message": "Credenciales validas", "user": user}, True
    return {"message": "Credenciales no validas"}, False
