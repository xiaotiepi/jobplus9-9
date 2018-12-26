from flask import (Blueprint, render_template, redirect,
<<<<<<< HEAD
                   url_for, flash, request)
from jobplus.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required
from jobplus.models import User, Company
=======
                   url_for, flash, request, abort, current_app)
from jobplus.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required
from ..models import User, Company, Job
>>>>>>> a1fa68e6590dca79d1e4aa85a6c5370657a8e1b6

front = Blueprint("front", __name__)


@front.route("/")
def index():
    commpanys = Company.query.limit(current_app.config['COMPANY_PER_PAGE'])
    jobs = Job.query.limit(current_app.config['JOB_PER_PAGE'])
    data = {
        'companys': commpanys,
        'jobs': jobs
    }
    return render_template('index.html', **data)


@front.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
<<<<<<< HEAD
        login_user(user, form.remember_me.data)
        if user.is_admin:
            pass
        elif user.is_boss:
            if not Company.query.filter_by(email=form.email.data).first():
                return redirect(url_for('company.profile', id=user.id))
            else:
                return redirect(url_for('.index'))
        else:
            if not User.query.filter_by(email=form.email.data).first().username:
                return redirect(url_for('user.profile', id=user.id))
=======
        if user.is_banned:
            flash("该用户已被禁止登录", 'error')
            redirect(url_for('front.login'))
        else:
            login_user(user, form.remember_me.data)
            if user.is_admin:
                return redirect(url_for('admin.index'))
            elif user.is_boss:
                if not User.query.filter_by(email=form.email.data).first().company_id:
                    return redirect(url_for('company.profile', id=user.id))
                else:
                    return redirect(url_for('.index'))
>>>>>>> a1fa68e6590dca79d1e4aa85a6c5370657a8e1b6
            else:
                if not User.query.filter_by(email=form.email.data).first().phone_number:
                    return redirect(url_for('user.profile', id=user.id))
                else:
                    return redirect(url_for('.index'))
            flash("您的邮箱或密码输入错误,请重新输入", "error")
    return render_template('login.html', form=form)


@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录', 'success')
    return redirect(url_for('.index'))


<<<<<<< HEAD
@front.route("/register/boss", methods=["GET", "POST"])
def register_boss():
    form = RegisterForm()
=======
@front.route("/companyregister", methods=["GET", "POST"])
def register_boss():
    form = RegisterForm()
    form.username.label = "企业名称"
>>>>>>> a1fa68e6590dca79d1e4aa85a6c5370657a8e1b6
    if form.validate_on_submit():
        form.create_boss()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('company_register.html', form=form)


<<<<<<< HEAD

@front.route("/register/user", methods=["GET", "POST"])
=======
@front.route("/userregister", methods=["GET", "POST"])
>>>>>>> a1fa68e6590dca79d1e4aa85a6c5370657a8e1b6
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
<<<<<<< HEAD
    return render_template('register_user.html', form=form)
=======
    return render_template('user_register.html', form=form)
>>>>>>> a1fa68e6590dca79d1e4aa85a6c5370657a8e1b6
