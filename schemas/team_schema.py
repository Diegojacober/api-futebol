from typing import Optional

from pydantic import BaseModel

class TeamSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str]
    code: Optional[str]
    ref_api: Optional[str]
    country_id: Optional[str]
    founded: Optional[str]
    logo: Optional[str]
    
    class Config:
        from_attributes = True
    