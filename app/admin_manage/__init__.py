from flask import Blueprint

admin_manage = Blueprint('admin_manage',__name__)

from . import views
