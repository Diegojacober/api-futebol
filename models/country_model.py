from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from core.configs import settings

class CountryModel(settings.DB_BASEMODEL):
    __tablename__ = 'countries'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256))
    flag = Column(String(256))
    ref_api = Column(String(256))
    leagues = relationship("LeagueModel",
                            cascade='all, delete-orphan',
                           back_populates='country',
                           uselist=True,
                           lazy='joined')