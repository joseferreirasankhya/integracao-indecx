from typing import Dict, Any
import requests
from utils.utils import DateUtils

class NPSService:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    # --- Public methods ---
    def process_nps_data(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa os dados do NPS seguindo todos os passos necessários:
        1. Validação
        2. Transformação
        3. Enriquecimento (se necessário)
        4. Envio para API
        """
        # Early returns para validações
        if not self._validate_webhook_data(webhook_data):
            raise ValueError("Invalid webhook data")

        try:
            # Pipeline de processamento
            transformed_data = self._transform_data(webhook_data)
            response = self._send_to_api(transformed_data)

            return {
                "status": "success",
                "message": "Data processed successfully",
                "data": response
            }
            
        except Exception as e:
            raise Exception(f"Failed to process NPS data: {str(e)}")

    # --- Private methods ---
    def _validate_webhook_data(self, data: Dict[str, Any]) -> bool:
        """Valida os dados recebidos do webhook"""
        required_fields = ['metric', 'review', 'email', 'controlId']
        return all(
            field in data and data[field] 
            for field in required_fields
        ) and data['metric'] == 'nps-0-10' and data['active'] == True

    def _transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transforma os dados para o formato da Sense API"""
        return {
            "nps": [{
                "id_legacy": data['controlId'],
                "customer": {
                    "id": None,
                    "id_legacy": data['clientId']
                },
                "ref_date": DateUtils.convert_to_date(data['createdAt']),
                "survey_date": DateUtils.convert_to_date(data['inviteDate']),
                "medium": data['channel'],
                "respondent": data['email'],
                "score": int(data['review']),
                "role": "",
                "stage": "",
                "group": data['clientId'],
                "category": "",
                "comments": data['feedback'],
                "tags": "NPS"
            }]
        }

    def _send_to_api(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Envia os dados para a API de destino"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            f"{self.api_url}/nps",
            json=data,
            headers=headers
        )
        
        if not response.ok:
            raise Exception(f"API request failed: {response.json()}")
            
        return response.json()
