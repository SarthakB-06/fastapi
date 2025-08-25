import redis


r = redis.Redis(host='localhost', port=6379, db=0)

try:
    if r.ping():
        print("Connected to Redis server successfully!")
except redis.ConnectionError as e:
    print(f"Failed to connect to Redis server: {e}")

r.set('framework' , 'FastAPI')


value = r.get('framework')
print(f"stored framework is: {value.decode()}")
