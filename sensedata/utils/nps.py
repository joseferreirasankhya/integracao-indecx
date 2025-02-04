# Imports
# - Dataclasses
from dataclasses import dataclass
# - Datetime
from datetime import date
# - Typing
from typing import Optional

# NPS data class
@dataclass
class NPSData:
    """
    Represents Net Promoter Score (NPS) survey response data.
    
    Stores information about an NPS survey response including identification,
    dates, respondent details, and survey results.
    """
    # NPS data properties
    form_id_legacy: str
    client_id_legacy: str
    ref_date: date
    survey_date: date
    medium: str
    respondent: str
    score: int
    comments: Optional[str]
    tags: Optional[list[str]]
    group: str

    def to_sense_api_json(self):
        '''
        Converts NPSData to Sense NPS API JSON format
        '''
        # Return the NPS data in the Sense NPS API JSON format
        return {
            "nps": [
                {
                    "id_legacy": self.form_id_legacy,

                    "customer": {
                        "id": '',
                        "id_legacy": self.client_id_legacy
                    },
                    "ref_date": self.ref_date,
                    "survey_date": self.survey_date,
                    "medium": self.medium,
                    "respondent": self.respondent,
                    "score": self.score,
                    "role": '',
                    "stage": '',
                    "group": self.group,
                    "category": '',
                    "comments": self.comments,
                    "tags": self.tags,
                    "form": {
                        "id": ''
                    }
                }
            ]
        }
