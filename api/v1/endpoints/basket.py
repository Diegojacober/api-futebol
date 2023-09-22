from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response
import httpx

router = APIRouter()

        

# GET teams
@router.get('/teams')
async def get_teams():
    async with httpx.AsyncClient() as client:
        r = await client.get(f'http://10.21.62.8:8001/api/v1/basquete/teams')
        
        response = r.json()
        
        return response
