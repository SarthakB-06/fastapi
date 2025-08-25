from fastapi import FastAPI
from pydantic import BaseModel
import redis
import sqlite3
import json
import hashlib


app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0)


def get_db_connection():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn


def inti_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 30), ('Bob', 25) ,('Jim' , 35)") 
    conn.commit()
    conn.close()


inti_db()

class UserQuery(BaseModel):
    user_id : int

def make_cache_key(user_id:int):
    raw = f"user:{user_id}"
    return f"UserQuery:{hashlib.sha256(raw.encode()).hexdigest()}"


@app.post("/get_user")
async def get_user(query: UserQuery):
    key = make_cache_key(query.user_id)

    cached_result = redis_client.get(key)

    if cached_result:
        print("Serving user data from cache")
        return json.loads(cached_result)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (query.user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return {"error": "User not found"}

    user_data = {
        "id": user["id"],
        "name": user["name"],
        "age": user["age"]
    }  

    redis_client.setex(key, json.dumps(user_data), ex=3600)
    
    return user_data  