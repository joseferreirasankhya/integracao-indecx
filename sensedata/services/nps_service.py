from typing import Optional, Dict, Any
from datetime import datetime
import requests

class NPSService:
    '''def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key'''

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
            enriched_data = self._enrich_data(transformed_data)
            #response = self._send_to_api(enriched_data)
            
            return {
                "status": "success",
                "message": "Data processed successfully",
                "data": enriched_data
            }
            
        except Exception as e:
            raise Exception(f"Failed to process NPS data: {str(e)}")

    def _validate_webhook_data(self, data: Dict[str, Any]) -> bool:
        """Valida os dados recebidos do webhook"""
        required_fields = ['metric', 'review', 'email', 'controlId']
        return all(
            field in data and data[field] 
            for field in required_fields
        ) and data['metric'] == 'nps-0-10'

    def _transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transforma os dados para o formato da Sense API"""
        return {
            "nps": [{
                "id_legacy": data['controlId'],
                "customer": {
                    "id": "",
                    "id_legacy": ""
                },
                "ref_date": data['createdAt'],
                "survey_date": data['inviteDate'],
                "medium": data['channel'],
                "respondent": data['email'],
                "score": int(data['review']),
                "role": "",
                "stage": "",
                "group": data['companyId'],
                "category": "",
                "comments": data['feedback'],
                "tags": "",
                "form": {"id": ""}
            }]
        }

    def _enrich_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enriquece os dados com informações adicionais se necessário
        Por exemplo: adicionar timestamps, IDs únicos, etc.
        """
        data['processed_at'] = datetime.utcnow().isoformat()
        return data

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
            raise Exception(f"API request failed: {response.status_code}")
            
        return response.json()
