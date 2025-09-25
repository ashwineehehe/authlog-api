from pydantic import BaseModel, EmailStr

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenUser(BaseModel):
    id: int
    email: EmailStr
