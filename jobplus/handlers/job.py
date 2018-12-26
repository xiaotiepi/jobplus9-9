from flask import Blueprint, render_template, request, current_app
<<<<<<< HEAD
from jobplus.models import Job
=======
from ..models import Job
>>>>>>> a1fa68e6590dca79d1e4aa85a6c5370657a8e1b6

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
<<<<<<< HEAD
    return render_template('job/job_list.html,', pagination=pagination, posts=posts)
=======
    return render_template('job/job_list.html', pagination=pagination, posts=posts)
>>>>>>> a1fa68e6590dca79d1e4aa85a6c5370657a8e1b6
