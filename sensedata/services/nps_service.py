# Imports
# - Utils
from sensedata.utils.nps import NPSData

# NPS Service
class NPSService:
    def transform_nps_data(self, request_data: dict):
        '''
        Transforms the request data to the Sense NPS API JSON format
        '''
        # If request data is provided
        try:
            # If the metric is nps-0-10
            if request_data['metric'] == 'nps-0-10':
                # Transform the request data to the Sense NPS API JSON format
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
                # Return the Sense NPS API JSON format
                return nps.to_sense_api_json()
            else:
                return None
        # If the metric is not provided
        except KeyError as e:
            # Log the missing key
            print(f"Missing key in request data: {e}")
            return None
        # If an error occurs
        except Exception as e:
            # Log any other exceptions
            print(f"An error occurred: {e}")
            return None
