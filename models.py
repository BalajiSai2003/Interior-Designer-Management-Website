from database import Base
from sqlalchemy import Column ,Integer ,String, Float, ForeignKey
from sqlalchemy.orm import relationship

class Designer(Base):
    __tablename__ = "designers"
    Designer_id  = Column(Integer,primary_key = True,nullable = False)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class Client(Base):
    __tablename__ = "clients"
    client_id  = Column(Integer,primary_key = True,nullable = False)
    name = Column(String,nullable = False)
    phone = Column(String,unique=True, nullable = False)
    email = Column(String,unique=True, nullable = False)
    Project = relationship("Project", back_populates="Client")
    rooms = relationship("Room", back_populates="Client")
    
class Project(Base):
    __tablename__ = "projects"
    Project_id  = Column(Integer,primary_key = True,nullable = False)
    client_id = Column(Integer, ForeignKey("clients.client_id", ondelete="CASCADE"))
    name = Column(String,nullable = False)
    description = Column(String,nullable = False)
    cost = Column(Float)
    Client = relationship("Client", back_populates="Project")
    Room = relationship("Room", back_populates="Project")


class Room(Base):
    __tablename__ = "rooms"
    room_id  = Column(Integer,primary_key = True,nullable = False)
    client_id = Column(Integer, ForeignKey("clients.client_id",ondelete="CASCADE"))
    Project_id = Column(Integer, ForeignKey("projects.Project_id",ondelete="CASCADE"))
    name = Column(String,nullable = False)
    length = Column(Float,nullable = False)
    width = Column(Float,nullable = False)
    area = Column(Float)
    num_walls = Column(Integer,nullable = False)
    cost = Column(Float)
    Project = relationship("Project", back_populates="Room")
    Client = relationship("Client", back_populates="rooms")
    Walls = relationship("Walls", back_populates="Room")
    



class Walls(Base):
    __tablename__ = "walls"
    wall_id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.room_id",ondelete="CASCADE"))
    name = Column(String)
    cost = Column(Float)
    Room = relationship("Room", back_populates="Walls")
    WallItem = relationship("WallItem", back_populates="Walls")
    

    
class WallItem(Base):
    __tablename__ = "wall_items"
    WallItem_id = Column(Integer, primary_key=True, index=True)
    wall_id = Column(Integer, ForeignKey("walls.wall_id",ondelete="CASCADE"))
    item = Column(String)
    length = Column(Float)
    width = Column(Float)
    depth = Column(Float)
    cost_per_unit = Column(Float)
    cost = Column(Float)
    Walls = relationship("Walls", back_populates="WallItem")
    