from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from core.configs import settings

class TeamModel(settings.DB_BASEMODEL):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256))
    code = Column(String(256))
    country_id = Column(String(256))
    founded = Column(String(256))
    logo = Column(String(256))
    ref_api = Column(String(256))