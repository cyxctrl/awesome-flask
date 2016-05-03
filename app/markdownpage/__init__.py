from flask import Blueprint

markdownpage = Blueprint('markdownpage',__name__)

from . import views