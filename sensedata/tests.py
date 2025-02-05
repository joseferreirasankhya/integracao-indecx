from unittest.mock import patch, Mock
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from sensedata.services.nps_service import NPSService

MOCK_NPS_DATA = {
    "_id": "67a21a00299e75001b700356",
    "email": "client@email.com",
    "feedback": "não entendi o que a Pam falou, beijos",
    "channel": "link",
    "companyId": "67a1fdb57b0d4d001af169bd",
    "controlId": "IBVWKJET",
    "metric": "nps-0-10",
    "review": 8,
    "createdAt": "2025-02-04T13:45:36.780Z",
    "inviteDate": "2025-02-04T13:45:36.755Z"
}

EXPECTED_TRANSFORMED_DATA = {
    "nps": [{
        "id_legacy": "IBVWKJET",
        "customer": {"id": "", "id_legacy": ""},
        "ref_date": "2025-02-04T13:45:36.780Z",
        "survey_date": "2025-02-04T13:45:36.755Z",
        "medium": "link",
        "respondent": "client@email.com",
        "score": 8,
        "role": "",
        "stage": "",
        "group": "67a1fdb57b0d4d001af169bd",
        "category": "",
        "comments": "não entendi o que a Pam falou, beijos",
        "tags": "",
        "form": {"id": ""}
    }]
}

class NPSServiceTests(TestCase):
    def setUp(self):
        self.service = NPSService(
            #api_url='http://test-api.com',
            #api_key='test-key'
        )

    def test_validate_webhook_data_success(self):
        """Test validation with valid data"""
        self.assertTrue(self.service._validate_webhook_data(MOCK_NPS_DATA))

    def test_validate_webhook_data_failure(self):
        """Test validation with invalid data"""
        invalid_data = MOCK_NPS_DATA.copy()
        invalid_data['metric'] = 'invalid-metric'
        self.assertFalse(self.service._validate_webhook_data(invalid_data))

    def test_transform_data(self):
        """Test data transformation"""
        transformed = self.service._transform_data(MOCK_NPS_DATA)
        self.assertEqual(transformed, EXPECTED_TRANSFORMED_DATA)

    @patch('requests.post')
    def test_send_to_api_success(self, mock_post):
        """Test successful API call"""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {"status": "success"}
        mock_post.return_value = mock_response

        response = self.service._send_to_api(EXPECTED_TRANSFORMED_DATA)
        self.assertEqual(response, {"status": "success"})

    @patch('requests.post')
    def test_send_to_api_failure(self, mock_post):
        """Test failed API call"""
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        with self.assertRaises(Exception):
            self.service._send_to_api(EXPECTED_TRANSFORMED_DATA)

class NPSAPITests(TestCase):
    def test_process_nps_without_data_returns_400(self):
        """Test API endpoint with no data"""
        response = self.client.post(reverse('process-nps'), {})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message': 'No data provided'})

    @patch('sensedata.services.nps_service.NPSService.process_nps_data')
    def test_process_nps_success(self, mock_process):
        """Test successful API call"""
        mock_process.return_value = {
            "status": "success",
            "message": "Data processed successfully",
            "data": EXPECTED_TRANSFORMED_DATA
        }

        response = self.client.post(
            reverse('process-nps'),
            {'answer': MOCK_NPS_DATA},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()['status'],
            'success'
        )

    @patch('sensedata.services.nps_service.NPSService.process_nps_data')
    def test_process_nps_validation_error(self, mock_process):
        """Test API call with invalid data"""
        mock_process.side_effect = ValueError("Invalid webhook data")

        response = self.client.post(
            reverse('process-nps'),
            {'answer': {'invalid': 'data'}},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'message': 'Invalid webhook data'}
        )
