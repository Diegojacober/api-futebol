from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.team_model import TeamModel 
from models.user_model import UserModel
from models.country_model import CountryModel

from schemas.team_schema import TeamSchema

from core.deps import get_session, get_current_user

router = APIRouter()

#POST Team
@router.post('/', response_model=TeamSchema, status_code=status.HTTP_201_CREATED)
async def create_team(team: TeamSchema, logged_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    
    
    new_team: TeamModel = TeamModel(
        name=team.name,
        code=team.code,
        country_id=team.country_id,
        founded=team.founded,
        logo=team.logo,
        ref_api=team.ref_api
    )

    db.add(new_team)
    await db.commit()
    return new_team
       
        

# GET Team
@router.get('/', response_model=List[TeamSchema])
async def get_teams(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TeamModel)
        result = await session.execute(query)
        seasons: List[TeamModel] = result.scalars().unique().all()
        
        return seasons
    

# GET Season
@router.get('/{team_id}', response_model=TeamSchema, status_code=status.HTTP_200_OK)
async def get_team(team_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TeamModel).filter(TeamModel.id == team_id)
        result = await session.execute(query)
        team: TeamModel = result.scalars().unique().one_or_none()
        
        if team:
            return team
        else:
            raise HTTPException(detail='Team not Found',
                                status_code=status.HTTP_404_NOT_FOUND)

# PUT team
@router.put('/{team_id}', response_model=TeamSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_season(team_id: int, team: TeamSchema , db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(TeamModel).filter(TeamModel.id == team_id)
        result = await session.execute(query)
        team_up: TeamModel = result.scalars().unique().one_or_none()
        
        if team_up:
            
            if team.name:
                team_up.name = team.name
                
            if team.code:
                team_up.code = team.code
                
            if team.ref_api:
                team_up.ref_api = team.ref_api

            if team.founded:
                team_up.founded = team.founded

            if team.logo:
                team_up.logo = team.logo

            if team.country_id:
                async with db as session:
                    query = select(CountryModel).filter(CountryModel.id == team.country_id)
                    result = await session.execute(query)
                    country: CountryModel = result.scalars().unique().one_or_none()
                        
                    if country:
                        team_up.country_id = team.country_id
                    else:
                        raise HTTPException(detail='Country not Found',
                                            status_code=status.HTTP_404_NOT_FOUND)
               
                
            await session.commit()
            
            return team_up
        else:
            raise HTTPException(detail='League not found',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE team
@router.delete('/{team_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: int, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):

    async with db as session:
        query = select(TeamModel).filter(TeamModel.id == team_id)
        result = await session.execute(query)
        team_del: TeamModel = result.scalars().unique().one_or_none()
        
        
        if team_del:
            await session.delete(team_del)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Team not found',
                                status_code=status.HTTP_404_NOT_FOUND)