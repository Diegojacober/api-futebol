from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.season_model import SeasonModel 
from models.user_model import UserModel
from models.league_model import LeagueModel

from schemas.season_schema import SeasonSchema
from schemas.season_schema import SeasonSchemaLeague

from core.deps import get_session, get_current_user

router = APIRouter()

#POST Season
@router.post('/', response_model=SeasonSchema, status_code=status.HTTP_201_CREATED)
async def create_season(season: SeasonSchema, logged_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    
    async with db as session:
        query = select(LeagueModel).filter(LeagueModel.id == season.league_id)
        result = await session.execute(query)
        league: LeagueModel = result.scalars().unique().one_or_none()
            
        if league:
            new_season: SeasonModel = SeasonModel(
                year=season.year,
                flag=season.flag,
                ref_api=season.ref_api,
                league_id=season.league_id,
                start=season.start,
                end=season.end,
                current=season.current
            )
        
            db.add(new_season)
            await db.commit()
            return new_season
        else:
            raise HTTPException(detail='League not Found',
                                status_code=status.HTTP_404_NOT_FOUND)
        

# GET Seasons
@router.get('/', response_model=List[SeasonSchemaLeague])
async def get_seasons(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(SeasonModel)
        result = await session.execute(query)
        seasons: List[SeasonModel] = result.scalars().unique().all()
        
        return seasons
    

# GET Season
@router.get('/{season_id}', response_model=SeasonSchemaLeague, status_code=status.HTTP_200_OK)
async def get_season(season_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(SeasonModel).filter(SeasonModel.id == season_id)
        result = await session.execute(query)
        season: SeasonModel = result.scalars().unique().one_or_none()
        
        if season:
            return season
        else:
            raise HTTPException(detail='Season not Found',
                                status_code=status.HTTP_404_NOT_FOUND)

# PUT season
@router.put('/{season_id}', response_model=SeasonSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_season(season_id: int, season: SeasonSchema , db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(SeasonModel).filter(SeasonModel.id == season_id)
        result = await session.execute(query)
        season_up: SeasonModel = result.scalars().unique().one_or_none()
        
        if season_up:
            
            if season.year:
                season_up.year = season.year
                
            if season.flag:
                season_up.flag = season.flag
                
            if season.ref_api:
                season_up.ref_api = season.ref_api

            if season.start:
                season_up.start = season.start

            if season.end:
                season_up.end = season.end
                
            if season.current:
                season_up.current = season.current

            if season.league_id:
                async with db as session:
                    query = select(LeagueModel).filter(LeagueModel.id == season.league_id)
                    result = await session.execute(query)
                    league: LeagueModel = result.scalars().unique().one_or_none()
                        
                    if league:
                        season_up.league_id = season.league_id
                    else:
                        raise HTTPException(detail='League not Found',
                                            status_code=status.HTTP_404_NOT_FOUND)
               
                
            await session.commit()
            
            return season_up
        else:
            raise HTTPException(detail='League not found',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE season
@router.delete('/{season_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_season(season_id: int, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):

    async with db as session:
        query = select(SeasonModel).filter(SeasonModel.id == season_id)
        result = await session.execute(query)
        season_del: SeasonModel = result.scalars().unique().one_or_none()
        
        
        if season_del:
            await session.delete(season_del)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Season not found',
                                status_code=status.HTTP_404_NOT_FOUND)