from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .crud import create_user_crud, get_users_crud, get_user_by_id_crud

app = FastAPI()

# Pydantic models for request/response validation
class UserCreate(BaseModel):
    username: str
    email: str
    password: str  # In practice, you should hash passwords

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

@app.post("/users/", response_model=UserResponse)
async def create_user_endpoint(user: UserCreate):
    user_data = create_user_crud(user.username, user.email, user.password)
    return user_data

@app.get("/users/", response_model=list[UserResponse])
async def read_users(skip: int = 0, limit: int = 100):
    users = get_users_crud(limit, skip)
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int):
    user = get_user_by_id_crud(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
