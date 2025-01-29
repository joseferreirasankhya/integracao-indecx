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
        # Get response from debug page
        response = self.client.post(reverse('debug'), {'message': 'Debug'})

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Debug', 'data': {'message': 'Debug'}})
