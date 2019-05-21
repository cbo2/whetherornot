from django.test import TestCase

# Create your tests here.

class WONTests(TestCase):
    def test_home_page_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_search_page_status(self):
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 200)