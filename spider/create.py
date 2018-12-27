import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from faker import Faker

# 记得更改成自己的数据库接口
DB_URI = 'mysql://xiaotiepi:12580@localhost:3306/plus_job?charset=utf8'
engine = create_engine(DB_URI)

Session = sessionmaker(bind=engine)
session = Session()
faker = Faker()


db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(BaseModel, UserMixin):
    __tablename__ = 'users'

    ROLE_USER = 10
    ROLE_BOSS = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # unique是否唯一，index索引
    username = db.Column(
        db.String(32),
        unique=True,
        index=True,
    )
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column(db.String(258), nullable=False)
    phone_number = db.Column(db.String(11), unique=True)
    work_year = db.Column(db.Integer)
    work_resume = db.column(db.LargeBinary)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    company_id = db.Column(db.Integer,
                           db.ForeignKey("company.id", ondelete="CASCADE"))
    company = db.relationship(
        "Company", backref="user", uselist=False)  # 一个账号下有一个公司
    is_banned = db.Column(db.Boolean, default=False)


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


def create_boss(company):
    user = User(username="boss", email='123456789@qq.com', password='123456', role=User.ROLE_BOSS)
    user.company = company
    return user


def item_jobs():
        with open("/home/xiaotiepi/jobplus9-9/spider/jobs.json", 'r', encoding="utf8") as f:
            jobs = json.load(f)
            print(jobs)
            job_list = []
            company_list = []
            for job in jobs:
                company = Company(name=job["company"],
                                  address=job["address"],
                                  net_site=job["net_site"],
                                  logo=job["logo"],
                                  introduce=faker.sentence(),
                                  detail=job["desc"],
                                  city=job["city"],
                                  financing=job["financing"],
                                  company_field=job["company_field"],
                                  company_scale=job['company_scale']
                                  )
                jobdata = Job(job_title=job['job_title'],
                              work_experience=job['work_experience'],
                              study_experience=job['study_experience'],
                              salary_range=job['xinshui'],
                              work_tags=job['work_tags'],
                              company_msg=company)
                job_list.append(jobdata)
                company_list.append(company)

            return job_list, company_list


def main():
    jobs, companys = item_jobs()
    user = create_boss(companys[0])
    session.add(user)
    for job in jobs:
        session.add(job)
    for com in companys:
        session.add(com)
    try:
        session.commit()
        print("数据生成完成")
    except Exception as e:
        print(e.args)
        print("如果已经有boss账号了，生成数据时，请注释48,49行")
        session.rollback()


if __name__ == '__main__':
    main()