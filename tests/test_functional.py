import re
from selenium import webdriver
from jobplus import create_app, db
import time
import unittest


class NewVistorTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.browser = webdriver.Firefox()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.browser.quit()
        
    def can_open_index_page(self):
        # 朋友推荐了一个新网站，
        # 李明去看了
        # 进入首页
        self.browser.get('http://localhost:5000/')
        self.assertTrue(re.search('JobPlus', self.browser.page_source))
        # time.sleep(3)

    def can_register(self, username, email, password):
        self.browser.find_element_by_name('username').send_keys(username)
        self.browser.find_element_by_name('email').send_keys(email)
        self.browser.find_element_by_name('password').send_keys(password)
        self.browser.find_element_by_name('repeat_password').send_keys(password)
        self.browser.find_element_by_name('submit').click()

    def can_login(self, email, password):
        self.browser.find_element_by_name('email'). \
            send_keys(email)
        self.browser.find_element_by_name('password').send_keys(password)
        self.browser.find_element_by_name('submit').click()

    def test_person_can_register_and_login(self):
        self.can_open_index_page()
        self.browser.find_element_by_link_text('求职者注册').click()
        self.assertIn('<h2>用户注册</h2>', self.browser.page_source)
        self.can_register('limin', 'limin@123.com', 'limin@123.com')
        # time.sleep(3)
    # def test_can_login(self):
        # 进入登录页面
        # self.browser.find_element_by_link_text('登录').click()
        self.assertIn('<h2>登录</h2>', self.browser.page_source)
        # 登录
        self.can_login('limin@123.com', 'limin@123.com')
        # 进入用户资料页面
        self.assertIn('<h2>完善用户信息</h2>', self.browser.page_source)
        self.assertIn('limin', self.browser.page_source)
        self.browser.find_element_by_name('username').send_keys('limin')
        self.browser.find_element_by_name('phone_number').send_keys('123465646')
        self.browser.find_element_by_name('work_year').send_keys('1')
        self.browser.find_element_by_name('submit').click()
        # self.browser.find_element_by_link_text('Profile').click()
        time.sleep(3)

        # self.fail('Finish the test!')

    def test_enterprise_can_register_and_login(self):
        self.can_open_index_page()
        self.browser.find_element_by_link_text('公司注册').click()
        self.assertIn('<h2>企业注册</h2>', self.browser.page_source)
        self.can_register('gongsi', 'gongsi@123.com', 'gongsi@123.com')
        # time.sleep(3)
        # def test_can_login(self):
        # 进入登录页面
        # self.browser.find_element_by_link_text('登录').click()
        self.assertIn('<h2>登录</h2>', self.browser.page_source)
        # 登录
        self.can_login('gongsi@123.com', 'gongsi@123.com')
        # 进入用户资料页面
        self.assertIn('<h2>完善企业信息</h2>', self.browser.page_source)
        self.assertIn('gongsi', self.browser.page_source)
        self.browser.find_element_by_name('name').send_keys('gongsi')
        self.browser.find_element_by_name('address').send_keys('address')
        self.browser.find_element_by_name('net_site').send_keys('www.wosuo.com.cn')
        self.browser.find_element_by_name('logo').send_keys('http://wosuo.com.cn/static/img/wosuologo.png')
        self.browser.find_element_by_name('introduce').send_keys('introduce')
        self.browser.find_element_by_name('detail').send_keys('detail')
        self.browser.find_element_by_name('city').send_keys('city')
        self.browser.find_element_by_name('financing').send_keys('financing')
        self.browser.find_element_by_name('company_field').send_keys('company_field')


        self.browser.find_element_by_name('submit').click()
        # self.browser.find_element_by_link_text('Profile').click()
        time.sleep(3)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
