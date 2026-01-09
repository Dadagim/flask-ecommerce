from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user


views = Blueprint("views",__name__, url_prefix="/views")






@views.route("/")
def home():
    return render_template("home.html", current_user=current_user)