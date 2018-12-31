from flask import Blueprint, render_template, url_for, redirect, request, current_app, flash, session
from flask_login import current_user
from jobplus.models import User, db, Company, Job
from jobplus.forms import AddBoss, AddUser, EditBoss, EditUser, JobForm

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
    session['user_boss']=page
    pagination = User.query.filter_by(role=20).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/users_boss.html', pagination=pagination)


@admin.route("/users/user")
def user_user():
    page = request.args.get('page', default=1, type=int)
    session['user_page'] = page
    pagination = User.query.filter_by(role=10).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/users_user.html', pagination=pagination)


@admin.route('/jobs')
def admin_jobs():
    page = request.args.get('page', default=1, type=int)
    session['job_page'] = page
    pagination = Job.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template("admin/admin_jobs.html", pagination=pagination)


@admin.route("/user/ban/<int:id>")
def ban_user(id):
    user = User.query.filter_by(id=id).first()
    user.is_banned = not user.is_banned
    db.session.add(user)
    db.session.commit()
    if user.is_boss:
        return redirect(url_for('admin.users_boss',page=session.get('user_boss')))
    else:
        return redirect(url_for('admin.user_user',page=session.get('user_page')))


@admin.route("/job/ban/<int:id>")
def ban_job(id):
    job = Job.query.filter_by(id=id).first()
    job.is_banned = not job.is_banned
    db.session.add(job)
    db.session.commit()
    return redirect(url_for('admin.admin_jobs'))


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


@admin.route('/users/addjob', methods=["GET", "POST"])
def add_job():
    # user = User.query.get_or_404(user_id)
    form = JobForm()
    if form.validate_on_submit():
        company_id = Company.query.filter(Company.name==form.company_name).first()
        form.create_job(company_id)
        return redirect(url_for('admin.admin_jobs'))
    return render_template('admin/add_job.html', form=form)


@admin.route('/users/<int:id>/delete')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('用户 "{}" 删除成功'.format(user.username), 'success')
    if user.is_boss:
        return redirect(url_for('admin.users_boss', page=session.get('user_boss')))
    else:
        return redirect(url_for('admin.user_user', page=session.get('user_page')))


@admin.route('/job/<int:id>/delete')
def delete_job(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    flash('职位 "{}" 删除成功'.format(job.job_title), 'success')
    return redirect(url_for('admin.admin_jobs', page=session.get('job_page')))


@admin.route('/users/edituser/<int:id>', methods=["GET", "POST"])
def edit_user(id):
    user = User.query.get_or_404(id)
    form = EditUser(obj=user)
    if form.validate_on_submit():
        form.update_user(id)
        flash('用户信息修改成功', 'success')
        return redirect(url_for('admin.user_user',page=session.get('user_page')))
    return render_template('admin/edit_user.html', form=form, user=user)


@admin.route('/users/editcompany/<int:id>', methods=["GET", "POST"])
def edit_boss(id):
    user = User.query.get_or_404(id)
    form = EditBoss(obj=user)
    company = Company.query.get_or_404(user.company_id)
    form.username = user.username
    form.introduce.data = company.introduce
    form.net_site.data = company.net_site
    if form.validate_on_submit():
        form.complate()
        flash('公司信息修改成功', 'success')
        return redirect(url_for('admin.users_boss',page=session.get('user_boss')))
    return render_template('admin/edit_boss.html', form=form, user=user)


@admin.route('/job/<int:id>/edit', methods=["GET", "POST"])
def edit_job(id):
    job = Job.query.get_or_404(id)
    form = JobForm(obj=job)
    # company = Company.query.get_or_404(job.company_id)
    # form.job_title = job.job_title
    # form.introduce.data = company.introduce
    # form.net_site.data = company.net_site
    if form.validate_on_submit():
        form.update_job(job)
        flash('职位信息修改成功', 'success')
        return redirect(url_for('admin.admin_jobs'), page=session.get('job_page'))
    return render_template('admin/edit_jobs.html', form=form, job=job)
