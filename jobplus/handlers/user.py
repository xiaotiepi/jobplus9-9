from flask import Blueprint, render_template
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
        # TODO 实现上传文件功能
        # print(form.work_resume.data)
        # filename = 'jobplus/resume' + form.work_resume.data
        # form.work_resume.data.save(filename)
        # form.work_resume.data=filename
        form.complete(id)
    return render_template('user/profile.html', form=form, id=id)
