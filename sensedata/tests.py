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
      "date":"2025-02-13T13:01:26.793Z",
      "anonymousResponse": False,
      "_id":"67aded263feb060032e06e27",
      "name":"EMPRESA XYZ",
      "email":"cliente@empresa.com",
      "phone":"5500000000000",
      "feedback":"O serviço precisa de melhorias, especialmente no suporte. O atendimento tem demoras e poderia ser mais eficiente.",
      "additionalQuestions":[
         {
            "conditionalQuestion":[],
            "multipleValues":[
               "Outros: Gerente"
            ],
            "options":[],
            "indicatorValueEnabled": False,
            "selectedIndicator":"None",
            "indicatorValue":"None",
            "indicatorCriterion":"None",
            "questionId":"67851f1db726a6002b1153de",
            "anonymousResponse": False,
            "_id":"67aded263feb060032e06e28",
            "text":" Qual o cargo que o(a) Sr.(a) ocupa atualmente na empresa? (PERGUNTAR PRIMEIRO)",
            "type":"MULTIPLE",
            "multipleType":"radio"
         }
      ],
      "channel":"manual",
      "companyId":"000000000000000000000000",
      "actionId":"000000000000000000000000",
      "inviteId":"000000000000000000000000",
      "detailsId":"000000000000000000000000",
      "review":0,
      "indicators":[
         {
            "_id":"000000000000000000000000",
            "column":"codigo_parceiro",
            "value":"99999",
            "indicatorId":"000000000000000000000000",
            "key":"99999"
         },
         {
            "_id":"000000000000000000000000",
            "column":"nome_contato",
            "value":"JOÃO SILVA",
            "indicatorId":"000000000000000000000000",
            "key":"joao_silva"
         },
         {
            "_id":"000000000000000000000000",
            "column":"codico_unidade",
            "value":"000",
            "indicatorId":"000000000000000000000000",
            "key":"000"
         },
         {
            "_id":"000000000000000000000000",
            "column":"unidade",
            "value":"FILIAL SUL",
            "indicatorId":"000000000000000000000000",
            "key":"filial_sul"
         },
         {
            "_id":"000000000000000000000000",
            "column":"cliente_desde",
            "value":"01/01/2020",
            "dateValue":"2020-01-01T00:00:00.000Z",
            "indicatorId":"000000000000000000000000",
            "key":"00000"
         },
         {
            "_id":"000000000000000000000000",
            "column":"tempo_de_casa",
            "value":"De 1 a 3 anos",
            "indicatorId":"000000000000000000000000",
            "key":"de_1_a_3_anos"
         },
         {
            "_id":"000000000000000000000000",
            "column":"segmento",
            "value":"Varejo",
            "indicatorId":"000000000000000000000000",
            "key":"varejo"
         },
         {
            "_id":"000000000000000000000000",
            "column":"perfil",
            "value":"BÁSICO",
            "indicatorId":"000000000000000000000000",
            "key":"basico"
         },
         {
            "_id":"000000000000000000000000",
            "column":"faixa_de_faturamento",
            "value":"100.000,00 À 200.000,00",
            "indicatorId":"000000000000000000000000",
            "key":"100.000,00_a_200.000,00"
         },
         {
            "_id":"000000000000000000000000",
            "column":"fase",
            "value":"Em Desenvolvimento",
            "indicatorId":"000000000000000000000000",
            "key":"em_desenvolvimento"
         },
         {
            "_id":"000000000000000000000000",
            "column":"status",
            "value":"Ativo",
            "indicatorId":"000000000000000000000000",
            "key":"ativo"
         },
         {
            "_id":"000000000000000000000000",
            "column":"classificacao",
            "value":"Prata",
            "indicatorId":"000000000000000000000000",
            "key":"prata"
         }
      ],
      "controlId":"XXXXXXXX",
      "metric":"nps-0-10",
      "createdAt":"2025-02-13T13:01:26.793Z"
   }
}


EXPECTED_TRANSFORMED_DATA = {
    "nps": [
        {
            "id_legacy": "XXXXXXXX",
            "customer": {
                "id": None,
                "id_legacy": 99999
            },
            "ref_date": "2025-02-13",
            "survey_date": "2025-02-13",
            "medium": "manual",
            "respondent": "JOÃO SILVA",
            "score": 0,
            "role": "Outros: Gerente",
            "stage": "",
            "group": "",
            "category": "",
            "comments": "O serviço precisa de melhorias, especialmente no suporte. O atendimento tem demoras e poderia ser mais eficiente.",
            "tags": "NPS"
        }
    ]
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
        mock_process.return_value = {
            "status": "success",
            "message": "Data processed successfully",
            "data": EXPECTED_TRANSFORMED_DATA
        }

        response = self.client.post(
            reverse('process-nps'),
            data=MOCK_NPS_DATA,
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

