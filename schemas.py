
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    username: str
    password: str

class ClientRequest(BaseModel):
    name: str
    phone: str
    email: EmailStr
    
class ClientDetails(BaseModel):
    client_id : int
    name: str
    phone: str
    email: EmailStr
    
    class Config:
        orm_mode = True
class ClientResponse(BaseModel):
    client_id : str
    name: str
    phone: str
    email: EmailStr
    Project : list = []
    # rooms : list = []

    class Config:
        orm_mode = True

class ProjectRequest(BaseModel):
    name: str
    description: str

class ProjectResponse(BaseModel):
    Project_id: int
    client_id : int
    name: str
    description: str
    cost: float
    Room: list = []
    
    class Config:
        orm_mode = True

class RoomDetailsRequest(BaseModel):
    name: str
    length: float
    width: float
    numWalls: int


class RoomDetailsResponse(BaseModel):
    room_id: int
    client_id : int
    name: str
    length: float
    width: float
    area: float
    num_walls: int
    cost: float
    Walls: list = []

    class Config:
        orm_mode = True

class WallRequest(BaseModel):
    name: str

class WallResponse(BaseModel):
    wall_id: int
    room_id: int
    name: str
    cost: float
    WallItem: list = []
    class Config:
        orm_mode = True

class WallItemRequest(BaseModel):
    item: str
    length: float
    width: float
    depth: float
    cost_per_unit: float

class WallItemResponse(BaseModel):
    WallItem_id: int
    wall_id: int
    item: str
    length: float
    width: float
    depth: float
    cost_per_unit: float
    cost: float

    class Config:
        orm_mode = True