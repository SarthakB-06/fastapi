from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    'johndoe': {
        'username' : 'johndoe',
        'hashed_password' : pwd_context.hash("secret"),

    }
}

def get_user(username : str):
    user = fake_users_db.get(username)
    return user

def verify_password(plain_password:str , hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
