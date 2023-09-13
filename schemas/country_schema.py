from typing import Optional, List

from pydantic import BaseModel


class CountrySchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str]
    flag: Optional[str]
    code: Optional[str]
    ref_api: Optional[str]
    
    class Config:
        from_attributes = True