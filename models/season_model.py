from sqlalchemy import Column, Integer, ForeignKey, String, DATE
from sqlalchemy.orm import relationship

from core.configs import settings

class SeasonModel(settings.DB_BASEMODEL):
    __tablename__ = 'seasons'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(String(256))
    flag = Column(String(256))
    ref_api = Column(String(256))
    league_id = Column(Integer, ForeignKey('leagues.id'))
    start = Column(DATE)
    end = Column(DATE)
    current = Column(String(256))
    league = relationship("LeagueModel",
                           back_populates='seasons',
                           lazy='joined')