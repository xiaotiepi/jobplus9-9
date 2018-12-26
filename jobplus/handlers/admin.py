from flask import Blueprint, render_template, url_for, redirect, request, current_app, flash
from flask_login import current_user
from jobplus.models import User, db,Company
from jobplus.forms import AddBoss, AddUser,EditBoss,EditUser

admin = Blueprint("admin", __name__, url_prefix='/admin')


@admin.before_request
def before_request():
    if not current_user.is_authenticated or current_user.role < 30:
        return redirect(url_for("front.index"))


@admin.route("/")
def index():
    return render_template("admin/admin_base.html")


@admin.route("/users/boss")
def users_boss():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.filter_by(role=20).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/users_boss.html', pagination=pagination)


@admin.route("/users/user")
def user_user():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.filter_by(role=10).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/users_user.html', pagination=pagination)


@admin.route("/ban/<int:id>")
def ban_user(id):
    user = User.query.filter_by(id=id).first()
    user.is_banned = not user.is_banned
    db.session.add(user)
    db.session.commit()
    if user.is_boss:
        return redirect(url_for('admin.users_boss'))
    else:
        return redirect(url_for('admin.user_user'))


@admin.route('/users/adduser', methods=["GET", "POST"])
def add_user():
    form = AddUser()
    if form.validate_on_submit():
        form.create_user()
        return redirect(url_for('admin.user_user'))
    return render_template('admin/add_user.html', form=form)


@admin.route('/users/addcompany', methods=["GET", "POST"])
def add_company():
    form = AddBoss()
    if form.validate_on_submit():
        form.create_boss()
        form.complate()
        return redirect(url_for('admin.users_boss'))
    return render_template('admin/add_boss.html', form=form)


@admin.route('/users/<int:id>/delete')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('用户 "{}" 删除成功'.format(user.username), 'success')
    if user.is_boss:
        return redirect(url_for('admin.users_boss'))
    else:
        return redirect(url_for('admin.user_user'))


@admin.route('/users/edituser/<int:id>', methods=["GET", "POST"])
def edit_user(id):
    user = User.query.get_or_404(id)
    form = EditUser(obj=user)
    if form.validate_on_submit():
        form.update_user(id)
        flash('用户信息修改成功', 'success')
        return redirect(url_for('admin.user_user'))
    return render_template('admin/edit_user.html', form=form, user=user)




@admin.route('/users/editcompany/<int:id>', methods=["GET", "POST"])
def edit_boss(id):
    user = User.query.get_or_404(id)
    form = EditBoss(obj=user)
    company=Company.query.get_or_404(user.company_id)
    form.username = user.username
    form.introduce.data=company.introduce
    form.net_site.data=company.net_site
    if form.validate_on_submit():
        form.complate()
        flash('公司信息修改成功', 'success')
        return redirect(url_for('admin.users_boss'))
    return render_template('admin/edit_boss.html', form=form, user=user)
