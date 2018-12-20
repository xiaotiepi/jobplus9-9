from flask import json
from selenium import webdriver

import time
from lxml import etree

"""
流程：1.打开当前页，获取每个链接。循环获取每个链接中的详情内容
2.完毕之后，点击下一页，重复1
"""


class LanGou(object):
    def __init__(self):
        self.jobs = []
        self.broswer = webdriver.Chrome()
        self.broswer.implicitly_wait(20)
        # 该地址就是网址实际地址，不用在network寻找
        self.url = "https://www.lagou.com/zhaopin/"

    def run(self):
        # 循环遍历每一页，最好睡几秒
        self.broswer.get(self.url)
        try:
            while True:
                # page_source相当于源代码啦
                source = self.broswer.page_source
                self.parse_one_page(source)
                # 上面是爬取完一页
                # 进行下一页,翻页
                # 第三部，请求完第一页，进入第二页，知道不能点击
                next_page_btn = self.broswer.find_element_by_xpath("//div[@class='pager_container']/a[last()]")
                if "page_no pager_next_disabled" in next_page_btn.get_attribute("class"):
                    with open("jobs.json", 'w', newline="\n", encoding="utf-8") as f:
                        f.write(json.dumps(self.jobs))
                    break
                else:
                    print("下一页")
                    next_page_btn.click()
                time.sleep(2)
        except :
            with open("jobs.json", 'w', newline="\n", encoding="utf-8") as f:
                f.write(json.dumps(self.jobs, ensure_ascii=False))
            print("爬取中断")

    # 第一步，请求界面，
    def parse_one_page(self, sourse):
        htmlEle = etree.HTML(sourse)
        # 1页有多少个职位就有好多连接
        links = htmlEle.xpath("//a[@class='position_link']/@href")
        for detail_url in links:
            self.request_detail(detail_url)
            time.sleep(2)

    # 第二步，循环请求详情界面数据，窗口切换，关闭，切换到列表页
    def request_detail(self, url):
        # 需要打开新的界面，在详情页中没有下一页按钮
        # self.broswer.get(url=url)
        self.broswer.execute_script("window.open('{}')".format(url))
        self.broswer.switch_to.window(self.broswer.window_handles[1])
        source = self.broswer.page_source
        self.parse_detail(source)
        # 关闭当前详情页面,切换到列表页
        self.broswer.close()
        self.broswer.switch_to.window(self.broswer.window_handles[0])

    # 注意L使用显示等待，xpath解析，不需要写最后的text(),是获取不到的，一般解析需要text()
    def parse_detail(self, source):
        htmlEle = etree.HTML(source)
        compony = htmlEle.xpath("//dl[@class='job_company']/dt//h2/text()")[0].strip()
        logo = htmlEle.xpath("//dl[@class='job_company']/dt//a//img/@src")[0].strip()
        net_site = htmlEle.xpath("//ul[@class='c_feature']//a/@href")[0]
        # financingEnv=htmlEle.xpath("//dl[@id='job_company']//li")[1]
        # // *[ @ id = "job_company"] / dd / ul / li[3] / text()
        financing = htmlEle.xpath("//ul[@class='c_feature']//text()")[7]
        company_field = htmlEle.xpath("//ul[@class='c_feature']//text()")[2]
        company_scale=htmlEle.xpath("//ul[@class='c_feature']//text()")[12]
        xinshui = htmlEle.xpath("//span[@class='salary']/text()")[0]
        desc = "\n".join(htmlEle.xpath("//dd[@class='job_bt']//text()"))  # 获取该类下的所有段落的文本
        job_title = htmlEle.xpath("//div[@class='job-name']//span/text()")[0]
        city=htmlEle.xpath("//dd[@class='job_request']//span/text()")[1]
        work_experience = htmlEle.xpath("//dd[@class='job_request']//span/text()")[2]
        study_experience = htmlEle.xpath("//dd[@class='job_request']//span/text()")[3]
        work_tags = htmlEle.xpath("//dd[@class='job_request']//li/text()")
        address_one = htmlEle.xpath("//div[@class='work_addr']//a/text()")[0]
        address_tow = htmlEle.xpath("//div[@class='work_addr']//a/text()")[1]
        address_three = htmlEle.xpath("//div[@class='work_addr']//text()")[6]
        job = {
            'job_title': job_title,
            'logo': logo.replace('//', ""),
            'net_site': net_site,
            'financing': financing.strip(),
            "company_field": company_field.strip(),
            'xinshui': xinshui.strip(),
            'city': city.replace(r"/", "").strip(),
            'work_experience': work_experience.replace("/", "").strip(),
            'study_experience': study_experience.replace("/", "").strip(),
            'work_tags': ",".join(work_tags),
            'company': compony.strip(),
            'desc': desc,
            'introduce': "暂无简介",
            'address': address_one+address_tow+address_three.strip(),
            'company_scale':company_scale.strip()

        }
        print(job)
        self.jobs.append(job)


if __name__ == '__main__':
    spider = LanGou()
    spider.run()
