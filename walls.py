from fastapi import status,HTTPException,Depends,APIRouter
from typing import List
import models,schemas
from rooms import update_room_cost
from database import  get_db
from sqlalchemy.orm import Session  


router = APIRouter(tags=["Walls"])

@router.post("/CerateWalls/{room_id}",status_code=status.HTTP_201_CREATED)
def create_wall(room_id : int, request : schemas.WallRequest,db : Session = Depends(get_db)):
    if not db.query(models.Room).filter(models.Room.room_id == room_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Room with id {room_id} not found")
    new_wall = models.Walls(room_id=room_id,name=request.name,cost = 0.0)
    db.add(new_wall)
    db.commit()
    db.refresh(new_wall)
    return new_wall

@router.get("/GetWalls/{room_id}",status_code=status.HTTP_200_OK,response_model=List[schemas.WallResponse])
def get_walls(room_id : int,db : Session = Depends(get_db)):
    if not db.query(models.Room).filter(models.Room.room_id == room_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Room with id {room_id} not found")
    if walls := db.query(models.Walls).filter(models.Walls.room_id == room_id).all():
        return walls
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Walls for room with id {room_id} not found")

@router.delete("/DeleteWalls/{wall_id}",status_code=status.HTTP_200_OK,response_model=schemas.WallResponse)
def delete_wall(wall_id : int,db : Session = Depends(get_db)):
    if wall := db.query(models.Walls).filter(models.Walls.wall_id == wall_id).first():
        update_room_cost(wall.room_id,db)
        db.delete(wall)
        db.commit()
        return wall
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Wall with id {wall_id} not found")