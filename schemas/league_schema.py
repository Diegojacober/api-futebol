from typing import Optional, List

from pydantic import BaseModel
from schemas.country_schema import CountrySchema

class LeagueSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str]
    logo: Optional[str]
    ref_api: Optional[str]
    country_id: Optional[int]
    
    
    class Config:
        from_attributes = True
        
class LeagueSchemaCountry(LeagueSchema):
    country: Optional[CountrySchema]
    
        