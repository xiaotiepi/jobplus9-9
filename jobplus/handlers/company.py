from flask import Blueprint,redirect,url_for,render_template
from ..forms import BossForm
company = Blueprint("company", __name__, url_prefix='/company')


@company.route("/")
def index():
    return "公司信息"

@company.route("/profile",methods=["GET","POST"])
def profile():
    form=BossForm()
    return render_template('company/profile.html', form=form)