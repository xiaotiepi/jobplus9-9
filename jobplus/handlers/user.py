from flask import Blueprint, render_template,redirect,url_for,flash
from ..models import User
from ..forms import UserForm
user = Blueprint("user", __name__, url_prefix='/user')


@user.route("/")
def index():
    return "用户信息"


@user.route("/profile/<int:id>",methods=["GET", "POST"])
def profile(id):
    form = UserForm()
    if form.validate_on_submit():
        form.complete(id)
        flash("个人信息填写成功","success")
        return redirect(url_for("front.index"))
    return render_template('user/profile.html', form=form, id=id)
