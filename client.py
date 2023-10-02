from fastapi import status,HTTPException,Depends,APIRouter
from typing import List
import models,schemas
from database import  get_db
from sqlalchemy.orm import Session ,joinedload 

router = APIRouter(tags=["Client"])

@router.post("/createClient",status_code=status.HTTP_201_CREATED ,response_model=schemas.ClientDetails)
def createUser(Client :schemas.ClientRequest ,db : Session = Depends(get_db)):

    new_client = models.Client(**Client.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return new_client



@router.get("/getClient",response_model=List[schemas.ClientResponse])
def getUser(db : Session = Depends(get_db)):
    
    return db.query(models.Client).options(joinedload(models.Client.Project).joinedload(models.Project.Room)).all()
# return db.query(models.Client).options(joinedload(models.Client.Project).joinedload(models.Project.Room).joinedload(models.Room.Walls).joinedload(models.Walls.WallItem)).all()

@router.delete("/DeleyeClient/{client_id}",response_model=schemas.ClientResponse)
def deleteClient(client_id : int,db : Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.client_id == client_id).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Client with id {client_id} not found")
    db.delete(client)
    db.commit()
    return client