from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from core.configs import settings

class LeagueModel(settings.DB_BASEMODEL):
    __tablename__ = 'leagues'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256))
    logo = Column(String(256))
    ref_api = Column(String(256))
    country_id = Column(Integer, ForeignKey('countries.id'))
    country = relationship("CountryModel",
                           back_populates='leagues',
                           lazy='joined')
    
    seasons = relationship("SeasonModel",
                            cascade='all, delete-orphan',
                           back_populates='league',
                           uselist=True,
                           lazy='joined')
    