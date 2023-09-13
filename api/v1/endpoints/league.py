from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.league_model import LeagueModel 
from models.user_model import UserModel
from models.country_model import CountryModel

from schemas.league_schema import LeagueSchema
from schemas.league_schema import LeagueSchemaCountry

from core.deps import get_session, get_current_user

router = APIRouter()

#POST league
@router.post('/', response_model=LeagueSchema, status_code=status.HTTP_201_CREATED)
async def create_league(league: LeagueSchema, logged_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    
    async with db as session:
        query = select(CountryModel).filter(CountryModel.id == league.country_id)
        result = await session.execute(query)
        country: CountryModel = result.scalars().unique().one_or_none()
            
        if country:
            new_league: LeagueModel = LeagueModel(name=league.name, logo=league.logo, ref_api=league.ref_api, country_id=league.country_id)
        
            db.add(new_league)
            await db.commit()
            return new_league
        else:
            raise HTTPException(detail='Country not Found',
                                status_code=status.HTTP_404_NOT_FOUND)
        

# GET leagues
@router.get('/', response_model=List[LeagueSchemaCountry])
async def get_leagues(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LeagueModel)
        result = await session.execute(query)
        leagues: List[LeagueModel] = result.scalars().unique().all()
        
        return leagues
    

# GET league
@router.get('/{league_id}', response_model=LeagueSchemaCountry, status_code=status.HTTP_200_OK)
async def get_league(league_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LeagueModel).filter(LeagueModel.id == league_id)
        result = await session.execute(query)
        league: LeagueModel = result.scalars().unique().one_or_none()
        
        if league:
            return league
        else:
            raise HTTPException(detail='League not Found',
                                status_code=status.HTTP_404_NOT_FOUND)
            
@router.get('/countries/{country_id}', response_model=List[LeagueSchemaCountry], status_code=status.HTTP_200_OK)
async def get_league_per_country(country_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LeagueModel).filter(LeagueModel.country_id == country_id)
        result = await session.execute(query)
        leagues: List[LeagueModel] = result.scalars().unique().all()
        
        if leagues:
            return leagues
        else:
            raise HTTPException(detail='Leagues not Found',
                                status_code=status.HTTP_404_NOT_FOUND)
            

# PUT artigo
@router.put('/{league_id}', response_model=LeagueSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_league(league_id: int, league: LeagueSchema , db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(LeagueModel).filter(LeagueModel.id == league_id)
        result = await session.execute(query)
        league_up: LeagueModel = result.scalars().unique().one_or_none()
        
        if league_up:
            
            if league.logo:
                league_up.logo = league.logo
                
            if league.name:
                league_up.name = league.name
                
            if league.ref_api:
                league_up.ref_api = league.ref_api

            if league.country_id:
                async with db as session:
                    query = select(CountryModel).filter(CountryModel.id == league.country_id)
                    result = await session.execute(query)
                    country: CountryModel = result.scalars().unique().one_or_none()
                        
                    if country:
                        league_up.country_id = league.country_id
                    else:
                        raise HTTPException(detail='Country not Found',
                                            status_code=status.HTTP_404_NOT_FOUND)
               
                
            await session.commit()
            
            return league_up
        else:
            raise HTTPException(detail='League not found',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE league
@router.delete('/{league_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_league(league_id: int, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):

    async with db as session:
        query = select(LeagueModel).filter(LeagueModel.id == league_id)
        result = await session.execute(query)
        league_del: LeagueModel = result.scalars().unique().one_or_none()
        
        
        if league_del:
            await session.delete(league_del)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='league not found',
                                status_code=status.HTTP_404_NOT_FOUND)