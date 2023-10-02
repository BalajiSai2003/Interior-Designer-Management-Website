from fastapi import FastAPI
import models
import client,rooms,walls,wallitems,login,projects
from database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}
app.include_router(login.router)
app.include_router(client.router)
app.include_router(projects.router)
app.include_router(rooms.router)
app.include_router(walls.router)
app.include_router(wallitems.router)
