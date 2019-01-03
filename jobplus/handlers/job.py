from flask import (Blueprint, request, render_template, url_for, flash, current_app, abort, redirect, session)
from ..models import Job, Delivery, db, User
from flask_login import login_required, current_user
from jobplus.decorators import role_required
from jobplus.forms import JobForm

job = Blueprint("job", __name__, url_prefix='/job')


@job.route("/")
def job_list():
    page = request.args.get("page", default=1, type=int)
    pagination = Job.query.order_by(Job.create_at.desc()).paginate(
        page=page,
        per_page=current_app.config['JOB_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items  # 当前页数的记录列表
    return render_template('job/job_list.html', pagination=pagination, posts=posts)


@job.route("/<int:id>")
def job_detail(id):
    job = Job.query.filter_by(id=id).first()
    if job:
        if Delivery.query.filter_by(user_id=current_user.id, job_id=id).first():
            return render_template('job/job_detail.html', job=job, state=False)
        else:
            return render_template('job/job_detail.html', job=job, state=True)
    else:
        abort(404)


@login_required
@job.route('/<int:job_id>/apply')
def apply(job_id):
    if Delivery.query.filter_by(user_id=current_user.id, job_id=job_id).first():
        flash("您已经投递过该工作的简历", 'info')
        return redirect(url_for('.job_detail', id=job_id))
    else:
        db.session.add(Delivery(user=current_user, job=Job.query.filter_by(id=job_id).first(),
                                company=Job.query.filter_by(id=job_id).first().company_msg))
        db.session.commit()
        flash('简历投递成功', 'success')
        return redirect(url_for('.job_detail', id=job_id))


@role_required(role=20)
@job.route('/admin')
def admin():
    session['page'] = page = request.args.get("page", default=1, type=int)
    pagination = Job.query.filter_by(company_msg=User.query.filter_by(id=current_user.id).first().company).paginate(
        page=page,
        per_page=current_app.config['JOB_PER_PAGE'],
        error_out=False
    )
    return render_template('job/admin.html', pagination=pagination)


@role_required(role=20)
@job.route('/new', methods=['GET', 'POST'])
def add_job():
    form = JobForm()
    del form.company_name
    if form.validate_on_submit():
        form.create_job(User.query.filter_by(id=current_user.id).first().company.id)
        return redirect(url_for('job.admin'))
    return render_template('job/add_job.html', form=form)


@job.route('/edit/<int:id>', methods=["GET", "POST"])
def edit_job(id):
    job = Job.query.get_or_404(id)
    form = JobForm(obj=job)
    del form.company_name
    if form.validate_on_submit():
        form.update_job(job)
        flash('职位信息修改成功', 'success')
        return redirect(url_for('job.admin', page=session.get('page')))
    return render_template('job/edit_job.html', form=form, job=job)


@role_required(role=20)
@job.route('/<int:id>/delete')
def delete_job(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    flash('职位 "{}" 删除成功'.format(job.job_title), 'success')
    return redirect(url_for('job.admin', page=session.get('job_page')))


@job.route("/ban/<int:id>")
def ban_job(id):
    job = Job.query.filter_by(id=id).first()
    job.is_banned = not job.is_banned
    db.session.add(job)
    db.session.commit()
    return redirect(url_for('job.admin', page=session.get('page')))


@job.route("/apply/todolist")
def todo():
    session['todo_page'] = page = request.args.get("page", default=1, type=int)
    pagination = Delivery.query.filter_by(company=current_user.company, undisposed=True, interview=False).paginate(
        page=page,
        per_page=current_app.config['JOB_PER_PAGE'],
        error_out=False
    )
    return render_template('job/todolist.html', pagination=pagination)


@job.route('/apply/rejectlist')
def rejectlist():
    session['reject_page'] = page = request.args.get("page", default=1, type=int)
    pagination = Delivery.query.filter_by(company=current_user.company, undisposed=False).paginate(
        page=page,
        per_page=current_app.config['JOB_PER_PAGE'],
        error_out=False
    )
    return render_template('job/rejectlist.html', pagination=pagination)


@job.route('/apply/interview')
def interview():
    session['inter_page'] = page = request.args.get("page", default=1, type=int)
    pagination = Delivery.query.filter_by(company=current_user.company, interview=True).paginate(
        page=page,
        per_page=current_app.config['JOB_PER_PAGE'],
        error_out=False
    )
    return render_template('job/interview.html', pagination=pagination)


@job.route('/apply/reject/<int:id>')
def reject(id):
    delivery = Delivery.query.filter_by(id=id).first()
    delivery.undisposed = False
    db.session.add(delivery)
    db.session.commit()
    return redirect(url_for('job.todo', page=session.get('todo_page')))


@job.route('/apply/interview/<int:id>')
def inter(id):
    delivery = Delivery.query.filter_by(id=id).first()
    delivery.interview = True
    db.session.add(delivery)
    db.session.commit()
    return redirect(url_for('job.todo', page=session.get('todo_page')))
