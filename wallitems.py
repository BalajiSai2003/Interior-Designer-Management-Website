from fastapi import status,HTTPException,Depends,APIRouter
from typing import List
import models,schemas,rooms
from database import  get_db
from sqlalchemy.orm import Session  


router = APIRouter(tags=["WallItems"])

@router.post("/CreateWallitems/{wall_id}",status_code=status.HTTP_201_CREATED,response_model=schemas.WallItemResponse)
def create_wallitem(wall_id : int, request : schemas.WallItemRequest,db : Session = Depends(get_db)):
    
    new_wallitem = models.WallItem(wall_id=wall_id,item=request.item,length=request.length,width=request.width,depth=request.depth,cost_per_unit=request.cost_per_unit,cost=request.cost_per_unit*request.length*request.width*request.depth)
    db.add(new_wallitem)
    db.commit()
    db.refresh(new_wallitem)
    room_id = db.query(models.Walls).filter(models.Walls.wall_id == wall_id).first().room_id
    rooms.update_room_cost(room_id,db)
    return new_wallitem

@router.get("/GetWallitems/{id}",status_code=status.HTTP_200_OK,response_model=List[schemas.WallItemResponse])
def get_wallitems(wall_id : int,db : Session = Depends(get_db)):
    if not db.query(models.Walls).filter(models.Walls.wall_id == wall_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Wall with id {wall_id} not found")
    if wallitems := db.query(models.WallItem).filter(models.WallItem.wall_id == wall_id).all():
        return wallitems
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"WallItems for wall with id {wall_id} not found")

@router.delete("/DeleteWallitems/{wallitem_id}",status_code=status.HTTP_200_OK,response_model=schemas.WallItemResponse)
def delete_wallitem(wallitem_id : int,db : Session = Depends(get_db)):
    if wallitem := db.query(models.WallItem).filter(models.WallItem.WallItem_id == wallitem_id).first():
        room_id = db.query(models.Walls).filter(models.Walls.wall_id == wallitem.wall_id).first().room_id
        Wall = db.query(models.Walls).filter(models.Walls.wall_id == wallitem.wall_id).first()
        Wall.cost = Wall.cost - wallitem.cost
        db.commit()
        db.refresh(Wall)
        db.delete(wallitem)
        db.commit()
        rooms.update_room_cost(room_id,db)
        return wallitem
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"WallItem with id {wallitem_id} not found")