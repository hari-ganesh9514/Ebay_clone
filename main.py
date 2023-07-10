from traceback import format_exception_only
from fastapi import FastAPI, Request,Form,Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import engine,SessionLocal
import models
from sqlalchemy.orm import Session
from pydantic import Field, BaseModel
app = FastAPI()
templates = Jinja2Templates(directory = "templates")

app.mount("/static",StaticFiles(directory="static"),name="static")

models.Base.metadata.create_all(bind=engine)
@app.get('/')
def welcome(request: Request):
    return templates.TemplateResponse("front_page.html",{"request": request})
@app.get('/login')
def welcome(request: Request):
    return templates.TemplateResponse("login.html",{"request": request})

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()


@app.post('/register_user',)
async def save_user_data(request: Request, name: str= Form(...), email: str=format_exception_only(...), password: str=Form(...), db:Session=Depends(get_db)):
    user= models.Users()
    user.name = name
    user.password = password
    user.email  = email
    
    userExists = db.query(models.Users).filter(models.Users.email == email).first()
    if userExists:
        return {"message":"User Already Exists"}
    db.add(user)
    db.commit()
    return templates.TemplateResponse('login.html',{"requests":request})

@app.get('/getusersList')
def welcome(request: Request,db: Session= Depends(get_db)):
    usersList=db.query(models.Users).all()
    return{"users":usersList}

@app.post('/login_user',)
async def login_user(request:Request, email:str=Form(...),password: str=Form(...), db:Session=Depends(get_db)):
    user=models.Users()
    userExists= db.query(models.Users).filter(models.Users.email == email).first()
    
    if userExists:
        userExists= db.query(models.Users).filters(models.Users.email== email,models.Users.password==password).first()
        if userExists:
            return templates.TemplateResponse("home.html",{"request": request, "user_details": userExists.name})
        else:
            return {"Please check your password"}
    else:
        return{"Create User"}