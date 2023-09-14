from fastapi import APIRouter

from api.v1.endpoints import user
from api.v1.endpoints import country
from api.v1.endpoints import league
from api.v1.endpoints import season
from api.v1.endpoints import team

api_router = APIRouter()

api_router.include_router(user.router, prefix='/users', tags=['Users'])
api_router.include_router(country.router, prefix='/countries', tags=['Countries'])
api_router.include_router(league.router, prefix='/leagues', tags=['Leagues'])
api_router.include_router(team.router, prefix='/teams', tags=['Teams'])