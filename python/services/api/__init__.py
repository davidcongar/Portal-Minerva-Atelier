# api/__init__.py
from flask import Blueprint

api_bp = Blueprint("api", __name__, url_prefix="/api")

# Optional: expose it for easy import
from python.services.api.adquisicion import *
from python.services.api.ventas import *
from python.services.api.proyectos import *
