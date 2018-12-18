from flask import (Blueprint)

job = Blueprint("job", __name__, url_prefix='/job')


@job.route("/")
def index():
    return "职位信息"