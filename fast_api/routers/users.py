from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api.database import get_session
from fast_api.models import User
from fast_api.schemas import Message, UserList, UserPublic, UserSchema
from fast_api.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=T_Session):
    db_user = session.scalar(select(User).where((User.username == user.username) | (User.email == user.email)))

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    hashed_password = get_password_hash(user.password)

    db_user = User(username=user.username, password=hashed_password, email=user.email)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/users/', response_model=UserList)
def read_users(
    session: T_Session,
    limit: int = 20,
    skip: int = 0,
):
    users = session.scalars(select(User).limit(limit).offset(skip))

    return {'users': users}


@router.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session: T_Session, current_user=T_CurrentUser):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions')

    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.email = user.email
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: T_Session, current_user=T_CurrentUser):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions')

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}
