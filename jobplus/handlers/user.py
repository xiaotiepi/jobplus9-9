from flask import Blueprint,render_template
from jobplus.models import User
from ..forms import UserForm
user = Blueprint("user", __name__, url_prefix='/user')


@user.route("/")
def index():
    return "用户信息"


@user.route("/profile",methods=["GET","POST"])
def profile():
    form=UserForm()
    return render_template('user/profile.html',form=form)
