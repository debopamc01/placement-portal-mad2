from flask import Blueprint, render_template

frontend_bp = Blueprint(name="frontend", import_name=__name__)


@frontend_bp.route("/")
def index():
    # TODO: Remove this, static folder and templates folder
    return render_template("index.html")
