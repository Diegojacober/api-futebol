from typing import Optional, List

from pydantic import BaseModel, HttpUrl

from .league_schema import LeagueSchema

class CountrySchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str]
    flag: Optional[str]
    ref_api: Optional[str]
    
    class Config:
        from_attributes = True
        
        
class CountrySchemaLeagues(CountrySchema):
    leagues: Optional[List[LeagueSchema]]