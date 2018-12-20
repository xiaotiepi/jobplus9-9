import json
from jobplus.models import User, Company, Job, db
from jobplus import create_app
from faker import Faker

app = create_app("development")
app.app_context().push()
faker = Faker()

# 生成一个用户boss
def create_boss(company):
    user = User(username="boss", email='123456789@qq.com', password='123456', role=User.ROLE_BOSS)
    user.company = company
    return user

def item_jobs():
        with open("jobs.json", 'r', encoding="utf8") as f:
            jobs = json.load(f)
            print(jobs)
            job_list=[]
            company_list=[]
            for job in jobs:
                company = Company(name=job["company"]
                                  , address=job["address"],
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
                              work_tags=job['work_tags']
                              ,company_msg=company)
                job_list.append(jobdata)
                company_list.append(company)

            return job_list, company_list


def main():
    jobs, companys = item_jobs()
    user = create_boss(companys[0])
    db.session.add(user)
    for job in jobs:
        db.session.add(job)
    for com in companys:
        db.session.add(com)
    try:
        db.session.commit()
        print("数据生成完成")
    except Exception as e:
        print(e.args)
        print("如果已经有boss账号了，生成数据时，请注释48,49行")
        db.session.rollback()


if __name__ == '__main__':
    main()
