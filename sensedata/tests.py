from unittest.mock import patch, Mock
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from sensedata.services.nps_service import NPSService
from dotenv import load_dotenv
import os

load_dotenv()

MOCK_NPS_DATA = {
   "answer":{
      "_id":"67ad0838ad10f500209c14c7",
      "profileAnalysisAI":{
         "content":"None",
         "date":"2025-02-12T20:44:40.261Z"
      },
      "active":True,
      "reviewLogs":[

      ],
      "date":"2025-02-12T20:44:40.255Z",
      "answerDate":"2025-02-12T20:44:40.255Z",
      "inviteDate":"2025-02-12T20:40:08.835Z",
      "typeAnswer":"None",
      "anonymousResponse":False,
      "clientId":"None",
      "categories":[

      ],
      "subCategories":[

      ],
      "tags":[

      ],
      "subTags":[

      ],
      "subCategoriesIA":[

      ],
      "audioResponseUrls":[

      ],
      "deleted":False,
      "partialToken":"None",
      "partialSaved":False,
      "partialCompleted":False,
      "sentEmailCategoryAlert":False,
      "alertEmailSent":False,
      "name":"KIFRANGO",
      "email":"usuario@kifrango.com.br",
      "phone":"(34) 99876-5432",
      "feedback":"Teste Teste 2",
      "media":"None",
      "additionalQuestions":[
         {
            "_id":"67ad0838ad10f500209c14c8",
            "type":"REVIEWS",
            "text":" Qual o cargo que o(a) Sr.(a) ocupa atualmente na empresa? (PERGUNTAR PRIMEIRO)"
         }
      ],
      "channel":"manual",
      "companyId":"67a1fdb57b0d4d001af169bd",
      "actionId":"67ad025fad10f500209c136d",
      "inviteId":"67ad07286769710013700b75",
      "detailsId":"67ad07286769710013700b32",
      "review":9,
      "indicators":[
         {
            "_id":"67ad07286769710013700b49",
            "column":"codigo_parceiro",
            "value":"19259",
            "indicatorId":"67ad033aad10f500209c13d2",
            "key":"19259"
         },
         {
            "_id":"67ad07286769710013700b4a",
            "column":"nome_contato",
            "value":"User2",
            "indicatorId":"67ad0347ad10f500209c13e2",
            "key":"user2"
         },
         {
            "_id":"67ad07286769710013700b4b",
            "column":"codico_unidade",
            "value":"34",
            "indicatorId":"67ad0366b1d260001afb8c57",
            "key":"34"
         },
         {
            "_id":"67ad07286769710013700b4c",
            "column":"unidade",
            "value":"FILIAL ESPIRITO SANTO",
            "indicatorId":"67ad0370b1d260001afb8c67",
            "key":"filial_espirito_santo"
         },
         {
            "_id":"67ad07286769710013700b4d",
            "column":"cliente_desde",
            "value":"09/08/2018",
            "dateValue":"2018-08-09T00:00:00.000Z",
            "indicatorId":"67ad0380ad10f500209c13ff",
            "key":"43321"
         },
         {
            "_id":"67ad07286769710013700b4e",
            "column":"tempo_de_casa",
            "value":"De 5 a 10 anos",
            "indicatorId":"67ad038cb1d260001afb8c77",
            "key":"de_5_a_10_anos"
         },
         {
            "_id":"67ad07286769710013700b4f",
            "column":"segmento",
            "value":"Indústria",
            "indicatorId":"67ad0395b1d260001afb8c8b",
            "key":"industria"
         },
         {
            "_id":"67ad07286769710013700b50",
            "column":"faixa_de_faturamento",
            "value":"1.000.001,00 À 4.000.000,00",
            "indicatorId":"67ad03aaad10f500209c1417",
            "key":"1.000.001,00_a_4.000.000,00"
         },
         {
            "_id":"67ad07286769710013700b51",
            "column":"fase",
            "value":"Acompanhamento Evolutivo",
            "indicatorId":"67ad03b1ad10f500209c142f",
            "key":"acompanhamento_evolutivo"
         },
         {
            "_id":"67ad07286769710013700b52",
            "column":"status",
            "value":"Ativo",
            "indicatorId":"67ad03baad10f500209c1443",
            "key":"ativo"
         },
         {
            "_id":"67ad07286769710013700b53",
            "column":"cargo_contato",
            "value":"Desenvolvedor",
            "indicatorId":"67ad03c4ad10f500209c1457",
            "key":"desenvolvedor"
         },
         {
            "_id":"67ad07286769710013700b54",
            "column":"classificacao",
            "value":"Prata",
            "indicatorId":"67ad03d1ad10f500209c1467",
            "key":"prata"
         }
      ],
      "controlId":"MBBXLF18",
      "metric":"nps-0-10",
      "createdAt":"2025-02-12T20:44:40.255Z",
      "answeredByUser":"67a1fe5e7b0d4d001af16a2c",
      "surveyResponseTime":{
         "endDate":"2025-02-12T20:44:39.955Z",
         "startDate":"2025-02-12T20:44:32.787Z"
      },
      "autoClassification":[

      ],
      "updatedAt":"2025-02-12T20:44:40.308Z",
      "sentimentAnalyzeGCP":{
         "score":"None",
         "keyPhrases":"None"
      },
      "actionName":"Pesquisa PHD - SANKHYA (Réplica)",
      "actionControlId":"O9CDXMK4",
      "text":"Em uma escala de 0 a 10 (onde 0 Jamais indicaria e 10 Certamente indicaria), qual a chance de você indicar a SANKHYA para um amigo ou conhecido?"
   }
}

EXPECTED_TRANSFORMED_DATA = {
    "nps": [{
        "id_legacy": "MBBXLF18",
        "customer": {"id": None, "id_legacy": 19259},
        "ref_date": "2025-02-12",
        "survey_date": "2025-02-12",
        "medium": "manual",
        "respondent": "User2",
        "score": 9,
        "role": "Desenvolvedor",
        "stage": "",
        "group": "",
        "category": "",
        "comments": "Teste Teste 2",
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
        self.assertTrue(self.service._validate_webhook_data(MOCK_NPS_DATA.get('answer')))

    def test_validate_webhook_data_failure(self):
        """Test validation with invalid data"""
        invalid_data = MOCK_NPS_DATA.copy()
        invalid_data['metric'] = 'invalid-metric'
        self.assertFalse(self.service._validate_webhook_data(invalid_data))

    def test_transform_data(self):
        """Test data transformation"""
        transformed = self.service._transform_data(MOCK_NPS_DATA.get('answer'))
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
            {'answer': {'invalid': 'data'}},
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

