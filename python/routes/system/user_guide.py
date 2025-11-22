# python/routes/user_guide.py

from flask import Blueprint, render_template,jsonify,request,redirect
from sqlalchemy import or_,and_,cast, String,func,text,extract
from python.models.modelos import *
from python.services.system.boto3_s3 import S3Service
from python.services.system.authentication import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
from python.services.system.extensions import csrf

s3_service = S3Service()

user_guide_bp = Blueprint("user_guide", __name__,url_prefix="/user_guide")


@user_guide_bp.route("/", methods=["GET","POST"])
@login_required
@roles_required()
def guide():
    context = {
        "breadcrumbs": [{"name":"Guía de usuario","url":""}]
    }    
    return render_template("system/user_guide/main.html",**context)
