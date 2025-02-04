# Imports
# - Utils
from sensedata.utils.nps import NPSData

# NPS Service
class NPSService:
    def transform_nps_data(self, request_data: dict):
        '''
        Transforms NPS data from the request into a NPSData object
        '''
        # Create NPSData object with the request data
        if request_data['metric'] == 'nps-0-10':
            nps = NPSData(
                form_id_legacy=request_data['controlId'],
                client_id_legacy=request_data['clientId'],
                ref_date=request_data['date'],
                survey_date=request_data['inviteDate'],
                medium=request_data['channel'],
                respondent=request_data['email'],
                score=int(request_data['review']),
                comments=request_data['feedback'],
                tags=request_data['tags'],
                group=request_data['companyId'],
            )
            # Convert NPSData object to Sense NPS API JSON format
            return nps.to_sense_api_json()
        else:
            return None
