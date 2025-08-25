from fastapi import FastAPI
from pydantic import BaseModel 
import redis 
import json 
import hashlib
import httpx


app = FastAPI()

redis_client = redis.Redis(host='localhost', port=6379, db=0)

class PostSchema(BaseModel):
    post_id : int


def make_cache_key(post_id:int):
    raw = f"external_api:post_{post_id}"
    return hashlib.sha256(raw.encode()).hexdigest()


@app.post("/get-post")
async def get_post(data:PostSchema):
    key = make_cache_key(data.post_id)

    cached_result = redis_client.get(key)

    if cached_result:
        print("serving from the cached result")
        return json.loads(cached_result)

    print("calling API")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://jsonplaceholder.typicode.com/posts/{data.post_id}")
        if response.status_code != 200:
            return {"error": "Post not found"}
        post_data = response.json()
        redis_client.setex(key ,600, json.dumps(post_data))
        return post_data