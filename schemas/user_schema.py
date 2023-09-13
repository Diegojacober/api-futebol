from typing import Optional, List

from pydantic import BaseModel, EmailStr

class UserSchemaBase(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    email: EmailStr
    
    
    class Config:
        from_attributes = True
        

class UserSchemaCreate(UserSchemaBase):
    password: str
    

class UserSchemaUp(UserSchemaBase):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]