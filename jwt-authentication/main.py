from fastapi import FastAPI,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from auth import create_access_token , verify_token
from utils import get_user, verify_password
from models import UserInDB

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post('/token')
def login(form_Data: OAuth2PasswordRequestForm = Depends()):
    user_dict = get_user(form_Data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_Data.password, user_dict['hashed_password']):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user_dict['username']})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get('/users')
def read_users(token : str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return {"username": user['sub']}

