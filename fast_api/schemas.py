from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: str

class UserList(BaseModel):
    users: list[UserPublic]

class Token(BaseModel):
    access_token: str
    token_type: str
