from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.country_model import CountryModel 
from models.user_model import UserModel

from schemas.country_schema import CountrySchema

from core.deps import get_session, get_current_user

router = APIRouter()

#POST Country
@router.post('/', response_model=CountrySchema, status_code=status.HTTP_201_CREATED)
async def create_country(country: CountrySchema, logged_user: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    new_country: CountryModel = CountryModel(
        name=country.name,
        flag=country.flag,
        code=country.code,
        ref_api=country.ref_api
    )
    
    db.add(new_country)
    await db.commit()
    return new_country

# GET countries
@router.get('/', response_model=List[CountrySchema])
async def get_countries(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CountryModel)
        result = await session.execute(query)
        countries: List[CountryModel] = result.scalars().unique().all()
        
        return countries
    

# GET country
@router.get('/{country_id}', response_model=CountrySchema, status_code=status.HTTP_200_OK)
async def get_country(country_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CountryModel).filter(CountryModel.id == country_id)
        result = await session.execute(query)
        country: CountryModel = result.scalars().unique().one_or_none()
        
        if country:
            return country
        else:
            raise HTTPException(detail='Country not Found',
                                status_code=status.HTTP_404_NOT_FOUND)
            

# PUT country
@router.put('/{country_id}', response_model=CountrySchema, status_code=status.HTTP_202_ACCEPTED)
async def put_country(country_id: int, country: CountrySchema , db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(CountryModel).filter(CountryModel.id == country_id)
        result = await session.execute(query)
        country_up: CountryModel = result.scalars().unique().one_or_none()
        
        if country_up:
            if country.code:
                country_up.code = country.code
            
            if country.flag:
                country_up.flag = country.flag
                
            if country.name:
                country_up.name = country.name
                
            if country.ref_api:
                country_up.ref_api = country.ref_api
                
            await session.commit()
            
            return country_up
        else:
            raise HTTPException(detail='Country not found',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE country
@router.delete('/{country_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_country(country_id: int, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):

    async with db as session:
        query = select(CountryModel).filter(CountryModel.id == country_id)
        result = await session.execute(query)
        country_del: CountryModel = result.scalars().unique().one_or_none()
        
        
        if country_del:
            await session.delete(country_del)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Country not found',
                                status_code=status.HTTP_404_NOT_FOUND)