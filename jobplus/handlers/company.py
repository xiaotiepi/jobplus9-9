from flask import Blueprint

company = Blueprint("company", __name__, url_prefix='/company')


@company.route("/")
def index():
    return "公司信息"