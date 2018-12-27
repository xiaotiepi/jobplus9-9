from flask import (Blueprint, request, render_template, url_for, flash, current_app, abort, redirect)
from ..models import Job
from flask_login import login_required, current_user
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
        return render_template('job/job_detail.html', job=job)
    else:
        abort(404)

