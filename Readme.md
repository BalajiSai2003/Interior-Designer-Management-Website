# Interior Designer Management Backend
Interior Designer Management using FastAPI
### This application has 6 routes
## 1) Authentication
### This route responsible for validate user
## 2) Client
### This route responsible for Adding Clients, To get clients Data, To Delete a Client
## 3) Project
### This route responsible for Adding a Project, To get Project Data, To Delete a Project
## 4) Rooms
### This route responsible for Adding Rooms, To get Rooms Data, To Delete a Room Based on Client id and project id
## 5) Wall
### This route responsible for Adding Walls based on room id, To get Walls Data based on room id, To Delete a Wall Based on Wall id
## 6) WallItem
### This route responsible for Adding WallItems, To get WallItems Data, To Delete a WallItem based on WallItem id
# How to run locally


First, clone this repo by using the following command in cmd Make sure to have git and python3 installed
````

git clone https://github.com/BalajiSai2003/Interior-Designer-Management-Website.git

````

Then, navigate to the cloned directory


````

cd Interior-Designer-Management-Website

````

Then install fastapp using all flag like 

````

pip install -r requirements.txt

````

Setup your Postgressql database system with username postgres password admin and database name as InteriorDesignerManagement

Then go this repo folder in your local computer run follwoing command
````

uvicorn main:app --reload

````

Then you can use following link to use the  API

````

http://127.0.0.1:8000/docs 

````