from fastapi import status,HTTPException,Depends,APIRouter
from typing import List
import models,schemas
from database import  get_db
from sqlalchemy.orm import Session ,joinedload


router = APIRouter(tags=["Projects"])

@router.post("/createProject/{client_id}",status_code=status.HTTP_201_CREATED ,response_model=schemas.ProjectResponse)
def createProject(client_id:int,Project :schemas.ProjectRequest ,db : Session = Depends(get_db)):
    if not db.query(models.Client).filter(models.Client.client_id == client_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Client with id {client_id} not found")
    
    new_project = models.Project(**Project.dict())
    new_project.client_id = client_id
    new_project.cost = 0.0
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project

@router.get("/getProject/{client_id}",response_model=List[schemas.ProjectResponse])
def getProject(client_id : int , db : Session = Depends(get_db)):
    if project := db.query(models.Project).filter(models.Project.client_id == client_id).options(joinedload(models.Project.Room)).all():
        return project
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Project with client id {client_id} not found")


# db.query(models.Project).filter(models.Project.client_id == client_id).options(joinedload(models.Project.Room).joinedload(models.Room.Walls).joinedload(models.Walls.WallItem)).all()


@router.delete("/DeleyeProject/{project_id}",response_model=schemas.ProjectResponse)
def deleteProject(project_id : int,db : Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.Project_id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Project with id {project_id} not found")
    db.delete(project)
    db.commit()
    return project