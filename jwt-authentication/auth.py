import os
from dotenv import load_dotenv
from datetime import datetime , timedelta,timezone
from authlib.jose import JoseError,jwt
from fastapi import HTTPException

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRY = int(os.getenv("ACCESS_TOKEN_EXPIRY", 30))  



def create_access_token(data : dict):
    header = {'alg' : ALGORITHM}
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY)
    payload = data.copy()
    payload.update({'exp' : expire})
    return jwt.encode(header, payload, SECRET_KEY).decode('utf-8')



def verify_token(token : str): 
    try: 
        claims = jwt.decode(token , SECRET_KEY)
        claims.validate()
        username = claims.get('sub')
        if not username:
            raise HTTPException(status_code=401, detail='Invalid token')
        return username
    except JoseError:
        raise HTTPException(status_code=401, detail='Invalid token')