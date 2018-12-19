from selenium import webdriver
import unittest
import re

class NewVistorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        
    def tearDown(self):
        self.browser.quit()
        
    def test_can_open_index_page(self):
        # 朋友推荐了一个新网站，
        # 李明去看了
        # 进入首页
        self.browser.get('http://localhost:5000/')
        self.assertTrue(re.search('JobPlus', self.browser.page_source))
        # 进入登录页面
        # self.browser.find_element_by_link_text('Log In').click()
        # self.assertIn('<h1>Login</h1>', self.client.page_source)
        # # 登录
        # self.browser.find_element_by_name('email').\
        # send_keys('john@example.com')
        # self.browser.find_element_by_name('password').send_keys('cat')
        # self.browser.find_element_by_name('submit').click()
        # self.assertTrue(re.search('Hello,\s+john!', self.client.page_source))
        # # 进入用户资料页面
        # self.browser.find_element_by_link_text('Profile').click()
        # self.assertIn('<h1>john</h1>', self.client.page_source)
        
        # 他注意到，网页的标题和头部都包含?这个词
        # self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')
        
if __name__ == '__main__':
    unittest.main(warnings='ignore')
