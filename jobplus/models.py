from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)


class User(BaseModel, UserMixin):
    __tablename__ = 'users'

    ROLE_USER = 10
    ROLE_BOSS = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # unique是否唯一，index索引
    username = db.Column(db.String(32), unique=True, index=True, )
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column(db.String(258), nullable=False)
    phone_number = db.Column(db.String(11), unique=True)
    work_year = db.Column(db.Integer)
    work_resume = db.column(db.LargeBinary)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id", ondelete="CASCADE"))
    company = db.relationship("Company", backref="user", uselist=False)  # 一个账号下有一个公司

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pwd):
        self._password = generate_password_hash(pwd)

    def check_pwd(self, pwd):
        return check_password_hash(self._password, pwd)

    @property
    def is_boss(self):
        return self.role == self.ROLE_BOSS

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN


class Company(BaseModel):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(64))  # 公司名字
    address = db.Column(db.String(256))  # 公司地址
    net_site = db.Column(db.String(64))  # 网站
    logo = db.Column(db.String(128))
    introduce = db.Column(db.String(256))  # 简介
    detail = db.Column(db.Text)  # 详情
    city = db.Column(db.String(128))  # city
    financing = db.Column(db.String(54))  # 融资
    company_field = db.Column(db.String(128))  # 领域
    company_scale = db.column(db.String(128))  # 规模大小

    def __repr__(self):
        return self.name




class Job(BaseModel):
    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_title = db.Column(db.String(128))  # 工作名字
    work_experience = db.Column(db.String(54))  # 工作经验要求
    study_experience = db.Column(db.String(54))  # 学历要求
    work_tags = db.Column(db.String(128))  # 职位标签
    salary_range = db.Column(db.String(54))  # 薪酬范围
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    company_msg = db.relationship("Company", backref="job")

    def __repr__(self):
        return self.job_title
    @property
    def tag_list(self):
        return self.work_tags.split(',')
