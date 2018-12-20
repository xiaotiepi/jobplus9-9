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
        time.sleep(3)

    def can_register(self):
        self.browser.find_element_by_name('username').send_keys('limin')
        self.browser.find_element_by_name('email').send_keys('limin@123.com')
        self.browser.find_element_by_name('password').send_keys('limin@123.com')
        self.browser.find_element_by_name('repeat_password').send_keys('limin@123.com')
        self.browser.find_element_by_name('submit').click()

    def can_login(self):
        self.browser.find_element_by_name('email'). \
            send_keys('limin@123.com')
        self.browser.find_element_by_name('password').send_keys('limin@123.com')
        self.browser.find_element_by_name('submit').click()

    def test_can_personal_register(self):
        self.can_open_index_page()
        self.browser.find_element_by_link_text('求职者注册').click()
        self.assertIn('<h2>用户注册</h2>', self.browser.page_source)
        self.can_register()
        time.sleep(3)
    # def test_can_login(self):
        # 进入登录页面
        # self.browser.find_element_by_link_text('登录').click()
        self.assertIn('<h2>登录</h2>', self.browser.page_source)
        # 登录
        self.can_login()
        # 进入用户资料页面
        self.assertIn('<h2>完善用户信息</h2>', self.browser.page_source)
        self.assertIn('limin', self.browser.page_source)
        # self.browser.find_element_by_link_text('Profile').click()
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
