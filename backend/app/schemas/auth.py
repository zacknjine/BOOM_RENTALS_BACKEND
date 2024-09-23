from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True  
