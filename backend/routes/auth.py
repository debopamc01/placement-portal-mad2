
from flask import (
    Blueprint,
    render_template,
)

from backend.utils.responses import *

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    return render_template("pages/index.html")
