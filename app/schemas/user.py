from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """
    Schema para registrar usuario
    """

    email: str
    password: str


class UserLogin(BaseModel):
    """
    Schema para login
    """

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    Schema de respuesta (no expone password)
    """

    id: int
    email: EmailStr

    class Config:
        from_attributes = True
