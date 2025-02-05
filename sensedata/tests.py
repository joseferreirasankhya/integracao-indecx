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

    def test_request_without_data(self):
        '''
        Tests if the request without data is responding correctly
        '''
        # Get response from debug page
        response = self.client.post(reverse('debug-nps'), {})

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'No data provided'})


    def test_transform_nps_data(self):
        '''
        Tests if the transform_nps_data function is working correctly
        '''
        # Create a mock request data
        data = {
            "answer": {
                "_id": "67a21a00299e75001b700356",
                "profileAnalysisAI": {
                    "content": '',
                    "date": "2025-02-04T13:45:36.784Z"
                },
                "active": True,
                "reviewLogs": [],
                "date": "2025-02-04T13:45:36.780Z",
                "answerDate": "2025-02-04T13:45:36.780Z",
                "inviteDate": "2025-02-04T13:45:36.755Z",
                "typeAnswer": "",
                "anonymousResponse": False,
                "clientId": "",
                "categories": [],
                "subCategories": [],
                "tags": "",
                "subTags": [],
                "subCategoriesIA": [],
                "audioResponseUrls": [],
                "deleted": False,
                "partialToken": "",
                "partialSaved": False,
                "partialCompleted": False,  
                "sentEmailCategoryAlert": False,
                "alertEmailSent": False,
                "name": "client",
                "email": "client@email.com",
                "phone": "5519999999999",
                "feedback": "não entendi o que a Pam falou, beijos",
                "media": "",
                "additionalQuestions": [],
                "channel": "link",
                "companyId": "67a1fdb57b0d4d001af169bd",
                "actionId": "67a21121299e75001b700223",
                "inviteId": "67a21a00299e75001b700351",
                "detailsId": "67a21a00299e75001b700350",
                "review": 8,
                "indicators": [],
                "controlId": "IBVWKJET",
                "metric": "nps-0-10",
                "createdAt": "2025-02-04T13:45:36.780Z",
                "surveyResponseTime": {
                    "endDate": "2025-02-04T13:45:36.435Z",
                    "startDate": "2025-02-04T13:44:53.848Z"
                },
                "autoClassification": [],
                "updatedAt": "2025-02-04T13:45:36.885Z",
                "sentimentAnalyzeGCP": {
                    "score": "",
                    "keyPhrases": ""
                },
                "actionName": "Teste",
                "actionControlId": "PXGP2240",
                "text": "Em uma escala de 0 a 10, quanto você indicaria a SANKHYA para um amigo ou familiar?"
            }
        }
        # Get response from debug page
        response = self.client.post(reverse('debug-nps'), data)

        # Assert that the response is 200
        self.assertEqual(response.status_code, 200)

        # Assert that the response is the expected JSON
        self.assertEqual(
            response.json(), 
            {
                'message': 'Debug', 
                'data': {
                    "nps": [
                        {
                            "id_legacy": "IBVWKJET",
                            "customer": {
                                "id": "",
                                "id_legacy": ""
                            },
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
                            "form": {
                                "id": ""
                            }
                        }
                    ]
                }
            })

    def test_transform_nps_data_with_invalid_metric(self):
        '''
        Tests if the transform_nps_data function is working correctly with an invalid metric
        '''
        # Create a mock request data with an invalid metric
        data = {
            "answer": {
                "_id": "67a21a00299e75001b700356",
                "profileAnalysisAI": {
                    "content": None,
                    "date": "2025-02-04T13:45:36.784Z"
                },
                "active": True,
                "reviewLogs": [],
                "date": "2025-02-04T13:45:36.780Z",
                "answerDate": "2025-02-04T13:45:36.780Z",
                "inviteDate": "2025-02-04T13:45:36.755Z",
                "typeAnswer": "",
                "anonymousResponse": False,
                "clientId": "",
                "categories": [],
                "subCategories": [],
                "tags": "",
                "subTags": [],
                "subCategoriesIA": [],
                "audioResponseUrls": [],
                "deleted": False,
                "partialToken": "",
                "partialSaved": False,
                "partialCompleted": False,  
                "sentEmailCategoryAlert": False,
                "alertEmailSent": False,
                "name": "client",
                "email": "client@email.com",
                "phone": "5519999999999",
                "feedback": "não entendi o que a Pam falou, beijos",
                "media": "",
                "additionalQuestions": [],
                "channel": "link",
                "companyId": "67a1fdb57b0d4d001af169bd",
                "actionId": "67a21121299e75001b700223",
                "inviteId": "67a21a00299e75001b700351",
                "detailsId": "67a21a00299e75001b700350",
                "review": 8,
                "indicators": [],
                "controlId": "IBVWKJET",
                "metric": "invalid-metric",
                "createdAt": "2025-02-04T13:45:36.780Z",
                "surveyResponseTime": {
                    "endDate": "2025-02-04T13:45:36.435Z",
                    "startDate": "2025-02-04T13:44:53.848Z"
                },
                "autoClassification": [],
                "updatedAt": "2025-02-04T13:45:36.885Z",
                "sentimentAnalyzeGCP": {
                    "score": "",
                    "keyPhrases": ""
                },
                "actionName": "Teste",
                "actionControlId": "PXGP2240",
                "text": "Em uma escala de 0 a 10, quanto você indicaria a SANKHYA para um amigo ou familiar?"
            }
        }
        # Get response from debug page
        response = self.client.post(reverse('debug-nps'), data)

        # Assert that the response is 400
        self.assertEqual(response.status_code, 400)

        # Assert that the response is the expected JSON
        self.assertEqual(response.json(), {'message': 'Wrong metric, please check the metric name'})
