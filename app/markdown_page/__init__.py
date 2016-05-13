from flask import Blueprint

markdown_page = Blueprint('markdown_page',__name__)

from . import views