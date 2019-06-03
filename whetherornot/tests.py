from django.test import TestCase
from selenium import webdriver
from time import sleep

# Create your tests here.

class WONFunctionalTests(TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    # def test_there_is_homepage(self):
    #     sleep(1)
    #     self.browser.get('http://localhost:8000')
    #     self.assertIn('Whether or Not App', self.browser.page_source)

    # def test_navigate_to_login(self):
    #     sleep(1)
    #     self.browser.get('http://localhost:8000')
    #     self.browser.find_element_by_id('login').click()
    #     self.assertIn('Username:', self.browser.page_source)

    # def test_can_login(self):
    #     sleep(1)
    #     self.browser.get('http://localhost:8000')
    #     self.browser.find_element_by_id('login').click()
    #     username = self.browser.find_element_by_id('id_username')
    #     username.send_keys('cbo')
    #     password = self.browser.find_element_by_id('id_password')
    #     password.send_keys('cbo')
    #     self.browser.find_element_by_name('submit').click()
    #     self.assertIn('Welcome cbo', self.browser.page_source)

    def tearDown(self):
        self.browser.close()


class WONUnitTests(TestCase):

    def test_home_page_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'search.html')

    def test_home_page_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_search_page_status(self):
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 200)

