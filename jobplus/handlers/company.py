from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash, abort
from ..forms import BossForm
from jobplus.models import Company

company = Blueprint("company", __name__, url_prefix='/company')


@company.route("/")
def company_list():
    page = request.args.get("page", default=1, type=int)
    pagination = Company.query.paginate(
        page=page,
        per_page=current_app.config['COMPANY_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items  # 当前页数的记录列表
    return render_template('company/company_list.html', pagination=pagination, posts=posts)


@company.route("/<int:id>")
def company_detail(id):
    company = Company.query.filter_by(id=id).first()
    if company:
        return render_template('company/company_detail.html', company=company)
    else:
        abort(404)


@company.route("/profile/<int:id>", methods=["GET", "POST"])
def profile(id):
    form = BossForm()
    if form.validate_on_submit():
        form.complete(id)
        flash("信息填写成功", 'success')
        return redirect(url_for("front.index"))
    return render_template('company/profile.html', form=form, id=id)
