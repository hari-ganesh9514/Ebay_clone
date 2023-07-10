from traceback import format_exception_only
from fastapi import FastAPI, Request,Form,Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
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
    cookie = request.cookies.get("user_name")
    if cookie is None:
        return templates.TemplateResponse("front_page.html",{"request": request})
    else:
        return templates.TemplateResponse("home.html",{"request":request,"user_details":cookie})

@app.get('/login')
def welcome(request: Request):
    return templates.TemplateResponse("login.html",{"request": request})

@app.get("/logout")
def welcome(request:Request):
    response = templates.TemplateResponse("front_page.html",{"request":request})
    response.delete_cookie(key="user_id",path="/")
    response.delete_cookie(key="user_name",path="/")
    return response
@app.get('/create_listings')
def welcome(request: Request):
    return templates.TemplateResponse("create_listings.html",{"request":request})
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
            response = templates.TemplateResponse("home.html",{"request": request, "user_details": userExists.name})
            response.set_cookie(key="user_id",value=userExists.id,path="/")
            response.set_cookie(key="user_name",value=userExists.name,path="/")
            return response
        else:
            return {"Please check your password"}
    else:
        return{"Create User"}
    
@app.post('/create_listing/{user_id}')
async def create_listing_data(user_id:int,request:Request,title:str=Form(...),price:float=Form(...),description:str=Form(...),image:str=Form(...),categories:str=Form(...), db:Session=Depends(get_db)):
    listing =models.Listings()
    listing.user_id=user_id
    listing.product_title=title
    listing.description=description
    listing.image=image
    listing.category=categories
    print(categories)
    db.add(listing)
    db.commit()
    listing_data =db.query(models.Listings).all()
    return templates.TemplateResponse("active_listings.html",{"request":request,"listings_data":listing_data})

@app.get('/active_listings')
def welcome(request: Request,db:Session=Depends(get_db)):
    listings_data = db.query(models.Listings).all()
    return templates.TemplateResponse("active_listings.html",{"request":request,"listings_data":listings_data})

@app.get('/categories')
def welcome(request:Request,db:Session=Depends(get_db)):
    listings_data= db.query(models.Listings).all()
    print(listings_data)
    result =[row.__dict__ for row in listings_data]
    categories={}
    for product in result:
        category = product["category"]
        if category not in categories:
            categories[category]=[]
        categories[category].append(product)
    print(categories)
  # return {"category":categories}
    return templates.TemplateResponse("categories.html",{"request":request,"categories":categories})