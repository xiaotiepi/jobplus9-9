<<<<<<< HEAD
from flask import Blueprint, render_template
from jobplus.models import User
=======
from flask import Blueprint, render_template,redirect,url_for,flash
from ..models import User
>>>>>>> a1fa68e6590dca79d1e4aa85a6c5370657a8e1b6
from ..forms import UserForm
user = Blueprint("user", __name__, url_prefix='/user')


@user.route("/")
def index():
    return "用户信息"


@user.route("/profile/<int:id>",methods=["GET", "POST"])
def profile(id):
    form = UserForm()
    if form.validate_on_submit():
<<<<<<< HEAD
        # TODO 实现上传文件功能
        # print(form.work_resume.data)
        # filename = 'jobplus/resume' + form.work_resume.data
        # form.work_resume.data.save(filename)
        # form.work_resume.data=filename
        form.complete(id)
=======
        form.complete(id)
        flash("个人信息填写成功","success")
        return redirect(url_for("front.index"))
>>>>>>> a1fa68e6590dca79d1e4aa85a6c5370657a8e1b6
    return render_template('user/profile.html', form=form, id=id)
