from fastapi import FastAPI,HTTPException,Depends,Form,status
from fastapi.security import OAuth2PasswordBearer 

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token")
def login(username: str = Form(...),password : str = Form(...)):
    if username == "admin" and password == "secret":
        return {"access_token": "valid_token", "token_type": "bearer"}
    raise HTTPException(status_code=400 , detail="Invalid credentials")

def decode_token(token: str):
    if token == 'valid_token':
        return {"username": "admin"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
    )


def get_current_user( token : str = Depends(oauth2_scheme)):
    return decode_token(token)


@app.get("/profile")
def get_profile(user = Depends(get_current_user)):
    return {"username": user["username"], "role": "admin"}