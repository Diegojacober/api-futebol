from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response
import httpx

router = APIRouter()

        

# GET teams
@router.get('/teams')
async def get_teams():
    async with httpx.AsyncClient() as client:
        r = await client.get(f'http://10.21.62.8:8001/api/v1/basquete/teams/')
        
        print(r.json())
        response = r.json()
        
        return response

# GET leagues 
@router.get('/leagues')
async def get_leagues():
    async with httpx.AsyncClient() as client:
        e = await client.get(f'http://10.21.62.8:8001/api/v1/basquete/leagues/')
        
        response = e.json()
        
        return response
    
