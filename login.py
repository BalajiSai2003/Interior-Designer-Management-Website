from fastapi import status,HTTPException,Depends ,APIRouter
import schemas,database,models
from sqlalchemy.orm import Session


router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(User_credentials : schemas.LoginRequest , db : Session = Depends(database.get_db)):
    designer = db.query(models.Designer).filter(models.Designer.username == User_credentials.username).first()
    if not designer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if designer.password != User_credentials.password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    return {"message":"Login Successful"}
