from typing import List

from fastapi import APIRouter
import httpx
from httpx import Headers

import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_HOST = os.getenv('API_HOST')

HeaderApi = Headers({'Content-Type': 'application/json',  'X-RapidAPI-Key': API_KEY,
         'X-RapidAPI-Host': API_HOST})

router = APIRouter()

        

# GET players by team code
@router.get('/team/{team_code}')
async def get_players_by_team_code(team_code: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(f'https://api-football-v1.p.rapidapi.com/v3/players?team={team_code}&season=2023', headers=HeaderApi)
        
        response = r.json()
        
        return response['response']
    
# GET player by league id
@router.get('/league/{league_id}')
async def get_players_by_league_id(league_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(f'https://api-football-v1.p.rapidapi.com/v3/players?league={league_id}&season=2023', headers=HeaderApi)
        
        
        response = r.json()

        return response['response']
    
