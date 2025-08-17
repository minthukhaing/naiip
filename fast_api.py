from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
# from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorClient
import os
import asyncio
import time

#call model
from models.my_en_convert import myan
from models.pali_my_convert import parli
import asyncio


SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key_for_dev")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "525600"))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "api_db")

# Initialize MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]
users_collection = db["users"]

# Rate Limiting
class RateLimiter:
    def __init__(self, max_calls=10, period=60):
        self.calls = {}
        self.max_calls = max_calls
        self.period = period

    def allow_request(self, user_id: str):
        now = time.time()
        if user_id not in self.calls:
            self.calls[user_id] = []
        timestamps = self.calls[user_id]
        timestamps[:] = [t for t in timestamps if t > now - self.period]
        if len(timestamps) >= self.max_calls:
            return False
        timestamps.append(now)
        return True

rate_limiter = RateLimiter(max_calls=10, period=60)



# JWT Setup
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    password: str

# Input အတွက် model
class TextInput(BaseModel):
    text: str

# Helper Functions

# Helper Functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Check if token is blacklisted
        blacklisted = await users_collection.find_one({"username": username})
        if not blacklisted:
            raise HTTPException(status_code=401, detail="Token has been revoked")
            
        # Check if user

        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



# Endpoints
@app.post("/register")
async def register(user: UserCreate):
    existing = await users_collection.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = get_password_hash(user.password)
    await users_collection.insert_one({"username": user.username, "password": hashed})
    return {"message": "User created"}

@app.get("/users")
async def get_users():
    users = await users_collection.find({}).to_list(100)
    return [{"username": u["username"]} for u in users]

@app.delete("/users/{username}")
async def delete_user(username: str):


    result = await users_collection.delete_one({"username": username})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
  

    return {"message": f"User {username} deleted"}

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(data={"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}


# Secured POST endpoint
@app.post("/myanmar_to_english")
def myanmar_to_english(input: TextInput, user: str = Depends(get_current_user)):
    
    if not rate_limiter.allow_request(user):
        raise HTTPException(status_code=429, detail="Too many requests. Try again later.")
    
    txt=input.text

    result=asyncio.run(myan(txt))

    return {
        "received_text": result,
        "length": len(input.text),
        "message": f"Thank you for the text(myanmar_to_english): '{input.text}'",
        "user": user
    }

@app.post("/parli_to_roman")
def parli_to_roman(input: TextInput, user: str = Depends(get_current_user)):
    if not rate_limiter.allow_request(user):
        raise HTTPException(status_code=429, detail="Too many requests. Try again later.")
    
    txt=input.text

    result=asyncio.run(parli(txt))

    return {
        "received_text": result,
        "length": len(input.text),
        "message": f"Thank you for the text(parli_to_roman): '{input.text}'",
        "user": user
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)