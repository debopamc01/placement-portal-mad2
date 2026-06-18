from flask import Blueprint, render_template


frontend_bp = Blueprint(name="frontend", import_name=__name__)

@frontend_bp.route("/")
def index():
    return render_template("index.html")