# python/routes/settings.py

from flask import Blueprint, render_template,jsonify,request,redirect
from sqlalchemy import or_,and_,cast, String,func,text,extract
from python.models.modelos import *
from python.services.system.boto3_s3 import S3Service
from python.services.system.authentication import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
from python.services.system.extensions import csrf

s3_service = S3Service()

settings_bp = Blueprint("settings", __name__,url_prefix="/settings")


@settings_bp.route("/usuarios", methods=["GET","POST"])
@login_required
@roles_required()
def usuarios():
    context = {
        "breadcrumbs": [{"name":"Configuración","url":""},{"name":"Usuarios","url":""}]
    }    
    columns=['nombre','correo_electronico','estatus']
    return render_template("system/settings/usuarios.html",columns=columns,table_name='usuarios',**context)

@settings_bp.route("/sucursales", methods=["GET","POST"])
@login_required
@roles_required()
def sucursales():
    context = {
        "breadcrumbs": [{"name":"Configuración","url":""},{"name":"Sucursales","url":""}]
    }        
    columns=['nombre','direccion']
    return render_template("system/settings/sucursales.html",columns=columns,table_name='sucursales',**context)

