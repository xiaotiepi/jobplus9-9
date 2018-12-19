from flask import Blueprint,redirect,url_for,render_template
from ..forms import BossForm
company = Blueprint("company", __name__, url_prefix='/company')


@company.route("/")
def index():
    return "公司信息"

@company.route("/profile/<int:id>",methods=["GET","POST"])
def profile(id):
    form=BossForm()
    if form.validate_on_submit():
        #TODO
        pass
    return render_template('company/profile.html', form=form,id=id)