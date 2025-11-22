# python/routes/automatizaciones.py

from flask import Blueprint, render_template,jsonify,request
from sqlalchemy import or_,and_,cast, String,func,text,extract
from python.models.modelos import *
from python.services.system.authentication import *
from datetime import datetime


dashboards_bp = Blueprint("dashboards", __name__,url_prefix="/dashboards")
@dashboards_bp.route("/operative_dashboard", methods=["GET","POST"])
@login_required
def operative_dashboard():
    data = {'activeMenu': 'inicio'}
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    date_range = f'{start_of_week} to {end_of_week}'
    return render_template('main/dashboards/operative/pagina_principal.html', **data,date_range=date_range)
