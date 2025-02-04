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
    id_legacy: str
    ref_date: date
    survey_date: date
    medium: str
    respondent: str
    score: int
    comments: Optional[str]
    tags: Optional[list[str]]
    role: str
    stage: str
    category: str
    form_id: str
