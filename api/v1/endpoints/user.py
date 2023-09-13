from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
 
from models.user_model import UserModel


from schemas.user_schema import UserSchemaBase
from schemas.user_schema import UserSchemaCreate
from schemas.user_schema import UserSchemaUp

from core.security import generate_hash_pass
from core.auth import authenticate, create_access_token

from core.deps import get_session, get_current_user

router = APIRouter()

@router.get('/logged', response_model=UserSchemaBase)
def get_logged(logged_user: UserModel = Depends(get_current_user)):
    return logged_user

# POST / SignUp -> Criar conta
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
async def post_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    new_user: UserModel = UserModel(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=generate_hash_pass(user.password)
    )
    
    async with db as session:
        try:
            session.add(new_user)
            await session.commit()

        
            return new_user
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='E-mail must be unique')
    
        
@router.get('/{user_id}', response_model=UserSchemaBase, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):

    if user_id == logged_user.id:
        async with db as session:
            query = select(UserModel).filter(UserModel.id == user_id)
            results = await session.execute(query)
            user: UserSchemaBase = results.scalars().unique().one_or_none()
            
            if user:
                return user
            else:
                raise HTTPException(
                    detail='User not found',
                    status_code=status.HTTP_404_NOT_FOUND)
    else:
        raise HTTPException(detail='You can only access your own profile',
                            status_code=status.HTTP_401_UNAUTHORIZED)
        
#PUT user
@router.put('/{user_id}', response_model=UserSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_user(user_id: int, user: UserSchemaUp, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):

    if user_id == logged_user.id:
        async with db as session:
            query = select(UserModel).filter(UserModel.id == user_id)
            results = await session.execute(query)
            user_up: UserSchemaUp = results.scalars().unique().one_or_none()
            
            if user_up:
                if user.first_name:
                    user_up.first_name = user.first_name
                
                if user.last_name:
                    user_up.last_name = user.last_name
                    
                if user.email:
                    user_up.email = user.email
                
                if user.password:
                    user_up.password = generate_hash_pass(user.password)
                
                await session.commit()
                
                return user_up
            else:
                raise HTTPException(
                    detail='User not found',
                    status_code=status.HTTP_404_NOT_FOUND)
    else:
        raise HTTPException(detail='Access denied',
                            status_code=status.HTTP_401_UNAUTHORIZED)

# POST login
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await authenticate(email=form_data.username, password=form_data.password, db=db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid Credentials'
        )
        
    return JSONResponse(content={"access_token": create_access_token(sub=user.id), "token_type": "bearer"})
        
        