from unittest.mock import patch, Mock
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from sensedata.services.nps_service import NPSService
from dotenv import load_dotenv
import os
import json

load_dotenv()

mock1_path = 'sensedata/tests/mock1.json'
mock2_path = 'sensedata/tests/mock2.json'
expected1_path = 'sensedata/tests/expected1.json'
expected2_path = 'sensedata/tests/expected2.json'

class NPSServiceTests(TestCase):
    def setUp(self):
        self.service = NPSService(
            api_url=os.getenv('SENSE_NPS_API_URL'),
            api_key=f"{os.getenv('SENSE_NPS_API_KEY')}="
        )

    def test_validate_webhook_data_success(self):
        """Test validation with valid data"""
        with open(mock1_path, encoding='utf8') as file:
            file = json.load(file)
            self.assertTrue(self.service._validate_webhook_data(file.get('answers')))

    def test_validate_webhook_data_failure(self):
        """Test validation with invalid data"""
        with open(mock1_path, encoding='utf8') as file:
            file = json.load(file)
            invalid_data = file.copy().get('answers')
            invalid_data['metric'] = 'invalid-metric'
            self.assertFalse(self.service._validate_webhook_data(invalid_data))

    def test_transform_data(self):
        """Test data transformation"""
        with open(mock1_path, encoding='utf8') as file, open(expected1_path, encoding='utf8') as expected:
            file = json.load(file)
            transformed = self.service._transform_data(file.get('answers'))
            self.assertEqual(transformed, json.load(expected))

    def test_send_to_api_with_mock2(self):
        """Test transform data call with other type of data"""
        with open(mock2_path, encoding='utf8') as file, open(expected2_path, encoding='utf8') as expected:
            file = json.load(file)
            transformed = self.service._transform_data(file.get('answer'))
            self.assertEqual(transformed, json.load(expected))

    @patch('requests.post')
    def test_send_to_api_success(self, mock_post):
        """Test successful API call"""
        with open(expected1_path, encoding='utf8') as expected:
            mock_response = Mock()
            mock_response.ok = True
            mock_response.json.return_value = {"status": "success"}
            mock_post.return_value = mock_response

            response = self.service._send_to_api(json.load(expected))
            self.assertEqual(response, {"status": "success"})

    @patch('requests.post')
    def test_send_to_api_failure(self, mock_post):
        """Test failed API call"""
        with open(expected1_path, encoding='utf8') as expected:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.status_code = 400
            mock_post.return_value = mock_response

            with self.assertRaises(Exception):
                self.service._send_to_api(json.load(expected))

class NPSAPITests(TestCase):
    def setUp(self):
        """Setup API key for authentication"""
        self.api_key = f"Bearer {os.getenv('API_KEY')}"
        self.headers = {"HTTP_AUTHORIZATION": self.api_key}

    def test_process_nps_without_data_returns_400(self):
        """Test API endpoint with no data"""
        response = self.client.post(
            reverse('process-nps'),
            {},
            content_type='application/json',
            **self.headers  # Adiciona a autenticação
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message': 'No data provided'})

    @patch('sensedata.services.nps_service.NPSService.process_nps_data')
    def test_process_nps_success(self, mock_process):
        """Test successful API call"""
        with open(mock1_path, encoding='utf8') as file, open(expected1_path, encoding='utf8') as expected:
            mock_process.return_value = {
                "status": "success",
                "message": "Data processed successfully",
                "data": json.load(expected)
            }

            response = self.client.post(
                reverse('process-nps'),
                data=json.load(file),
                content_type='application/json',
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json().get('status'), 'success')

    @patch('sensedata.services.nps_service.NPSService.process_nps_data')
    def test_process_nps_validation_error(self, mock_process):
        """Test API call with invalid data"""
        mock_process.side_effect = ValueError("Invalid webhook data")

        response = self.client.post(
            reverse('process-nps'),
            {'answers': {'invalid': 'data'}},
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message': 'Invalid webhook data'})

    # Desabilitado temporariamente
    '''def test_process_nps_without_api_key_returns_403(self):
        """Test API call without authentication"""
        response = self.client.post(
            reverse('process-nps'),
            data=MOCK_NPS_DATA,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'No API key provided.'})'''

