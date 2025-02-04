# Imports
# - Django
from django.test import TestCase
from django.urls import reverse

# Test Cases
class SensedataTests(TestCase):
    def test_index(self):
        '''
        Tests if the index page is responding correctly
        '''
        # Get response from index page
        response = self.client.get(reverse('index'))

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Hello, World!'})

    def test_debug(self):
        '''
        Tests if the debug page is responding correctly
        '''
        data = {
            'message': 'Debug',
            'data': 'test_data'
        }
        response = self.client.post(reverse('debug'), data)
        self.assertEqual(response.json(), {'message': 'Debug', 'data': data})
        self.assertEqual(response.status_code, 200)

    def test_request_without_data(self):
        '''
        Tests if the request without data is responding correctly
        '''
        response = self.client.post(reverse('debug'), {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'No data provided'})
