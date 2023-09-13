from typing import Optional, List

from pydantic import BaseModel
from .league_schema import LeagueSchema

class SeasonSchema(BaseModel):
    id: Optional[int] = None
    year: Optional[str]
    flag: Optional[str]
    ref_api: Optional[str]
    league_id: Optional[int]
    start: Optional[str]
    end: Optional[str]
    current: Optional[str]
    
    class Config:
        from_attributes = True
        
class SeasonSchemaLeague(SeasonSchema):
    league: Optional[LeagueSchema]
    