from fastapi import APIRouter

from api.v1.endpoints import user
from api.v1.endpoints import country

api_router = APIRouter()

api_router.include_router(user.router, prefix='/users', tags=['Users'])
api_router.include_router(country.router, prefix='/countries', tags=['Countries'])