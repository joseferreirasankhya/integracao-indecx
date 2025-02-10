from unittest.mock import patch, Mock
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from sensedata.services.nps_service import NPSService
from dotenv import load_dotenv
import os

load_dotenv()

MOCK_NPS_DATA = {
  "answers": {
    "active": True,
    "date": "2025-02-10T20:35:20.896Z",
    "anonymousResponse": False,
    "_id": "67aa6308ff525d001a6dd51d",
    "name": "LABTECH PRODUTOS PARA LABORATORIOS E HOSPITAIS LTDA",
    "email": "jose.ferreira@sankhya.com.br",
    "phone": "(51)999999999",
    "feedback": "Sankhya é top, Sankhya é agro, Sankhya é vida!!!",
    "additionalQuestions": [],
    "channel": "email",
    "companyId": "67a1fdb57b0d4d001af169bd",
    "actionId": "67aa350c6ab287002201a7e7",
    "inviteId": "67aa62f16877e10012d3c854",
    "detailsId": "67aa62f16877e10012d3c83f",
    "review": 10,
    "indicators": [
      {
        "_id": "67aa62f16877e10012d3c843",
        "column": "codigo_parceiro",
        "value": "34232",
        "indicatorId": "67aa3fe46ab287002201a9c5",
        "key": "34232"
      },
      {
        "_id": "67aa62f16877e10012d3c844",
        "column": "nome_do_contato",
        "value": "José Lucas",
        "indicatorId": "67aa3ffe0e7d84001c2f5e7c",
        "key": "jose_lucas"
      },
      {
        "_id": "67aa62f16877e10012d3c845",
        "column": "unidade",
        "value": "FILIAL SÃO JOSÉ DOS CAMPOS",
        "indicatorId": "67aa40116ab287002201a9f5",
        "key": "filial_sao_jose_dos_campos"
      },
      {
        "_id": "67aa62f16877e10012d3c846",
        "column": "cliente_desde",
        "value": "01/04/2022",
        "dateValue": "2022-04-01T00:00:00.000Z",
        "indicatorId": "67aa40156ab287002201aa05",
        "key": "44652"
      },
      {
        "_id": "67aa62f16877e10012d3c847",
        "column": "tempo_de_casa",
        "value": "De 1 a 3 anos",
        "indicatorId": "67aa401a6ab287002201aa15",
        "key": "de_1_a_3_anos"
      },
      {
        "_id": "67aa62f16877e10012d3c848",
        "column": "segmento",
        "value": "Serviço",
        "indicatorId": "67aa401d6ab287002201aa25",
        "key": "servico"
      },
      {
        "_id": "67aa62f16877e10012d3c849",
        "column": "faixa_de_faturamento",
        "value": "1.000.001,00 À 4.000.000,00",
        "indicatorId": "67aa402e6ab287002201aa45",
        "key": "1.000.001,00_a_4.000.000,00"
      },
      {
        "_id": "67aa62f16877e10012d3c84a",
        "column": "fase",
        "value": "Acompanhamento Evolutivo",
        "indicatorId": "67aa40306ab287002201aa55",
        "key": "acompanhamento_evolutivo"
      },
      {
        "_id": "67aa62f16877e10012d3c84b",
        "column": "status",
        "value": "Ativo",
        "indicatorId": "67aa40326ab287002201aa65",
        "key": "ativo"
      },
      {
        "_id": "67aa62f16877e10012d3c84c",
        "column": "cargo_do_contato",
        "value": "Diretor de TI",
        "indicatorId": "67aa403e0e7d84001c2f5e9f",
        "key": "diretor_de_ti"
      },
      {
        "_id": "67aa62f16877e10012d3c84d",
        "column": "classificacao",
        "value": "Prata",
        "indicatorId": "67aa40446ab287002201aa75",
        "key": "prata"
      }
    ],
    "controlId": "0VFBL4YQ",
    "metric": "nps-0-10",
    "createdAt": "2025-02-10T20:35:20.896Z"
  }
}

EXPECTED_TRANSFORMED_DATA = {
    "nps": [{
        "id_legacy": "0VFBL4YQ",
        "customer": {"id": None, "id_legacy": 34232},
        "ref_date": "2025-02-10",
        "survey_date": "2025-02-10",
        "medium": "email",
        "respondent": "José Lucas",
        "score": 10,
        "role": "Diretor de TI",
        "stage": "",
        "group": 34232,
        "category": "",
        "comments": "Sankhya é top, Sankhya é agro, Sankhya é vida!!!",
        "tags": "NPS",
    }]
}

class NPSServiceTests(TestCase):
    def setUp(self):
        self.service = NPSService(
            api_url=os.getenv('SENSE_NPS_API_URL'),
            api_key=f"{os.getenv('SENSE_NPS_API_KEY')}="
        )

    def test_validate_webhook_data_success(self):
        """Test validation with valid data"""
        self.assertTrue(self.service._validate_webhook_data(MOCK_NPS_DATA.get('answers')))

    def test_validate_webhook_data_failure(self):
        """Test validation with invalid data"""
        invalid_data = MOCK_NPS_DATA.copy()
        invalid_data['metric'] = 'invalid-metric'
        self.assertFalse(self.service._validate_webhook_data(invalid_data))

    def test_transform_data(self):
        """Test data transformation"""
        transformed = self.service._transform_data(MOCK_NPS_DATA.get('answers'))
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
            data=MOCK_NPS_DATA,
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json().get('status'),
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