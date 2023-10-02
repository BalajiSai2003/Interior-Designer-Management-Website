from fastapi import status,HTTPException,Depends,APIRouter
from typing import List
import models,schemas
from database import  get_db
from sqlalchemy.orm import Session  ,joinedload



router = APIRouter(tags=["Rooms"])



@router.post("/rooms/{client_id}/{Project_id}",status_code=status.HTTP_201_CREATED,response_model=schemas.RoomDetailsResponse)
def create_room(client_id : int, Project_id : int , request : schemas.RoomDetailsRequest,db : Session = Depends(get_db)):
    if not (db.query(models.Client).filter(models.Client.client_id == client_id).first()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"client with id {client_id}  not found")
    if not (db.query(models.Project).filter(models.Project.Project_id == Project_id).first()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"project with id {Project_id} not found")
    new_room = models.Room(client_id=client_id,Project_id = Project_id,name=request.name,length=request.length,width=request.width,area=request.length*request.width,num_walls=request.numWalls,cost = 0.0)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

@router.get("/rooms/{client_id}/{Project_id}",status_code=status.HTTP_200_OK,response_model=List[schemas.RoomDetailsResponse])
def get_rooms(client_id : int,Project_id : int ,db : Session = Depends(get_db)):
    if not (db.query(models.Client).filter(models.Client.client_id == client_id).first()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"client with id {client_id}  not found")
    if not (db.query(models.Project).filter(models.Project.Project_id == Project_id).first()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"project with id {Project_id} not found")
    if rooms := db.query(models.Room)\
    .filter(models.Room.client_id == client_id, models.Room.Project_id == Project_id)\
    .options(joinedload(models.Room.Walls))\
    .all():
        
        return rooms
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Rooms with client id {client_id} and project id {Project_id} not found")


@router.delete("/rooms/{client_id}/{Project_id}/{room_id}",status_code=status.HTTP_200_OK,response_model=schemas.RoomDetailsResponse)
def delete_room(client_id : int,Project_id : int,room_id : int,db : Session = Depends(get_db)):
    if not (db.query(models.Client).filter(models.Client.client_id == client_id).first()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"client with id {client_id}  not found")
    if not (db.query(models.Project).filter(models.Project.Project_id == Project_id).first()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"project with id {Project_id} not found")
    if room := db.query(models.Room).filter(models.Room.room_id == room_id).first():
        Project_id = room.Project_id
        update_project_cost(Project_id,db)
        db.delete(room)
        db.commit()
        return room
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Room with id {room_id} not found")



def update_room_cost(id : int,db : Session = Depends(get_db)):
    if room := db.query(models.Room).filter(models.Room.room_id == id).first():
        room.cost = 0
        for wall in db.query(models.Walls).filter(models.Walls.room_id == id).all():
            wall.cost = sum(
                wallitem.cost
                for wallitem in db.query(models.WallItem)
                .filter(models.WallItem.wall_id == wall.wall_id)
                .all()
            )
            room.cost += wall.cost
        # print(room.cost,room.room_id,room.Project_id,room.room_id)
        db.commit()
        db.refresh(room)
        update_project_cost(room.Project_id,db)
        return room
    
def update_project_cost(id : int,db : Session = Depends(get_db)):
    if project := db.query(models.Project).filter(models.Project.Project_id == id).first():
        project.cost = sum(
            room.cost
            for room in db.query(models.Room).filter(models.Room.Project_id == id).all()
        )
        db.commit()
        db.refresh(project)
        return project
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Room with id {id} not found")




