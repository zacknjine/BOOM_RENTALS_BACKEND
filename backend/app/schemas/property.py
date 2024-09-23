from pydantic import BaseModel

class PropertyBase(BaseModel):
    name: str
    location: str
    number_of_houses: int
    description: str

class PropertyCreate(PropertyBase):
    pass

class Property(PropertyBase):
    id: int  

    class Config:
        from_attributes = True  
