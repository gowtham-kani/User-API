from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# In-memory database for users
users_db = []

# Pydantic model for creating a user
class UserCreate(BaseModel):
    id : int
    name: str
    email: str

# Pydantic model for updating a user (id is not required in the body)
class UserUpdate(BaseModel):
    name: str
    email: str

# Pydantic model for returning a user
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

# GET all users
@app.get("/users", response_model=List[UserResponse])
def get_users():
    return users_db

# GET a single user by ID
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = next((user for user in users_db if user["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#
# POST a new user (create)
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    # Check if the provided ID already exists in the database
    existing_user = next((u for u in users_db if u["id"] == user.id), None)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this ID already exists")
    
    # If the ID is unique, store the new user
    new_user = {"id": user.id, "name": user.name, "email": user.email}
    users_db.append(new_user)
    return new_user


# PUT to update an existing user (id is taken from URL, not the body)
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserUpdate):
    user = next((user for user in users_db if user["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user["name"] = updated_user.name
    user["email"] = updated_user.email
    return user

# DELETE a user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    global users_db
    user = next((user for user in users_db if user["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    users_db = [user for user in users_db if user["id"] != user_id]
    return {"detail": "User deleted"}
