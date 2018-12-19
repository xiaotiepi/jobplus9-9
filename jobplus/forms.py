from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError,IntegerField,FileField
from wtforms.validators import Length, Email, Required,EqualTo,URL
from jobplus.models import db, User,Company


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱未注册')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_pwd(field.data):
            raise ValidationError('密码错误')


class RegisterForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已经被注册')

    def create_user(self):
        user = User(email=self.email.data,password=self.password.data)
        db.session.add(user)
        db.session.commit()

    def create_boss(self):
        user = User(email=self.email.data, password=self.password.data,role=20)
        db.session.add(user)
        db.session.commit()

class UserForm(FlaskForm):
    username=StringField('用户名',validators=[Required(),Length(3, 24)])
    phone_number=IntegerField('手机号',validators=[Required()])
    work_year=IntegerField("工作经验",validators=[Required()])
    work_resume = FileField('简历',validators=[Required()])
    company=StringField('公司')
    submit=SubmitField('提交')


class BossForm(FlaskForm):
    email=StringField('邮箱',validators=[Required(),Email()])
    name = StringField('企业名称',validators=[Required(),Length(3,50)])
    address=StringField('公司地址',validators=[Required()])
    net_site=StringField('网站链接',validators=[Required(),URL()])
    logo=StringField("logo图片链接",validators=[Required(),URL()])
    introduce=StringField("一句话简介",validators=[Required()])
    detail=StringField("详细介绍")
    financing=StringField("融资")
    company_field=StringField("领域")
    submit=SubmitField('提交')
