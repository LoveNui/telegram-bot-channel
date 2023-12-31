from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import uvicorn
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/logins/", response_model=schemas.User)
def read_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, email=user.email, password=user.password)
    if db_user is False:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/api_key/", response_model=schemas.API)
def read_user(api: schemas.APIBase, db: Session = Depends(get_db)):
    db_api = crud.create_user_api(db, api=api)
    if db_api is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_api

# Delete Users
@app.post("/admin/delete/users/",)
def create_user(token_str: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    if not token.verify_token(token=token_str):
        raise HTTPException(status_code=404, detail="User don't sign in")
    if token.decode_access_token(token=token_str) != "admin@mygpt.com":
        raise HTTPException(status_code=404, detail="This bot does not exist")
    
    if crud.delete_user(db, email=email):
        return {"result":"Successfully"}
    else:
        raise HTTPException(status_code=404, detail="Failed")


# Delete API
@app.post("/admin/delete/bot/{bot_username}")
def create_user(token_str: Annotated[str, Depends(oauth2_scheme)], bot_username:str, db: Session = Depends(get_db)):
    if not token.verify_token(token=token_str):
        raise HTTPException(status_code=404, detail="User don't sign in")
    if token.decode_access_token(token=token_str) != "admin@mygpt.com":
        raise HTTPException(status_code=404, detail="This bot does not exist")
    bots = crud.bots(db)
    if crud.delete_bot(db, bot_username=bot_username):
        return {"result":"Successfully"}
    else:
        raise HTTPException(status_code=404, detail="Failed")

@app.post("/admin/bots")
def bots(token_str:Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    if not token.verify_token(token=token_str):
        raise HTTPException(status_code=404, detail="User don't sign in")
    if token.decode_access_token(token=token_str) != "admin@mygpt.com":
        raise HTTPException(status_code=404, detail="This bot does not exist")
    bots = crud.bots(db)
    return {"bots":bots}

if __name__ == "__main__":
    #os.remove('clone_voice_source/New_Hero.mp3')
    uvicorn.run(app, host="localhost", port=8000)